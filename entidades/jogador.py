#jogador.py
import pygame
from entidades.inimigos import Boss


class Jogador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 30
        self.altura = 30
        self.velocidade = 5
        self.cor = (0, 200, 100)
        self.direcao_da_frente = "direita"  # Inicialmente, o jogador está olhando para a direita
        self.cooldown_tiro = 300  # Tempo em milissegundos (300 = meio segundo)
        self.ultimo_tiro = 0      # Relógio zera quando o jogo começa
        self.vida_jogador = 10

        # Criar o rect para colisões
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)

        #Carregar os Efeitos Sonoros
        self.som_faca = pygame.mixer.Sound("assets/sons/faca.wav")
        self.som_pistola = pygame.mixer.Sound("assets/sons/tiro.wav")
        self.som_espingarda = pygame.mixer.Sound("assets/sons/espingarda.wav")
        self.som_pitu = pygame.mixer.Sound("assets/sons/pitu.wav")

    def mover(self, grupo_inimigos=None):
        teclas = pygame.key.get_pressed()
        vel_x = 0
        vel_y = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            if self.x > 0:
                self.x -= self.velocidade #anda pra esquerda
                self.direcao_da_frente = "esquerda"  # Atualiza a direção da frente para esquerda

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            if self.x < 994:
                self.x += self.velocidade
                self.direcao_da_frente = "direita"

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            if self.y > 0:
                self.y -= self.velocidade
                self.direcao_da_frente = "cima"

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            if self.y < 607:
                self.y += self.velocidade
                self.direcao_da_frente = "baixo"

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