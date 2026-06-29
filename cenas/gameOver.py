import pygame
from button import button

class GameOver():
    def __init__(self, tela, larguraTela, alturaTela):
        self.tela = tela

        # Imagens
        reiniciarImg = pygame.image.load("reiniciarNaoPressionado.png").convert_alpha()
        reiniciarImgPressionado = pygame.image.load("reiniciarPressionado.png").convert_alpha()
        menuImg = pygame.image.load("menuNaoPressionado.png").convert_alpha()
        menuImgPressionado = pygame.image.load("menuPressionado.png").convert_alpha()
        exitImg = pygame.image.load("exitNaoPressionado.png").convert_alpha()
        exitImgPressionado = pygame.image.load("exitPressionado.png").convert_alpha()
        self.background = pygame.image.load("fundoGameover.png").convert()
        self.background = pygame.transform.scale(self.background, (larguraTela, alturaTela))

        # Redimensionar
        reiniciarImg = pygame.transform.scale(reiniciarImg, (200, 200))
        reiniciarImgPressionado = pygame.transform.scale(reiniciarImgPressionado, (200, 200))
        menuImg = pygame.transform.scale(menuImg, (200, 200))
        menuImgPressionado = pygame.transform.scale(menuImgPressionado, (200, 200))
        exitImg = pygame.transform.scale(exitImg, (200, 200))
        exitImgPressionado = pygame.transform.scale(exitImgPressionado, (200, 200))

        # Posicionamento
        larguraBotao = reiniciarImg.get_width()
        alturaBotao = reiniciarImg.get_height()
        espacoEntreBotoes = 20
        totalLargura = larguraBotao * 3 + espacoEntreBotoes * 2

        xReiniciar = (larguraTela // 2) - totalLargura // 2
        xMenu = xReiniciar + larguraBotao + espacoEntreBotoes
        xExit = xMenu + larguraBotao + espacoEntreBotoes
        yBotoes = alturaTela - alturaBotao - 200

        # Instâncias
        self.reiniciarBotao = button(xReiniciar, yBotoes, reiniciarImg, reiniciarImgPressionado)
        self.menuBotao = button(xMenu, yBotoes, menuImg, menuImgPressionado)
        self.exitBotao = button(xExit, yBotoes, exitImg, exitImgPressionado)
    def update(self):
        self.tela.blit(self.background, (0, 0))

        clicouReiniciar = self.reiniciarBotao.draw(self.tela)
        clicouMenu = self.menuBotao.draw(self.tela)
        clicouExit = self.exitBotao.draw(self.tela)

        if clicouExit:
            return "exit"
        if clicouReiniciar:
            return "jogo"
        if clicouMenu:
            return "menu"

        return "gameOver"
    
    def entrar(self):
        self.reiniciarBotao.reset()  # ou returnBotao no pause
        self.menuBotao.reset()
        self.exitBotao.reset()