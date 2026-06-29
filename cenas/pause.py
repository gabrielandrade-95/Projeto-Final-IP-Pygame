import pygame
from button import button

class Pause():
    def __init__(self, tela, larguraTela, alturaTela):
        self.tela = tela

        # Imagens
        returnImg = pygame.image.load("returnNaoPressionado.png").convert_alpha()
        returnImgPressionado = pygame.image.load("returnPressionado.png").convert_alpha()
        menuImg = pygame.image.load("menuNaoPressionado.png").convert_alpha()
        menuImgPressionado = pygame.image.load("menuPressionado.png").convert_alpha()
        exitImg = pygame.image.load("exitNaoPressionado.png").convert_alpha()
        exitImgPressionado = pygame.image.load("exitPressionado.png").convert_alpha()
        self.background = pygame.image.load("fundoPause.png").convert()
        self.background = pygame.transform.scale(self.background, (larguraTela, alturaTela))

        # Redimensionar
        returnImg = pygame.transform.scale(returnImg, (200, 200))
        returnImgPressionado = pygame.transform.scale(returnImgPressionado, (200, 200))
        menuImg = pygame.transform.scale(menuImg, (200, 200))
        menuImgPressionado = pygame.transform.scale(menuImgPressionado, (200, 200))
        exitImg = pygame.transform.scale(exitImg, (80, 80))         
        exitImgPressionado = pygame.transform.scale(exitImgPressionado, (80, 80))  

        # Posicionamento 
        larguraBotao = returnImg.get_width()
        alturaBotao = returnImg.get_height()
        espacoEntreBotoes = 60
        totalLargura = larguraBotao * 2 + espacoEntreBotoes  

        xReturn = (larguraTela // 2) - totalLargura // 2
        xMenu = xReturn + larguraBotao + espacoEntreBotoes
        yBotoes = alturaTela - alturaBotao - 200

        # Instâncias
        self.returnBotao = button(xReturn, yBotoes, returnImg, returnImgPressionado)
        self.menuBotao = button(xMenu, yBotoes, menuImg, menuImgPressionado)
        self.exitBotao = button(10, 10, exitImg, exitImgPressionado)

    def update(self):
        self.tela.blit(self.background, (0, 0))

        clicouReturn = self.returnBotao.draw(self.tela)
        clicouMenu = self.menuBotao.draw(self.tela)
        clicouExit = self.exitBotao.draw(self.tela)

        if clicouExit:
            return "exit"
        if clicouReturn:
            return "jogo"  
        if clicouMenu:
            return "menu"

        return "pause"
    
    def entrar(self):
        self.returnBotao.reset()  # ou returnBotao no pause
        self.menuBotao.reset()
        self.exitBotao.reset()