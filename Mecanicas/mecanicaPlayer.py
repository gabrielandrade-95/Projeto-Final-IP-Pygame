import pygame
import sys

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

    def mover(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            if self.x > 0 :
                self.x -= self.velocidade #anda pra esquerda
                self.direcao_da_frente = "esquerda"  # Atualiza a direção da frente para esquerda

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            if self.x < 770 :
                self.x += self.velocidade
                self.direcao_da_frente = "direita" 

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            if self.y > 0 :
                self.y -= self.velocidade
                self.direcao_da_frente = "cima"

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            if self.y < 570 :
                self.y += self.velocidade
                self.direcao_da_frente = "baixo"

    def desenhar(self, tela):
        retangulo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(tela, self.cor, retangulo)
