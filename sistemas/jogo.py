import pygame
import sys
from Mecanicas.mecanicaPlayer import Jogador 

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("O Cangaço")
        self.rodando = True
        self.relogio = pygame.time.Clock()

        # Cria o jogador usando a classe que veio da Mecanicas
        self.player = Jogador(400, 300)

    def rodar(self):
        # loop 
        while self.rodando:
            self.checar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(60)

        pygame.quit()
        sys.exit()

    def checar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

    def atualizar(self):
        # calculando o movimento do jogador
        self.player.mover()

    def desenhar(self):
        self.tela.fill((40, 44, 52)) # Cor de fundo
        
        self.player.desenhar(self.tela)

        pygame.display.flip()