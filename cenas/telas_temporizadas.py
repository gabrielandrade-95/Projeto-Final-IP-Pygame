#Base para telas que aparecem sozinhas, com fade in/out, e depois de um tempo trocam de estado sozinhas (créditos e tela fim usam isso)

import pygame

class TelaTemporizada:


    DURACAO_TOTAL = 10000   
    DURACAO_FADE = 2000     

    def __init__(self, gerenciador, caminho_imagem):
        self.gerenciador = gerenciador

        fundo = pygame.image.load(caminho_imagem).convert()
        self.fundo = pygame.transform.scale(fundo, (1024, 637))

        self.inicio = pygame.time.get_ticks()

        self.overlay = pygame.Surface((1024, 637))
        self.overlay.fill((0, 0, 0))

    def checar_eventos(self, evento):
        pass

    def atualizar(self):
        tempo_decorrido = pygame.time.get_ticks() - self.inicio
        if tempo_decorrido >= self.DURACAO_TOTAL:
            self.ao_terminar()

    def ao_terminar(self):
        #cada tela decide para onde ir quando o tempo acaba
        raise NotImplementedError

    def _calcular_alpha(self):
        tempo_decorrido = pygame.time.get_ticks() - self.inicio

        if tempo_decorrido < self.DURACAO_FADE:
            return int(255 * (1 - tempo_decorrido / self.DURACAO_FADE))

        tempo_restante = self.DURACAO_TOTAL - tempo_decorrido
        if tempo_restante < self.DURACAO_FADE:
            return int(255 * (1 - max(tempo_restante, 0) / self.DURACAO_FADE))

        return 0

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

        alpha = self._calcular_alpha()
        if alpha > 0:
            self.overlay.set_alpha(alpha)
            tela.blit(self.overlay, (0, 0))