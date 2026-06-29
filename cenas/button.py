import pygame

class button():
    def __init__(self, x, y, image, imagePressionado):
        self.image = image
        self.imagePressionado = imagePressionado
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.pressionado = False
        self.tempoPressionado = 0

    def draw(self, tela):
        imagemAtual = self.image
        clicado = False #armazenar se botão foi clicado

        # Verificar clique
        clique = pygame.mouse.get_pressed()[0]
        mousePos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mousePos) and clique:
            self.pressionado = True
            self.tempoPressionado = pygame.time.get_ticks()

        # Trocar sprite enquanto estiver dentro do tempo
        if self.pressionado:
            if pygame.time.get_ticks() - self.tempoPressionado < 150:
                imagemAtual = self.imagePressionado
            else:
                self.pressionado = False  # reseta depois dos 150ms
                clicado = True
        tela.blit(imagemAtual, (self.rect.x, self.rect.y))
        return clicado
    
    def reset(self): # reset de botão para mudança de tela
        self.pressionado = False
        self.tempoPressionado = 0