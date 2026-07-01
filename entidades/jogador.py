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
                "direita" : [],
                "esquerda" : [],
                "cima" : [],
                "baixo" : []
            },
            "Espingarda" : {
                "direita" : [],
                "esquerda" : [],
                "cima" : [],
                "baixo" : []
            }
        }
        self.image = self.animacoes[self.arma_equipada]["direita"][0]

        # Criar o rect para colisões
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)

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
        retangulo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(tela, self.cor, retangulo)

    def atualizar_arma(self, arma) :
        self.arma_equipada = arma
        self.sprite_atual = 0
        self.image = self.animacoes[self.arma_equipada][self.direcao_da_frente][0]

    def animar(self):
        frames = self.animacoes[self.arma_equipada][self.direcao_da_frente]

        self.sprite_atual += self.velocidade_animacao

        if self.sprite_atual >= len(frames):
            self.sprite_atual = 0

        self.image = frames[int(self.sprite_atual)]