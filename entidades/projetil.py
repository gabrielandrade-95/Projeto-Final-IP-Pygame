import pygame

class Projetil(pygame.sprite.Sprite):
    # aceitar o vel_x e vel_y pra a diagonal da espingarda
    def __init__(self, x, y, direcao, vel_x=None, vel_y=None):
        super().__init__()
        
        self.direcao = direcao
        
        # Define o formato do projétil baseado na direção principal
        if self.direcao in ["cima", "baixo"]:
            self.image = pygame.Surface((4, 10))
        else:
            self.image = pygame.Surface((10, 4))

        self.image.fill((255, 255, 0)) # Amarelo
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        
        self.velocidade = 15

        # Se passarmos velocidades manuais (Shotgun) usamos elas.
        # Se não (Pistola), calcula o padrão reto:
        if vel_x is not None and vel_y is not None:
            self.vel_x = vel_x
            self.vel_y = vel_y
        else:
            self.vel_x = 0
            self.vel_y = 0
            if self.direcao == "direita":
                self.vel_x = self.velocidade
            elif self.direcao == "esquerda":
                self.vel_x = -self.velocidade
            elif self.direcao == "cima":
                self.vel_y = -self.velocidade   
            elif self.direcao == "baixo":
                self.vel_y = self.velocidade
            
    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Remove o projétil se sair da tela
        if (self.rect.x < 0 or self.rect.x > 800 or 
            self.rect.y < 0 or self.rect.y > 600):
            self.kill()