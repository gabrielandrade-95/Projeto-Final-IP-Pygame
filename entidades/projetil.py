import pygame

class Projetil (pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        super().__init__()
        
        # Cria a imagem da bala 
        self.image = pygame.Surface((10, 4))
        self.image.fill((255, 255, 0)) # Amarelo
        self.rect = self.image.get_rect()
        
        #posiciona o projetil no centro do jogador
        self.rect.x = x
        self.rect.y = y
        
        
        self.velocidade = 15
        self.direcao = direcao
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
        
        # tira o projetil se ele sair da tela
        if (self.rect.x < 0 or self.rect.x > 800 or 
            self.rect.y < 0 or self.rect.y > 600):
            self.kill()

    