#jogador.py
import pygame
from entidades.inimigos import Boss


class Jogador:
    def __init__(self, x, y):
        tamanho = (64,64)
        self.x = x
        self.y = y
        self.largura = tamanho[0]
        self.altura = tamanho[1]
        self.velocidade = 5
        self.direcao_da_frente = "direita"  # Inicialmente, o jogador está olhando para a direita
        self.cooldown_tiro = 300  # Tempo em milissegundos (300 = meio segundo)
        self.ultimo_tiro = 0      # Relógio zera quando o jogo começa
        self.vida_jogador = 10
        self.arma_equipada = "desarmado"
        self.sprite_atual = 0
        self.velocidade_animacao = 0.15

        self.animacoes = {
            "desarmado" : {
                "direita" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/direitadesarmado1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/direitadesarmado2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/direitadesarmado3.png").convert_alpha(),
                    tamanho
                )],
                "esquerda" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/esquerdadesarmado1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/esquerdadesarmado2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/esquerdadesarmado3.png").convert_alpha(),
                    tamanho
                )],
                "cima" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/cimadesarmado1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/cimadesarmado2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/cimadesarmado3.png").convert_alpha(),
                    tamanho
                )],
                "baixo" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/baixodesarmado1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/baixodesarmado2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/baixodesarmado3.png").convert_alpha(),
                    tamanho
                )]
            },
            "Peixeira" : {
                "direita" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/direitapeixeira1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/direitapeixeira2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/direitapeixeira3.png").convert_alpha(),
                    tamanho
                )],
                "esquerda" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/esquerdapeixeira1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/esquerdapeixeira2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/esquerdapeixeira3.png").convert_alpha(),
                    tamanho
                )],
                "cima" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/cimapeixeira1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/cimapeixeira2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/cimapeixeira3.png").convert_alpha(),
                    tamanho
                )],
                "baixo" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/baixopeixeira1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/baixopeixeira2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/baixopeixeira3.png").convert_alpha(),
                    tamanho
                )]
            },
            "Revolver" : {
                "direita" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/revolverdireita1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/revolverdireita2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/revolverdireita3.png").convert_alpha(),
                    tamanho
                )],
                "esquerda" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/revolveresquerda1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/revolveresquerda2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/revolveresquerda3.png").convert_alpha(),
                    tamanho
                )],
                "cima" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/revolvercima1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/revolvercima2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/revolvercima3.png").convert_alpha(),
                    tamanho
                )],
                "baixo" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/revolverbaixo1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/revolverbaixo2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/revolverbaixo3.png").convert_alpha(),
                    tamanho
                )]
            },
            "Espingarda" : {
                "direita" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/espingardadireita1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/espingardadireita2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/espingardadireita3.png").convert_alpha(),
                    tamanho
                )],
                "esquerda" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/espingardaesquerda1.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/espingardaesquerda2.png").convert_alpha(),
                    tamanho
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/espingardaesquerda3.png").convert_alpha(),
                    tamanho
                )],
                "cima" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/espingardacima1.png").convert_alpha(),
                    (48,64)
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/espingardacima2.png").convert_alpha(),
                    (48,64)
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/espingardacima3.png").convert_alpha(),
                    (48,64)
                )],
                "baixo" : [pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/espingardabaixo1.png").convert_alpha(),
                    (48,64)
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/espingardabaixo2.png").convert_alpha(),
                    (48,64)
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/sprites_entidades/espingardabaixo3.png").convert_alpha(),
                    (48,64)
                )]
            }
        }
        self.image = self.animacoes[self.arma_equipada]["direita"][0]

        # Criar o rect para colisões
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)

        #Carregar os Efeitos Sonoros
        self.som_faca = pygame.mixer.Sound("assets/sons/faca.wav")
        self.som_pistola = pygame.mixer.Sound("assets/sons/tiro.wav")
        self.som_espingarda = pygame.mixer.Sound("assets/sons/espingarda.wav")
        self.som_pitu = pygame.mixer.Sound("assets/sons/pitu.wav")

    def mover(self, grupo_inimigos=None):
        movendo = False

        teclas = pygame.key.get_pressed()
        vel_x = 0
        vel_y = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            if self.x > 0:
                self.x -= self.velocidade #anda pra esquerda
                self.direcao_da_frente = "esquerda"  # Atualiza a direção da frente para esquerda
                movendo = True

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            if self.x < 1024-64:
                self.x += self.velocidade
                self.direcao_da_frente = "direita"
                movendo = True

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            if self.y > 0:
                self.y -= self.velocidade
                self.direcao_da_frente = "cima"
                movendo = True

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            if self.y < 637-64:
                self.y += self.velocidade
                self.direcao_da_frente = "baixo"
                movendo = True

        # Força de empurrão dos inimigos
        if grupo_inimigos:
            for inimigo in grupo_inimigos:
                if self.rect.colliderect(inimigo.rect):
                    d_X = self.rect.centerx - inimigo.rect.centerx
                    d_y = self.rect.centery - inimigo.rect.centery
                    dist = (d_X**2 + d_y**2) ** 0.5
                    if dist != 0:
                        vel_x += (d_X / dist) * 3
                        vel_y += (d_y / dist) * 3

        self.x += vel_x
        self.y += vel_y

        if movendo:
            self.animar()
        else:
            self.sprite_atual = 0
            self.image = self.animacoes[self.arma_equipada][self.direcao_da_frente][0]

        # Atualiza o rect do jogador após receber a movimentação e empurrões
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Limita a posição no eixo X
        if self.rect.left < 0:
            self.rect.left = 0
            self.x = self.rect.x  # sincroniza variável interna com a borda esquerda
        elif self.rect.right > 1024:
            self.rect.right = 1024
            self.x = self.rect.x  # sincroniza variável interna com a borda direita
        
        # Limita a posição no eixo Y
        if self.rect.top < 0:
            self.rect.top = 0
            self.y = self.rect.y  # sincroniza variável interna com o topo
        elif self.rect.bottom > 637:
            self.rect.bottom = 637
            self.y = self.rect.y  # sincroniza variável interna com a base

    def dano_jogador(self, grupo_inimigos):
        tempo_atual = pygame.time.get_ticks()

        posicao_jogador = self.rect.centerx  # pega a posição X do jogador
    
        for inimigo in grupo_inimigos:
            if isinstance(inimigo, Boss):
                posicao_boss = inimigo.rect.centerx
                if abs(posicao_jogador - posicao_boss) <= 10:
                    if tempo_atual - inimigo.ultimo_dano >= inimigo.cooldown_dano:
                        print("Deu dano no jogador")
                        self.vida_jogador -= 1.5 #dano do boss
                        inimigo.ultimo_dano = tempo_atual
                        return True
            else:
                if self.rect.colliderect(inimigo.rect):
                    if tempo_atual - inimigo.ultimo_dano >= inimigo.cooldown_dano:
                        print("Deu dano no jogador")
                        self.vida_jogador -= 0.35 #dano do inimigo
                        inimigo.ultimo_dano = tempo_atual
                        return True
        return False

    def desenhar(self, tela):
        tela.blit(self.image, (self.x, self.y))

    def atualizar_arma(self, arma_ativa):
        self.arma_equipada = arma_ativa
        
        # verifica se a arma existe nas animações
        if self.arma_equipada not in self.animacoes:
            print(f"Aviso: Arma '{self.arma_equipada}' não encontrada nas animações")
            return
        
        # verifica se a direção existe
        if self.direcao_da_frente not in self.animacoes[self.arma_equipada]:
            print(f"Aviso: Direção '{self.direcao_da_frente}' não encontrada para '{self.arma_equipada}'")
            return
        
        # verifica se tem frames
        if len(self.animacoes[self.arma_equipada][self.direcao_da_frente]) == 0:
            print(f"Aviso: Nenhum frame encontrado para '{self.arma_equipada}' na direção '{self.direcao_da_frente}'")
            return
        
        self.image = self.animacoes[self.arma_equipada][self.direcao_da_frente][0]

    def animar(self):
        frames = self.animacoes[self.arma_equipada][self.direcao_da_frente]

        self.sprite_atual += self.velocidade_animacao

        if self.sprite_atual >= len(frames):
            self.sprite_atual = 0

        self.image = frames[int(self.sprite_atual)]