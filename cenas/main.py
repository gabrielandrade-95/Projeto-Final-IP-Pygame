import pygame
from menu import Menu
from gameOver import GameOver
from pause import Pause

pygame.init()

alturaTela = 500
larguraTela = 800

tela = pygame.display.set_mode((larguraTela, alturaTela))
pygame.display.set_caption("jogo")

menu = Menu(tela, larguraTela, alturaTela)
gameOver = GameOver(tela, larguraTela, alturaTela)
pause = Pause(tela, larguraTela, alturaTela)

telaAtual = "pause"
telaAnterior = ""

run = True

while run:

    if telaAtual == "menu":
        telaAtual = menu.update()

    elif telaAtual == "jogo":
        pass  # seu amigo preenche aqui

    elif telaAtual == "pause":
        telaAtual = pause.update()

    elif telaAtual == "gameOver":
        telaAtual = gameOver.update()

    elif telaAtual == "exit":
        run = False

    # Resetar botões ao entrar em uma tela nova
    if telaAtual != telaAnterior:
        if telaAtual == "menu":
            menu.entrar()
        elif telaAtual == "pause":
            pause.entrar()
        elif telaAtual == "gameOver":
            gameOver.entrar()

    telaAnterior = telaAtual

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()