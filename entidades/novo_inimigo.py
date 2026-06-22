import pygame
import random

class Inimigo(pygame.sprite.Sprite) :
    def __init__(self, x, y) :
        super().__init__()

        self.image = pygame.Surface((20,20)) # Os inimigos são quadraddos 20x20
        self.image.fill((255,0,0)) # Eles são vermelhos
        self.rect = self.image.get_rect() # A função get_rect gera um retângulo que cobre toda a imagem do inimigo que vai servir para as colisões
        self.rect.x = x # retangulo de colisão tem largura X
        self.rect.y = y # retangulo de colisão tem altura Y
        
        self.velocidade = 1.5 # Velocidade do inimigo é 1.5
        
        # Variáveis para controle de dano
        self.ultimo_dano = 0
        self.cooldown_dano = 1000 # O inimigo pode causar dano a cada 1 segundo (1000 milissegundos)


    def update(self, jogador, grupo_inimigos): # Método para atualizar a posição do inimigo (seguir o jogador)
        # O método recebe o player como parâmetro, pois serão utilizadas as coordenadas dele para calcular o movimento do inimigo

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
                # Calcula vetor de repulsão
                distancia_x = self.rect.centerx - inimigo.rect.centerx
                distancia_y = self.rect.centery - inimigo.rect.centery
                dist = (distancia_x**2 + distancia_y**2) ** 0.5
                    
                if dist != 0:
                    # Afasta na direção oposta
                    vel_x += (distancia_x / dist) * 3  # força de repulsão = 3
                    vel_y += (distancia_y / dist) * 3
        
        self.rect.x += vel_x
        self.rect.y += vel_y
    
    def dano_inimigo (self, projetil):
        if self.rect.colliderect(projetil.rect): # Se o retângulo do inimigo colidir com o retângulo do projetil
        
            self.kill() # Mata o inimigo
            projetil.kill() # Mata o projetil
            return True
        return False
    
 