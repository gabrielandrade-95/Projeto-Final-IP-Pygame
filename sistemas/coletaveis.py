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
            self.imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
            self.imagem = pygame.transform.scale(self.imagem_original, (40, 40))
        except (pygame.error, FileNotFoundError):
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
        super().__init__(x, y, "Peixeira", "assets/sprites_objetos/peixeira.png")


class Revolver(ColetavelBase):
    def __init__(self, x, y):
        super().__init__(x, y, "Revolver", "assets/sprites_objetos/revolver.png")


class Espingarda(ColetavelBase):
    def __init__(self, x, y):
        super().__init__(x, y, "Espingarda", "assets/sprites_objetos/espingarda.png")


class Pitu(ColetavelBase):
    def __init__(self, x, y):
        super().__init__(x, y, "Pitu", "assets/Pitu.png")


class Inventario:
    ARMAS = ["Peixeira", "Revolver", "Espingarda"]
    
    def __init__(self):
        self.armas_liberadas = {arma: False for arma in self.ARMAS}
        self.arma_ativa = None
        
        try:
            hud = pygame.image.load("assets/huds/hud_inventario.png").convert_alpha()
            self.imagem_hud_fundo = pygame.transform.scale(hud, (300, 150))
        except (pygame.error, FileNotFoundError):
            self.imagem_hud_fundo = pygame.Surface((300, 150))
        
        self.imagem_hud = {}
        for nome in self.ARMAS:
            try:
                img = pygame.image.load(f"assets/sprites_objetos/{nome.lower()}.png").convert_alpha()
                self.imagem_hud[nome] = pygame.transform.scale(img, (45, 45))
            except (pygame.error, FileNotFoundError):
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
        x_hud, y_hud = 10, 517
        hud_reduzido = pygame.transform.scale(self.imagem_hud_fundo, (220, 110))
        tela.blit(hud_reduzido, (x_hud, y_hud))
        
        x_inicial = x_hud + 37
        y_arma = y_hud + 48
        largura_bloco = 53
        
        for i, nome in enumerate(self.ARMAS):
            x_arma = x_inicial + i * largura_bloco
            if self.armas_liberadas[nome]:
                arma_reduzida = pygame.transform.scale(self.imagem_hud[nome], (33, 33))
                tela.blit(arma_reduzida, (x_arma, y_arma))
            if self.arma_ativa == nome:
                borda = pygame.Rect(x_arma - 1, y_arma - 1, 33, 33)
                pygame.draw.rect(tela, (255, 255, 255), borda, 2)