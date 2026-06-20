import pygame
import sys
from Mecanicas.mecanicaPlayer import Jogador 
from entidades.projetil import Projetil



class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("O Cangaço")
        self.rodando = True
        self.relogio = pygame.time.Clock()

        # Cria o jogador usando a classe que veio da Mecanicas
        self.player = Jogador(400, 300)
        self.grupo_projeteis = pygame.sprite.Group() #grupo para armazenar os projeteis serve para atualizar e desenhar todos os projeteis de uma vez

    def rodar(self):
        # loop 
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

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False

                if evento.key == pygame.K_SPACE:  
                    tempo_atual = pygame.time.get_ticks()
                    if tempo_atual - self.player.ultimo_tiro >= self.player.cooldown_tiro:
                        px = self.player.x
                        py = self.player.y
                        direcao = self.player.direcao_da_frente
                        novo_tiro = Projetil(px, py, direcao)
                        self.grupo_projeteis.add(novo_tiro)
                        self.player.ultimo_tiro = tempo_atual

    def update(self):
        # calculando o movimento do jogador
        self.player.mover()
        # atualizando os projeteis
        self.grupo_projeteis.update()

    def desenhar(self):
        self.tela.fill((40, 44, 52)) # cor de fundo
        
        self.player.desenhar(self.tela) # desenha o jogador
        
        # desenha os projeteis do grupo 
        self.grupo_projeteis.draw(self.tela) 

        pygame.display.flip()
        
    def atualizar(self):
        self.player.mover()
        self.grupo_projeteis.update()

