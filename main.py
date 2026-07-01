import pygame
from menu import Menu
from gameOver import GameOver
from pause import Pause
from sistemas.jogo import Jogo

pygame.init()

alturaTela = 600
larguraTela = 800

tela = pygame.display.set_mode((larguraTela, alturaTela))
pygame.display.set_caption("O Cangaço")

menu = Menu(tela, larguraTela, alturaTela)
gameOver = GameOver(tela, larguraTela, alturaTela)
pause = Pause(tela, larguraTela, alturaTela)
jogo = Jogo(tela)

telaAtual = "menu"
telaAnterior = ""
relogio = pygame.time.Clock()

run = True

while run:
    eventos = pygame.event.get()

    for event in eventos:
        if event.type == pygame.QUIT:
            run = False

    if telaAtual == "menu":
        telaAtual = menu.update()

    elif telaAtual == "jogo":
        telaAtual = jogo.atualizar_frame(eventos)

    elif telaAtual == "pause":
        telaAtual = pause.update()

    elif telaAtual == "gameOver":
        telaAtual = gameOver.update()

    elif telaAtual == "exit":
        run = False

    # Ao trocar de tela
    if telaAtual != telaAnterior:
        if telaAtual == "menu":
            menu.entrar()
        elif telaAtual == "pause":
            pause.entrar()
        elif telaAtual == "gameOver":
            gameOver.entrar()
        elif telaAtual == "jogo" and telaAnterior in ("menu", "gameOver"):
            # jogo novo: recria o estado do zero (menu = novo jogo, gameOver = reiniciar)
            jogo = Jogo(tela)
        # se vier do "pause", NÃO recria -> o jogo continua de onde parou

    telaAnterior = telaAtual

    relogio.tick(60)
    pygame.display.update()

pygame.quit()