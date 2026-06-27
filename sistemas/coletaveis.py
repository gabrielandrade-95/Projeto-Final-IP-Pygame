import pygame
from abc import ABC, abstractmethod
from sistemas.colisao import checar_colisao_retangulos


class ColetavelBase(pygame.sprite.Sprite, ABC):

    def __init__(self, x, y, nome, caminho_imagem):
        super().__init__()
        self.x = x
        self.y = y
        self.nome = nome
        self.coletado = False

        try:                                            #cria o "erro"
            self.imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
            self.imagem = pygame.transform.scale(self.imagem_original, (40, 40))

        except pygame.error:
            self.imagem = pygame.Surface((30, 30))
            self.imagem.fill((255, 0, 0))

        self.largura = self.imagem.get_width()
        self.altura = self.imagem.get_height()

    def obter_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def desenhar(self, tela):
        #desenha o item na tela se ele n foi pego ainda
        if not self.coletado:
            #desenha a arma na tela 
            tela.blit(self.imagem, (self.x, self.y))

    def processar_coleta(self, jogador, inventario):
        if self.coletado:
            return

        rect_jogador = pygame.Rect(jogador.x, jogador.y, jogador.largura, jogador.altura)   #retangulo do jogador e do item
        rect_item = self.obter_rect()

        #chamar a  função colisao pra checar
        if checar_colisao_retangulos(rect_jogador, rect_item):
            self.coletado = True  #item some do mapa
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


#criar o inv
class Inventario:
    def __init__(self):
        self.armas_liberadas = {
            "Peixeira": False,
            "Revolver": False,
            "Espingarda": False
        }

        #lista dos slots do inv
        self.ordem_slots = ["Peixeira", "Revolver", "Espingarda"]

        #arma atual
        self.arma_ativa = None

        #load nos assets
        try:
            self.imagem_hud_fundo = pygame.image.load("assets/hud_inventario.png").convert_alpha()
            self.imagem_hud_fundo = pygame.transform.scale(self.imagem_hud_fundo, (300, 150))

        except pygame.error:
            self.imagem_hud_fundo = pygame.Surface((300, 150))

        #sprite da arma
        self.imagem_hud = {}

        for nome_arma in self.ordem_slots:
            caminho = f"assets/{nome_arma.lower()}.png"

            try:
                img = pygame.image.load(caminho).convert_alpha()
                self.imagem_hud[nome_arma] = pygame.transform.scale(img, (45, 45))

            except pygame.error:
                surf = pygame.Surface((40, 40))
                surf.fill((100, 100, 100))
                self.imagem_hud[nome_arma] = surf


    #metódo para adicionar a arma no inventário após a colisão
    def adicionar_arma(self, nome_arma):
        #conferir se  arma existe
        if nome_arma in self.armas_liberadas:
            #aciona a arma no inventario pra True
            self.armas_liberadas[nome_arma] = True

            #no caso da primeira arma (onde o player vai estar com armas em None)
            if self.arma_ativa is None:
                self.arma_ativa = nome_arma

            print(f"{nome_arma} FOI LIBERADA NO INVENTÁRIO!")

    #escolhas das armas
    def trocar_arma(self):
        teclas = pygame.key.get_pressed()

        #caso ele tecle 1, 2 OU 3 e já tenha coletado a arma em questão
        if teclas[pygame.K_1] and self.armas_liberadas["Peixeira"]:
            self.arma_ativa = "Peixeira"
            print("Lampião equipou a Peixeira!")

        elif teclas[pygame.K_2] and self.armas_liberadas["Revolver"]:
            self.arma_ativa = "Revolver"
            print("Lampião equipou o Revólvi!")

        elif teclas[pygame.K_3] and self.armas_liberadas["Espingarda"]:
            self.arma_ativa = "Espingarda"
            print("Lampião equipou a Espingarda! Cuida!!!")


    #hud do inv na tela
    def desenhar_hud(self, tela):
        #config do tamanho do HUD
        x_hud = 250
        y_hud = 450

        #desenhar assests de fundo (slots vazios)
        tela.blit(self.imagem_hud_fundo, (x_hud, y_hud))

        #alinhar as armas dentro dos slots
        largura_bloco = 72
        x_inicial = x_hud + 50
        y_arma = y_hud + 65

        #passar pelos 3 slots do hud pra desenhar um por um
        for i, nome_arma in enumerate(self.ordem_slots):
            x_arma = x_inicial + i * largura_bloco

            #se a arma do slot já foi coletada
            if self.armas_liberadas[nome_arma]:
                # desenha a imagem da arma  no slot
                tela.blit(self.imagem_hud[nome_arma], (x_arma, y_arma))

            #se a arma for a arma ativa (atual) = borda branca
            if self.arma_ativa == nome_arma:
                retangulo_selecionado = pygame.Rect(
                    x_arma - 1, y_arma - 1, 42, 42)
                pygame.draw.rect(tela, (255, 255, 255),
                                 retangulo_selecionado, 2)
