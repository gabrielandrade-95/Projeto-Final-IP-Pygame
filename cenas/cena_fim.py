import pygame
from cenas.telas_temporizadas import TelaTemporizada


class CenaFim(TelaTemporizada):
    def __init__(self, gerenciador):
        super().__init__(gerenciador, "assets/telas/tela_fim.png")

        # TOCAR MUSICA TEMA VITORIA
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/sons/musica_final.mp3")
        pygame.mixer.music.play(-1)

    def ao_terminar(self):
        self.gerenciador.ir_para_menu()
