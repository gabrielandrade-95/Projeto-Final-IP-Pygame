import pygame
import sys


class Jogador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 30
        self.altura = 30
        self.velocidade = 5
        self.cor = (0, 200, 100)

    def mover(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.velocidade

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.velocidade

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.y -= self.velocidade

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.y += self.velocidade

    def desenhar(self, tela):
        retangulo = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(tela, self.cor, retangulo)


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Movimentacao")
        self.rodando = True

        self.relogio = pygame.time.Clock()

        self.player = Jogador(400, 300)

    def rodar(self):
        while self.rodando:

            self.checar_eventos()
            self.atualizar()
            self.desenhar()

            self.relogio.tick(60)

        pygame.quit()
        sys.exit()

    def checar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

    def atualizar(self):
        self.player.mover()

    def desenhar(self):
        self.tela.fill((40, 44, 52))
        self.player.desenhar(self.tela)

        pygame.display.flip()


if __name__ == "__main__":
    meu_jogo = Jogo()
    meu_jogo.rodar()
