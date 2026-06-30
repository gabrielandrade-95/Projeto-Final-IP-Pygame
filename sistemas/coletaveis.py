#coletaveis.py
import pygame
from abc import ABC, abstractmethod


class ColetavelBase(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, nome, caminho_imagem):
        super().__init__()
        self.x = x
        self.y = y
        self.nome = nome
        self.coletado = False

        try:
            imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
            self.imagem = pygame.transform.scale(imagem_original, (40, 40))
        except pygame.error:
            self.imagem = pygame.Surface((30, 30))
            self.imagem.fill((255, 0, 0))

        self.largura = self.imagem.get_width()
        self.altura = self.imagem.get_height()

    def obter_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def desenhar(self, tela):
        if not self.coletado:
            tela.blit(self.imagem, (self.x, self.y))

    def processar_coleta(self, jogador, inventario):
        if self.coletado:
            return

        rect_jogador = pygame.Rect(jogador.x, jogador.y, jogador.largura, jogador.altura)
        if rect_jogador.colliderect(self.obter_rect()):
            self.coletado = True
            inventario.adicionar_arma(self.nome)


class Peixeira(ColetavelBase):
    def __init__(self, x, y):
        super().__init__(x, y, "Peixeira", "assets/peixeira.png")


class Revolver(ColetavelBase):
    def __init__(self, x, y):
        super().__init__(x, y, "Revolver", "assets/revolver.png")


class Espingarda(ColetavelBase):
    def __init__(self, x, y):
        super().__init__(x, y, "Espingarda", "assets/espingarda.png")


class Inventario:
    ARMAS = ["Peixeira", "Revolver", "Espingarda"]

    def __init__(self):
        self.armas_liberadas = {arma: False for arma in self.ARMAS}
        self.arma_ativa = None

        try:
            hud = pygame.image.load("assets/hud_inventario.png").convert_alpha()
            self.imagem_hud_fundo = pygame.transform.scale(hud, (300, 150))
        except pygame.error:
            self.imagem_hud_fundo = pygame.Surface((300, 150))

        self.imagem_hud = {}
        for nome in self.ARMAS:
            try:
                img = pygame.image.load(f"assets/{nome.lower()}.png").convert_alpha()
                self.imagem_hud[nome] = pygame.transform.scale(img, (45, 45))
            except pygame.error:
                surf = pygame.Surface((40, 40))
                surf.fill((100, 100, 100))
                self.imagem_hud[nome] = surf

    def adicionar_arma(self, nome_arma):
        if nome_arma in self.armas_liberadas:
            self.armas_liberadas[nome_arma] = True
            if self.arma_ativa is None:
                self.arma_ativa = nome_arma
            print(f"{nome_arma} adicionada ao inventário!")

    def trocar_arma(self):
        teclas = pygame.key.get_pressed()
        mapeamento = {
            pygame.K_1: "Peixeira",
            pygame.K_2: "Revolver",
            pygame.K_3: "Espingarda",
        }
        for tecla, arma in mapeamento.items():
            if teclas[tecla] and self.armas_liberadas[arma]:
                self.arma_ativa = arma
                break

    def desenhar_hud(self, tela):
        x_hud, y_hud = 250, 450
        tela.blit(self.imagem_hud_fundo, (x_hud, y_hud))

        x_inicial = x_hud + 50
        y_arma = y_hud + 65
        largura_bloco = 72

        for i, nome in enumerate(self.ARMAS):
            x_arma = x_inicial + i * largura_bloco

            if self.armas_liberadas[nome]:
                tela.blit(self.imagem_hud[nome], (x_arma, y_arma))

            if self.arma_ativa == nome:
                borda = pygame.Rect(x_arma - 1, y_arma - 1, 42, 42)
                pygame.draw.rect(tela, (255, 255, 255), borda, 2)