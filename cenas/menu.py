import pygame
from button import button

class Menu():
    def __init__(self, tela, larguraTela, alturaTela):
        self.tela = tela

        #imagens 

        startImg = pygame.image.load("botaoNaoPressionado.png").convert_alpha()
        startImgPressionado = pygame.image.load("botaoPressionado.png").convert_alpha()

        exitImg = pygame.image.load("exitNaoPressionado.png").convert_alpha()
        exitImgPressionado = pygame.image.load("exitPressionado.png").convert_alpha()

        creditosImg = pygame.image.load("creditosNaoPressionado.png").convert_alpha()
        creditosImgPressionado = pygame.image.load("creditosPressionado.png").convert_alpha()

        self.background = pygame.image.load("Fundo.png").convert()
        self.background = pygame.transform.scale(self.background, (larguraTela, alturaTela)) 

        #redimensionar imagens
        startImg = pygame.transform.scale(startImg, (200, 200))
        startImgPressionado = pygame.transform.scale(startImgPressionado, (200, 200))
        exitImg = pygame.transform.scale(exitImg, (200, 200))
        exitImgPressionado = pygame.transform.scale(exitImgPressionado, (200, 200))
        creditosImg = pygame.transform.scale(creditosImg, (80, 80))  
        creditosImgPressionado = pygame.transform.scale(creditosImgPressionado, (80, 80))
        larguraBotao = startImg.get_width()
        alturaBotao = startImg.get_height()

        espacoEntreBotoes = 20
        totalLargura = larguraBotao * 2 + espacoEntreBotoes  


        xPlay = (larguraTela // 2) - totalLargura // 2
        xExit = xPlay + larguraBotao + espacoEntreBotoes
        yBotoes = alturaTela - alturaBotao + 10


        #criar instancia de botão
        self.playBotao = button(xPlay, yBotoes, startImg, startImgPressionado)
        self.exitBotao = button(xExit, yBotoes, exitImg, exitImgPressionado)
        self.credBotao = button(10, 10, creditosImg, creditosImgPressionado)

    def update(self):
        self.tela.blit(self.background, (0, 0))

        clicouPlay = self.playBotao.draw(self.tela)
        clicouCred = self.credBotao.draw(self.tela)
        clicouExit = self.exitBotao.draw(self.tela)

        if clicouExit:
            return "exit"
        if clicouPlay:
            return "jogo"
        if clicouCred:
            return "creditos"

        return "menu"
    
    def entrar(self):
        self.playBotao.reset()
        self.exitBotao.reset()
        self.credBotao.reset()