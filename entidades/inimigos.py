import pygame
import math
import random

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.velocidade = 1.5 
        self.vida = 2

        # criando um dicionário para guardar as listas de animação por direção
        self.animations = {"direita": [], "esquerda": [], "baixo": [], "cima": []}
        
        # Carrega os frames diretamente (frame por frame)
        self._carregar_frames()
        
        # estado inicial
        self.direcao = "baixo"
        self.quadro_atual = 0.0
        self.velocidade_animacao = 0.15 
        
        if len(self.animations["baixo"]) > 0:
            self.image = self.animations[self.direcao][int(self.quadro_atual)]
        else:
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 0, 0))
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ultimo_dano = 0
        self.cooldown_dano = 1000

    def _carregar_frames(self):
        # Direita
        try:
            self.animations["direita"].append(pygame.image.load("assets/sprites_entidades/inimigo/Direita 1.png").convert_alpha())
            self.animations["direita"].append(pygame.image.load("assets/sprites_entidades/inimigo/Direita 2.png").convert_alpha())
            self.animations["direita"].append(pygame.image.load("assets/sprites_entidades/inimigo/Direita 3.png").convert_alpha())
            
            # Redimensiona se necessário
            self.animations["direita"] = [pygame.transform.scale(frame, (50, 50)) for frame in self.animations["direita"]]
        except (pygame.error, FileNotFoundError):
            print("Aviso: Frames de 'direita' não encontrados")
        
        # Esquerda
        try:
            self.animations["esquerda"].append(pygame.image.load("assets/sprites_entidades/inimigo/Esquerda 1.png").convert_alpha())
            self.animations["esquerda"].append(pygame.image.load("assets/sprites_entidades/inimigo/Esquerda 2.png").convert_alpha())
            self.animations["esquerda"].append(pygame.image.load("assets/sprites_entidades/inimigo/Esquerda 3.png").convert_alpha())
            
            self.animations["esquerda"] = [pygame.transform.scale(frame, (50, 50)) for frame in self.animations["esquerda"]]
        except (pygame.error, FileNotFoundError):
            print("Aviso: Frames de 'esquerda' não encontrados")
        
        # Cima
        try:
            self.animations["cima"].append(pygame.image.load("assets/sprites_entidades/inimigo/Costas 1.png").convert_alpha())
            self.animations["cima"].append(pygame.image.load("assets/sprites_entidades/inimigo/Costas 2.png").convert_alpha())
            self.animations["cima"].append(pygame.image.load("assets/sprites_entidades/inimigo/Costas 3.png").convert_alpha())
            
            self.animations["cima"] = [pygame.transform.scale(frame, (50, 50)) for frame in self.animations["cima"]]
        except (pygame.error, FileNotFoundError):
            print("Aviso: Frames de 'cima' não encontrados")
        
        # Baixo
        try:
            self.animations["baixo"].append(pygame.image.load("assets/sprites_entidades/inimigo/Frente 1.png").convert_alpha())
            self.animations["baixo"].append(pygame.image.load("assets/sprites_entidades/inimigo/Frente 2.png").convert_alpha())
            self.animations["baixo"].append(pygame.image.load("assets/sprites_entidades/inimigo/Frente 3.png").convert_alpha())
            
            self.animations["baixo"] = [pygame.transform.scale(frame, (50, 50)) for frame in self.animations["baixo"]]
        except (pygame.error, FileNotFoundError):
            print("Aviso: Frames de 'baixo' não encontrados")

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
        # Verifica se tem frames para a direção atual
        if len(self.animations[self.direcao]) == 0:
            return
            
        # Avança o contador do quadro usando o valor quebrado pra controlar a velocidade
        self.quadro_atual += self.velocidade_animacao
        
        # Se o contador passar do máximo ou atingir o tamanho da lista de frames ele reinicia
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
        self.velocidade_animacao = 0.25 # Anima mais rápido
        
        # Se não tiver frames carregados, cria um bloco verde de fallback
        if len(self.animations["baixo"]) == 0:
            self.image = pygame.Surface((20, 20))
            self.image.fill((0, 255, 0))
        else:
            # Aplica uma tonalidade verde aos frames existentes
            for direcao in self.animations:
                for i, frame in enumerate(self.animations[direcao]): 
                    copia = frame.copy()
                    copia.fill((255, 140, 0), special_flags=pygame.BLEND_RGB_ADD)
                    self.animations[direcao][i] = copia


class Boss(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.velocidade = 1.0 
        self.vida = 30 
        self.esta_atacando = False
        self.ultimo_ataque_especial = pygame.time.get_ticks()
        self.cooldown_especial = 5000 # 5000 milissegundos = 5 segundos
        
        # Carrega frames específicos do Boss
        self._carregar_frames_boss()
    
    def _carregar_frames_boss(self):
        # Limpa as animações herdadas para colocar as do boss
        self.animations = {
            'esquerda': [],
            'direita': [],  
            'cima': [],        
            'baixo': [],
            'ataque_direita': [],
            'ataque_esquerda': []
        }
        
        # Carrega caminhada - Direita
        try:
            self.animations["direita"].append(pygame.image.load("assets/sprites_entidades/inimigo/Direita 1.png").convert_alpha())
            self.animations["direita"].append(pygame.image.load("assets/sprites_entidades/inimigo/Direita 2.png").convert_alpha())
            self.animations["direita"].append(pygame.image.load("assets/sprites_entidades/inimigo/Direita 3.png").convert_alpha())
            
            # Aumenta o tamanho do boss em relação ao inimigo normal
            self.animations["direita"] = [pygame.transform.scale(frame, (80, 80)) for frame in self.animations["direita"]]
        except (pygame.error, FileNotFoundError):
            print("Aviso: Frames de 'direita' do boss não encontrados")
        
        # Carrega caminhada - Esquerda
        try:
            self.animations["esquerda"].append(pygame.image.load("assets/sprites_entidades/inimigo/Esquerda 1.png").convert_alpha())
            self.animations["esquerda"].append(pygame.image.load("assets/sprites_entidades/inimigo/Esquerda 2.png").convert_alpha())
            self.animations["esquerda"].append(pygame.image.load("assets/sprites_entidades/inimigo/Esquerda 3.png").convert_alpha())
            
            self.animations["esquerda"] = [pygame.transform.scale(frame, (80, 80)) for frame in self.animations["esquerda"]]
        except (pygame.error, FileNotFoundError):
            print("Aviso: Frames de 'esquerda' do boss não encontrados")
        
        # Carrega caminhada - Cima
        try:
            self.animations["cima"].append(pygame.image.load("assets/sprites_entidades/inimigo/Costas 1.png").convert_alpha())
            self.animations["cima"].append(pygame.image.load("assets/sprites_entidades/inimigo/Costas 2.png").convert_alpha())
            self.animations["cima"].append(pygame.image.load("assets/sprites_entidades/inimigo/Costas 3.png").convert_alpha())
            
            self.animations["cima"] = [pygame.transform.scale(frame, (80, 80)) for frame in self.animations["cima"]]
        except (pygame.error, FileNotFoundError):
            print("Aviso: Frames de 'cima' do boss não encontrados")
        
        # Carrega caminhada - Baixo
        try:
            self.animations["baixo"].append(pygame.image.load("assets/sprites_entidades/inimigo/Frente 1.png").convert_alpha())
            self.animations["baixo"].append(pygame.image.load("assets/sprites_entidades/inimigo/Frente 2.png").convert_alpha())
            self.animations["baixo"].append(pygame.image.load("assets/sprites_entidades/inimigo/Frente 3.png").convert_alpha())
            
            self.animations["baixo"] = [pygame.transform.scale(frame, (80, 80)) for frame in self.animations["baixo"]]
        except (pygame.error, FileNotFoundError):
            print("Aviso: Frames de 'baixo' do boss não encontrados")
        
        # Carrega ataque Direita
        try:
            self.animations['ataque_direita'].append(pygame.image.load("assets/sprites_entidades/inimigo/Ataque D 1.png").convert_alpha())
            self.animations['ataque_direita'].append(pygame.image.load("assets/sprites_entidades/inimigo/Ataque D 2.png").convert_alpha())
            self.animations['ataque_direita'].append(pygame.image.load("assets/sprites_entidades/inimigo/Ataque D 3.png").convert_alpha())
            
            self.animations['ataque_direita'] = [pygame.transform.scale(frame, (90, 90)) for frame in self.animations['ataque_direita']]
        except (pygame.error, FileNotFoundError):
            print("Aviso: Frames de 'ataque_direita' do boss não encontrados")
        
        # Carrega ataque Esquerda
        try:
            self.animations['ataque_esquerda'].append(pygame.image.load("assets/sprites_entidades/inimigo/Ataque E 1.png").convert_alpha())
            self.animations['ataque_esquerda'].append(pygame.image.load("assets/sprites_entidades/inimigo/Ataque E 2.png").convert_alpha())
            self.animations['ataque_esquerda'].append(pygame.image.load("assets/sprites_entidades/inimigo/Ataque E 3.png").convert_alpha())
            
            self.animations['ataque_esquerda'] = [pygame.transform.scale(frame, (90, 90)) for frame in self.animations['ataque_esquerda']]
        except (pygame.error, FileNotFoundError):
            print("Aviso: Frames de 'ataque_esquerda' do boss não encontrados")
        
        # Define imagem inicial
        if len(self.animations['baixo']) > 0:
            self.image = self.animations['baixo'][0]
        else:
            self.image = pygame.Surface((80, 80))
            self.image.fill((0, 0, 255))
        
        self.rect = self.image.get_rect(center=(self.rect.x, self.rect.y))
    
    def update(self, jogador, grupo_inimigos):
        tempo_atual = pygame.time.get_ticks()
        
        # Se não tiver atacando anda e persegue o jogador normalmente
        if not self.esta_atacando:
            # Chama o movimento padrão que veio do Inimigo (mãe)
            super().update(jogador, grupo_inimigos)
            
            # Conta o tempo para ver se já se passaram 5 segundos
            if tempo_atual - self.ultimo_ataque_especial >= self.cooldown_especial:
                self.soltar_ataque_especial()
                
        # Se tiver atacando fica parado no lugar rodando a animação do poder
        else:
            self.animar_ataque()
     
    def soltar_ataque_especial(self):
        # Escolhe um dos ataques especiais (só esquerda e direita)
        lista_ataques = ['ataque_esquerda', 'ataque_direita']
        
        ataque_escolhido = random.choice(lista_ataques)
        
        # Verifica se tem frames para esse ataque
        if len(self.animations[ataque_escolhido]) == 0:
            self.ultimo_ataque_especial = pygame.time.get_ticks()
            return
        
        self.direcao = ataque_escolhido
        self.quadro_atual = 0.0
        self.esta_atacando = True
        print(f"Boss usou: {self.direcao}!")
                
    def animar_ataque(self):
        # Verifica se tem frames para a animação de ataque
        if len(self.animations[self.direcao]) == 0:
            self.esta_atacando = False
            return
            
        # Avança os frames do ataque um pouco mais rápido (0.20) para o efeito fluir bem
        self.quadro_atual += 0.20
        
        # Se a animação do especial chegou ao fim
        if self.quadro_atual >= len(self.animations[self.direcao]):
            self.esta_atacando = False # Termina o ataque e libera o Boss para andar
            self.direcao = 'baixo'     # Faz ele olhar para frente novamente
            self.quadro_atual = 0.0
            self.ultimo_ataque_especial = pygame.time.get_ticks() # Reseta o relógio de 5s
        else:
            # Atualiza a imagem com o frame do ataque atual
            self.image = self.animations[self.direcao][int(self.quadro_atual)]
            
    def dano_inimigo(self, projetil):
        # O Boss substitui esse método porque toma 1.5 de dano por bala
        if self.rect.colliderect(projetil.rect):  
            projetil.kill()  
            return self.receber_dano(1.5)  
        return False
