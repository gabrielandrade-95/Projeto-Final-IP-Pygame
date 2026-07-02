import pygame
import math
import random

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.velocidade = 1.5 
        self.vida = 2

        self.sprite_largura = 64
        self.sprite_altura = 64
        
        # Tenta carregar o spritesheet. Se não achar, cria um bloco vermelho reserva
        try:
            caminho_spritesheet = "assets/sprites_entidades/spritesheet_inimigo.png"
            self.spritesheet = pygame.image.load(caminho_spritesheet).convert()
            self.spritesheet.set_colorkey((255, 255, 255)) # Branco vira transparente
            self.tem_sprite = True
        except (pygame.error, FileNotFoundError):
            # Se a imagem não existir ainda, gera um bloco vermelho padrão para não quebrar o jogo
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 0, 0))
            self.tem_sprite = False
            
        # criando um dicionário para guardar as listas de animação por direção
        self.animations = {"direita": [], "esquerda": [], "baixo": [], "cima": []}
         
        # recorta os sprites e preenche as listas se a imagem existir
        if self.tem_sprite:
            linha = 0
            for direcao in ["direita", "esquerda", "baixo", "cima"]:
                for coluna in range(6):
                    x_crop = coluna * self.sprite_largura
                    y_crop = linha * self.sprite_altura
                    
                    sprite = self.spritesheet.subsurface((x_crop, y_crop, self.sprite_largura, self.sprite_altura))
                    sprite = pygame.transform.scale(sprite, (35, 35))
                    
                    self.animations[direcao].append(sprite)
                     
                linha += 1
        
        # estado inicial
        self.direcao = "baixo"
        self.quadro_atual = 0.0
        self.velocidade_animacao = 0.15 
        
        if self.tem_sprite:
            self.image = self.animations[self.direcao][int(self.quadro_atual)]
        else:
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 0, 0))
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ultimo_dano = 0
        self.cooldown_dano = 1000

    def update(self, jogador, grupo_inimigos): 
        # Método para atualizar a posição do inimigo (seguir o jogador)
        dx = jogador.rect.centerx - self.rect.centerx
        dy = jogador.rect.centery - self.rect.centery
        distancia = (dx**2 + dy**2) ** 0.5

        if distancia != 0:
            dx /= distancia
            dy /= distancia

        vel_x = dx * self.velocidade
        vel_y = dy * self.velocidade
        
        if abs(vel_x) > abs(vel_y):
            self.direcao = "direita" if vel_x > 0 else "esquerda"
        else:
            self.direcao = "baixo" if vel_y > 0 else "cima"

        # Repulsão com outros inimigos
        for inimigo in grupo_inimigos:
            if inimigo != self and self.rect.colliderect(inimigo.rect):
                distancia_x = self.rect.centerx - inimigo.rect.centerx
                distancia_y = self.rect.centery - inimigo.rect.centery
                dist = (distancia_x**2 + distancia_y**2) ** 0.5

                if dist != 0:
                    vel_x += (distancia_x / dist) * 3  # força de repulsão = 3
                    vel_y += (distancia_y / dist) * 3

        self.rect.x += vel_x
        self.rect.y += vel_y
        self.animar()
        
    def animar(self):
        if not self.tem_sprite:
            return
            
        # avança o contador do quadro usando o valor quebrado pra controlar a velocidade
        self.quadro_atual += self.velocidade_animacao
        
        # se o contador passar do máximo ou atingir o tamanho da lista de frames ele reinicia
        if self.quadro_atual >= len(self.animations[self.direcao]):
            self.quadro_atual = 0.0
            
        self.image = self.animations[self.direcao][int(self.quadro_atual)]

    def receber_dano(self, quantidade):
        self.vida -= quantidade
        if self.vida <= 0:
            self.kill() 
            return True 
        return False 

    def dano_inimigo(self, projetil):
        if self.rect.colliderect(projetil.rect): 
            projetil.kill() 
            return self.receber_dano(1) 
        return False


class InimigoRapido(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        self.velocidade = 2.5 
        self.vida = 2
        
        # se não tiver imagem, aplica o bloco verde, se tiver, reaplica a animação verde.
        if not self.tem_sprite:
            self.image = pygame.Surface((20, 20))
            self.image.fill((0, 255, 0)) # Verde
        else:
            self.velocidade_animacao = 0.25 # anima mais rápido
            for direcao in self.animations:
                for i, frame in enumerate(self.animations[direcao]): 
                    copia = frame.copy()
                    copia.fill((0, 100, 0), special_flags=pygame.BLEND_RGB_ADD)
                    self.animations[direcao][i] = copia


class Boss(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.velocidade = 1.0 
        self.vida = 30 
        
        self.sprite_largura = 140
        self.sprite_altura = 115
        
        try:
            caminho_spritesheet = "assets/sprites_entidades/Boss.png"
            self.spritesheet = pygame.image.load(caminho_spritesheet).convert()
            self.spritesheet.set_colorkey((255, 255, 255)) 
            self.tem_sprite = True
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 0, 255))  # azul caso falhe
            self.rect = self.image.get_rect(center=(x, y))
            self.tem_sprite = False
            return
        
        # temporizador de habilidade
        self.ultimo_ataque_especial = pygame.time.get_ticks()
        self.cooldown_especial = 5000 # 5000 milissegundos = 5 segundos
        self.esta_atacando = False
        
        if self.tem_sprite:
            self.animations = {
                'esquerda': [],
                'direita': [],  
                'cima': [],        
                'baixo': [],       
                'ataque_tridente': [],
                'ataque_fogo': [],    
                'chuva_tridentes': [], 
                'portal_caos': []    
            }
            direcoes_caminhada = ['esquerda', 'direita', 'cima', 'baixo']
            # mesma lógica, porém, como o spritesheet é diferente o for fica diferente
            for linha, direcao in enumerate(direcoes_caminhada):
                for coluna in range(8):
                    x_crop = coluna * self.sprite_largura
                    y_crop = linha * self.sprite_altura
                    
                    try:
                        sprite = self.spritesheet.subsurface((x_crop, y_crop, self.sprite_largura, self.sprite_altura))
                        sprite = pygame.transform.scale(sprite, (80, 80)) # Tamanho dele na tela
                        self.animations[direcao].append(sprite)
                    except pygame.error:
                        pass # previne erros se passar da borda da imagem
                    
            # cortando os ataques especiais
            y_linha_4 = 4 * self.sprite_altura
            for coluna in range(4): # lâmina/Tridente cortando
                try:
                    sprite = self.spritesheet.subsurface((coluna * self.sprite_largura, y_linha_4, self.sprite_largura, self.sprite_altura))
                    self.animations['ataque_tridente'].append(pygame.transform.scale(sprite, (90, 90)))
                except pygame.error:
                    pass
                
            for coluna in range(4, 11): # lançando bola de fogo / explosão
                try:
                    sprite = self.spritesheet.subsurface((coluna * self.sprite_largura, y_linha_4, self.sprite_largura, self.sprite_altura))
                    self.animations['ataque_fogo'].append(pygame.transform.scale(sprite, (90, 90)))
                except pygame.error:
                    pass

            y_linha_5 = 5 * self.sprite_altura
            for coluna in range(7):
                try:
                    sprite = self.spritesheet.subsurface((coluna * self.sprite_largura, y_linha_5, self.sprite_largura, self.sprite_altura))
                    self.animations['chuva_tridentes'].append(pygame.transform.scale(sprite, (95, 95)))
                except pygame.error:
                    pass
                
            for coluna in range(7, 11):
                try:
                    sprite = self.spritesheet.subsurface((coluna * self.sprite_largura, y_linha_5, self.sprite_largura, self.sprite_altura))
                    self.animations['portal_caos'].append(pygame.transform.scale(sprite, (100, 100)))
                except pygame.error:
                    pass
                
            # imagem inicial
            if self.animations['baixo']:
                self.image = self.animations['baixo'][0]
            self.rect = self.image.get_rect(center=(x, y))
    
    def update(self, jogador, grupo_inimigos):
        tempo_atual = pygame.time.get_ticks()
        
        # se não tiver atacando anda e persegue o jogador normalmente
        if not self.esta_atacando:
            # Chama o movimento padrão que veio do Inimigo (mãe)
            super().update(jogador, grupo_inimigos)
            
            # Conta o tempo para ver se já se passaram 5 segundos
            if tempo_atual - self.ultimo_ataque_especial >= self.cooldown_especial:
                self.soltar_ataque_especial()
                
        # se tiver atacando fica parado no lugar rodando a animação do poder
        else:
            self.animar_ataque()
     
    def soltar_ataque_especial(self):
        if not self.tem_sprite:
            self.ultimo_ataque_especial = pygame.time.get_ticks()
            return
            
        # escolhe um dos ataques especiais cortados do dicionário
        lista_ataques = ['ataque_tridente', 'ataque_fogo', 'chuva_tridentes', 'portal_caos']
        
        self.direcao = random.choice(lista_ataques)
        self.quadro_atual = 0.0
        self.esta_atacando = True
        print(f"Boss usou: {self.direcao}!")
                
    def animar_ataque(self):
        if not self.tem_sprite:
            self.esta_atacando = False
            return
            
        # avança os frames do ataque um pouco mais rápido (0.20) para o efeito fluir bem
        self.quadro_atual += 0.20
        
        # se a animação do especial chegou ao fim
        if self.quadro_atual >= len(self.animations[self.direcao]):
            self.esta_atacando = False # termina o ataque e libera o Boss para andar
            self.direcao = 'baixo'     # faz ele olhar para frente novamente
            self.quadro_atual = 0.0
            self.ultimo_ataque_especial = pygame.time.get_ticks() # reseta o relógio de 5s
        else:
            # atualiza a imagem com o frame do ataque atual
            self.image = self.animations[self.direcao][int(self.quadro_atual)]
            
    def dano_inimigo(self, projetil):
        # O Boss substitui esse método porque toma 1.5 de dano por bala
        if self.rect.colliderect(projetil.rect):  
            projetil.kill()  
            return self.receber_dano(1.5)  
        return False
