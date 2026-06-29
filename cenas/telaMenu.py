import pygame

pygame.init()

alturaTela = 500
larguraTela = 800

tela = pygame.display.set_mode((larguraTela, alturaTela))
pygame.display.set_caption("botão")

#imagens 

startImg = pygame.image.load("botaoNaoPressionado.png").convert_alpha()
startImgPressionado = pygame.image.load("botaoPressionado.png").convert_alpha()

exitImg = pygame.image.load("exitNaoPressionado.png").convert_alpha()
exitImgPressionado = pygame.image.load("exitPressionado.png").convert_alpha()

creditosImg = pygame.image.load("creditosNaoPressionado.png").convert_alpha()
creditosImgPressionado = pygame.image.load("creditosPressionado.png").convert_alpha()

background = pygame.image.load("Fundo.png").convert()
background = pygame.transform.scale(background, (larguraTela, alturaTela)) 

#redimensionar imagens
startImg = pygame.transform.scale(startImg, (200, 200))
startImgPressionado = pygame.transform.scale(startImgPressionado, (200, 200))
exitImg = pygame.transform.scale(exitImg, (200, 200))
exitImgPressionado = pygame.transform.scale(exitImgPressionado, (200, 200))
creditosImg = pygame.transform.scale(creditosImg, (80, 80))  
creditosImgPressionado = pygame.transform.scale(creditosImgPressionado, (80, 80))

#classe de botão

class button():
    def __init__(self, x, y, image, imagePressionado):
        self.image = image
        self.imagePressionado = imagePressionado
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.pressionado = False
        self.tempoPressionado = 0

    def draw(self):
        imagemAtual = self.image
        clicado = False #armazenar se botão foi clicado

        # Verificar clique
        clique = pygame.mouse.get_pressed()[0]
        mousePos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mousePos) and clique:
            self.pressionado = True
            self.tempoPressionado = pygame.time.get_ticks()

        # Trocar sprite enquanto estiver dentro do tempo
        if self.pressionado:
            if pygame.time.get_ticks() - self.tempoPressionado < 150:
                imagemAtual = self.imagePressionado
            else:
                self.pressionado = False  # reseta depois dos 150ms
                clicado = True
        tela.blit(imagemAtual, (self.rect.x, self.rect.y))
        return clicado
        

#local e tamanho do botão

larguraBotao = startImg.get_width()
alturaBotao = startImg.get_height()

espacoEntreBotoes = 20
totalLargura = larguraBotao * 2 + espacoEntreBotoes  


xPlay = (larguraTela // 2) - totalLargura // 2
xExit = xPlay + larguraBotao + espacoEntreBotoes
yBotoes = alturaTela - alturaBotao + 10


#criar instancia de botão
playBotao = button(xPlay, yBotoes, startImg, startImgPressionado)
exitBotao = button(xExit, yBotoes, exitImg, exitImgPressionado)
credBotao = button(10, 10, creditosImg, creditosImgPressionado)


run = True

telaAtual = "menu"

while run:
    tela.blit(background, (0, 0))

    if telaAtual == "menu":
        clicouPlay = playBotao.draw()
        clicouCred = credBotao.draw()
        clicouExit = exitBotao.draw()

        if clicouExit:
            run = False

        if clicouPlay:
            telaAtual = "jogo"

        if clicouCred:
            telaAtual = "creditos"

    elif telaAtual == "jogo":
        tela.fill((0, 0, 0))
    
    elif telaAtual == "creditos":
        tela.fill((0, 0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()




