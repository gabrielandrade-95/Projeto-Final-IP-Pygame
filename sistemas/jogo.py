import pygame
import sys
import random
from Mecanicas.mecanicaPlayer import Jogador
from entidades.projetil import Projetil
from entidades.novo_inimigo import Inimigo
from sistemas.coletaveis import Peixeira, Revolver, Espingarda, Inventario


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("O Cangaço")
        self.rodando = True
        self.relogio = pygame.time.Clock()

        # cria o player
        self.player = Jogador(400, 300)

        # sprite
        self.grupo_projeteis = pygame.sprite.Group()
        self.grupo_inimigos = pygame.sprite.Group()
        self.grupo_coletaveis = pygame.sprite.Group()

        # inv
        self.inventario = Inventario()

        # contadores
        self.kills = 0
        self.fase_completa = False

        self.peixeira_coletada = False

        # cria a peixeira no chão
        peixeira = Peixeira(400, 250)
        self.grupo_coletaveis.add(peixeira)

        caminho_fonte = "assets/Smokum.ttf"

        try:
            self.fonte = pygame.font.Font(caminho_fonte, 36)
            self.fonte_grande = pygame.font.Font(caminho_fonte, 72)
        except FileNotFoundError:

            # por a fonte
            self.fonte = pygame.font.SysFont("impact", 36)
            self.fonte_grande = pygame.font.SysFont("impact", 72)

        # cor dos texto
        self.COR_TEXTO = (255, 255, 255)  # branco
        self.COR_SOMBRA = (0, 0, 0)  # preto para sombra

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

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False

                # troca de arma se tiver arma
                self.inventario.trocar_arma()

                if evento.key == pygame.K_SPACE:
                    tempo_atual = pygame.time.get_ticks()
                    if tempo_atual - self.player.ultimo_tiro >= self.player.cooldown_tiro:
                        if self.inventario.arma_ativa is not None:
                            px = self.player.x
                            py = self.player.y
                            direcao = self.player.direcao_da_frente
                            novo_tiro = Projetil(px + 15, py + 15, direcao)
                            self.grupo_projeteis.add(novo_tiro)
                            self.player.ultimo_tiro = tempo_atual

    def onda_inimigos(self, grupo_inimigos, jogador):
        # spawnar os bixo
        if len(grupo_inimigos) < 5:
            x = 0
            y = 0
            borda = random.choice(["topo", "baixo", "esquerda", "direita"])
            if borda == "esquerda":
                x, y = -20, random.randint(0, 580)
            elif borda == "direita":
                x, y = 820, random.randint(0, 580)
            elif borda == "topo":
                x, y = random.randint(0, 780), -20
            else:
                x, y = random.randint(0, 780), 620

            novo_inimigo = Inimigo(x, y)
            grupo_inimigos.add(novo_inimigo)

    def checar_colisoes(self):
        # ve se a bala pegou no inimigo
        for projetil in self.grupo_projeteis:
            for inimigo in self.grupo_inimigos:
                if inimigo.dano_inimigo(projetil):
                    self.kills += 1

    def checar_vida(self):
        # ver se morreu
        if self.player.vida_jogador <= 0:
            return True
        return False

    def atualizar(self):
        # se morrer para tudo
        if self.player.vida_jogador <= 0:
            self.rodando = False
            return

        # movimento
        self.player.mover()
        self.grupo_projeteis.update()

        # colisoes
        self.checar_colisoes()
        self.player.dano_jogador(self.grupo_inimigos)

        # atualizar inimigos
        for inimigo in self.grupo_inimigos:
            inimigo.update(self.player, self.grupo_inimigos)

        # processar a coleta de itens
        for coletavel in self.grupo_coletaveis:
            coletavel.processar_coleta(self.player, self.inventario)

            # se coletou a peixeira ativa os inimigos
            if isinstance(coletavel, Peixeira) and coletavel.coletado:
                self.peixeira_coletada = True

        if self.kills >= 10:
            self.fase_completa = True
            self.grupo_inimigos.empty()

        # so aparece os inimigos se tiver coletado a peixeira E não estiver na fase completa
        if self.peixeira_coletada and not self.fase_completa:
            self.onda_inimigos(self.grupo_inimigos, self.player)

    def desenhar(self):
        # fundo do jogo
        if self.player.vida_jogador <= 3:
            self.tela.fill((100, 30, 27))  # vermelho quando ta baixa
        else:
            self.tela.fill((242, 133, 0))  # laranja com a vida cheia

        # desenhar o jogador
        self.player.desenhar(self.tela)

        # desenhar os tiros
        self.grupo_projeteis.draw(self.tela)

        # desenhar os inimigos
        self.grupo_inimigos.draw(self.tela)

        # desenhar o coletavel da faca
        for coletavel in self.grupo_coletaveis:
            coletavel.desenhar(self.tela)

        # mostrar a hud
        kills_surf = self.fonte.render(
            f"Kills: {self.kills}/10", True, self.COR_TEXTO)  # kills
        kills_sombra = self.fonte.render(
            f"Kills: {self.kills}/10", True, self.COR_SOMBRA)

        self.tela.blit(kills_sombra, (12, 12))
        self.tela.blit(kills_surf, (10, 10))

        vida_surf = self.fonte.render(
            # vida
            f"Vida: {int(self.player.vida_jogador)}", True, self.COR_TEXTO)
        vida_sombra = self.fonte.render(
            f"Vida: {int(self.player.vida_jogador)}", True, self.COR_SOMBRA)

        self.tela.blit(vida_sombra, (12, 52))
        self.tela.blit(vida_surf, (10, 50))

        if not self.peixeira_coletada:  # msg antes de pegara pexeira
            msg_surf = self.fonte.render(
                f"Colete a Peixeira para começar!", True, (255, 255, 0))
            msg_sombra = self.fonte.render(
                f"Colete a Peixeira para começar!", True, self.COR_SOMBRA)
            self.tela.blit(msg_sombra, (152, 22))
            self.tela.blit(msg_surf, (150, 20))

        if self.fase_completa:  # fase completa
            fase_texto_surf = self.fonte.render(
                f"Você venceu! Colete a arma!", True, (0, 255, 0))
            fase_texto_sombra = self.fonte.render(
                "Você venceu! Colete a arma!", True, self.COR_SOMBRA)

            self.tela.blit(fase_texto_sombra, (202, 52))
            self.tela.blit(fase_texto_surf, (200, 50))

        if self.player.vida_jogador <= 0:  # derrota
            texto_fim = self.fonte_grande.render(
                "Game Over", True, (255, 0, 0))
            fim_sombra = self.fonte_grande.render(
                "Game Over", True, self.COR_SOMBRA)

            # bagulho de sombra do game over
            self.tela.blit(fim_sombra, (203, 253))
            self.tela.blit(texto_fim, (200, 250))

        # desenha o inventário (HUD das armas)
        self.inventario.desenhar_hud(self.tela)

        pygame.display.flip()
