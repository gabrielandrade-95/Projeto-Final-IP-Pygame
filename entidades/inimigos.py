import pygame
import math

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.velocidade = 1.5 # Velocidade do inimigo é 1.5
        self.image = pygame.Surface((20,20)) # Os inimigos são quadrados 20x20
        self.image.fill((255,0,0)) # Eles são vermelhos
        self.rect = self.image.get_rect() # A função get_rect gera um retângulo
        self.rect.x = x 
        self.rect.y = y 

        # Variáveis para controle de dano
        self.ultimo_dano = 0
        self.cooldown_dano = 1000 
        self.vida = 2

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

    def receber_dano(self, quantidade):
        #Método geral para qualquer fonte de dano (bala ou peixeira)
        self.vida -= quantidade
        if self.vida <= 0:
            self.kill() # Remove o inimigo do jogo
            return True # Morreu
        return False # Sobreviveu

    def dano_inimigo(self, projetil):
        #Gerencia o dano recebido por projéteis (balas)
        if self.rect.colliderect(projetil.rect): 
            projetil.kill() # Mata o projetil
            return self.receber_dano(1) # Cada projétil faz 1 de dano base
        return False


class InimigoRapido(Inimigo):
    def __init__(self, x, y):
        # Chama o construtor do Inimigo original
        super().__init__(x, y)

        # Modifica apenas o que o Inimigo Rápido tem de diferente
        self.velocidade = 2.5 
        self.vida = 1

        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0)) # Verde
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Boss(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.velocidade = 1.0 
        self.vida = 30 
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))  # Azul
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def dano_inimigo(self, projetil):
        #O Boss substitui esse método porque toma 1.5 de dano por bala
        if self.rect.colliderect(projetil.rect):  
            projetil.kill()  
            return self.receber_dano(1.5)  
        return False