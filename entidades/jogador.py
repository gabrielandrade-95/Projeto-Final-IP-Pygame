import pygame


class Jogador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 30
        self.altura = 30
        self.velocidade = 5
        self.cor = (0, 200, 100)
        self.direcao_da_frente = "direita"
        self.cooldown_tiro = 300   # milissegundos entre tiros
        self.ultimo_tiro = 0
        self.vida_jogador = 1000

        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)

    def mover(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            if self.x > 0:
                self.x -= self.velocidade
                self.direcao_da_frente = "esquerda"

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            if self.x < 770:
                self.x += self.velocidade
                self.direcao_da_frente = "direita"

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            if self.y > 0:
                self.y -= self.velocidade
                self.direcao_da_frente = "cima"

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            if self.y < 570:
                self.y += self.velocidade
                self.direcao_da_frente = "baixo"

        # sincroniza o rect após o movimento
        self.rect.x = self.x
        self.rect.y = self.y

    def dano_jogador(self, grupo_inimigos):
        tempo_atual = pygame.time.get_ticks()

        for inimigo in grupo_inimigos:
            if self.rect.colliderect(inimigo.rect):
                if tempo_atual - inimigo.ultimo_dano >= inimigo.cooldown_dano:
                    self.vida_jogador -= 0.35
                    inimigo.ultimo_dano = tempo_atual
                    return True
        return False

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)