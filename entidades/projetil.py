import pygame

class Projetil (pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        super().__init__()
        
        # Cria a imagem da bala 
        self.direcao = direcao # Primeiro é verificada a direção em que o projétil está sendo disparado
        if self.direcao == "cima" or self.direcao == "baixo" :
            self.image = pygame.Surface((4,10)) # Projétil vertical
        else :
            self.image = pygame.Surface((10,4)) # Projétil horizontal

        self.image.fill((255, 255, 0)) # Amarelo
        self.rect = self.image.get_rect()
        
        #posiciona o projetil no centro do jogador
        self.rect.x = x
        self.rect.y = y
        
        
        self.velocidade = 15
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