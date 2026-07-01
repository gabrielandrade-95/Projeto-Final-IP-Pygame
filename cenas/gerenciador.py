#gerenciador.py
import pygame
import sys
from cenas.cena_menu import CenaMenu
from cenas.cena_pause import CenaPause
from cenas.cena_over import CenaOver
from sistemas.jogo import Jogo


class Gerenciador:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((1024, 637))
        pygame.display.set_caption("O Cangaço")
        self.relogio = pygame.time.Clock()
        self.estado = "menu"
        self.jogo_atual = None
        self.cena_menu = CenaMenu(self)

    def iniciar_jogo(self):
        self.estado = "jogo"

    def retomar_jogo(self):
        self.estado = "jogo"

    def reiniciar_jogo(self):
        self.jogo_atual = None
        self.estado = "jogo"

    def ir_para_menu(self):
        self.jogo_atual = None
        self.estado = "menu"

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
                if self.jogo_atual is None:
                    self.jogo_atual = Jogo()
                self.jogo_atual.rodando = True
                self.jogo_atual.pausado = False
                self.jogo_atual.rodar()

                if self.jogo_atual.pausado:
                    self.estado = "pause"
                elif self.jogo_atual.game_over:
                    self.estado = "over"
                else:
                    self.jogo_atual = None
                    self.estado = "menu"

            elif self.estado == "pause":
                cena_pause = CenaPause(self)
                while self.estado == "pause":
                    self.relogio.tick(60)
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        cena_pause.checar_eventos(evento)
                    cena_pause.atualizar()
                    cena_pause.desenhar(self.tela)
                    pygame.display.flip()

            elif self.estado == "over":
                cena_over = CenaOver(self)
                while self.estado == "over":
                    self.relogio.tick(60)
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        cena_over.checar_eventos(evento)
                    cena_over.atualizar()
                    cena_over.desenhar(self.tela)
                    pygame.display.flip()