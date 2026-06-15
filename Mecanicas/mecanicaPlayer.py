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

    def mover(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            if self.x > 0 :
                self.x -= self.velocidade

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            if self.x < 770 :
                self.x += self.velocidade

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            if self.y > 0 :
                self.y -= self.velocidade

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            if self.y < 570 :
                self.y += self.velocidade

    def desenhar(self, tela):
        retangulo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(tela, self.cor, retangulo)
