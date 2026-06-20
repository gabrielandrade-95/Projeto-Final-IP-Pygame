import pygame

class Inimigo(pygame.sprite.Sprite) :
    def __init__(self, x, y) :
        super().__init__()

        self.image = pygame.Surface((20,20)) # Os inimigos são quadraddos 20x20
        self.image.fill((255,0,0)) # Eles são vermelhos
        self.rect = self.image.get_rect() # A função get_rect gera um retângulo que cobre toda a imagem do inimigo que vai servir para as colisões
        self.rect.x = x # retangulo de colisão tem largura X
        self.rect.y = y # retangulo de colisão tem altura Y
        
        self.velocidade = 2 # Velocidade do inimigo é 2

    def update(self, jogador): # Método para atualizar a posição do inimigo (seguir o jogador)
        # O método recebe o player como parâmetro, pois serão utilizadas as coordenadas dele para calcular o movimento do inimigo

        dx = jogador.rect.centerx - self.rect.centerx
        dy = jogador.rect.centery - self.rect.centery

        distancia = (dx**2 + dy**2) ** 0.5

        if distancia != 0:
            dx /= distancia
            dy /= distancia

        self.rect.x += dx * self.velocidade
        self.rect.y += dy * self.velocidade