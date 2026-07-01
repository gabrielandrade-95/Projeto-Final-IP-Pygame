#gerenciador.py
import pygame
import sys
from cenas.cena_menu import CenaMenu
from sistemas.jogo import Jogo


class Gerenciador:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((1024, 637))
        pygame.display.set_caption("O Cangaço")
        self.relogio = pygame.time.Clock()
        self.estado = "menu"
        self.cena_menu = CenaMenu(self)

    def iniciar_jogo(self):
        self.estado = "jogo"

    def rodar(self):
        while True:
            self.relogio.tick(60)

            if self.estado == "menu":
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    self.cena_menu.checar_eventos(evento)

                self.cena_menu.atualizar()
                self.cena_menu.desenhar(self.tela)
                pygame.display.flip()

            elif self.estado == "jogo":
                jogo = Jogo()
                jogo.rodar()
                self.estado = "menu"  # volta pro menu quando o jogo termina