import pygame
import sys
import random
import math

from entidades.jogador import Jogador
from entidades.projetil import Projetil
from entidades.inimigos import Inimigo
from sistemas.coletaveis import Peixeira, Revolver, Espingarda, Inventario


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("O Cangaço")
        self.rodando = True
        self.relogio = pygame.time.Clock()

        caminho_fonte = "assets/Smokum.ttf"
        try:
            self.fonte = pygame.font.Font(caminho_fonte, 36)
            self.fonte_grande = pygame.font.Font(caminho_fonte, 72)
        except FileNotFoundError:
            self.fonte = pygame.font.SysFont("impact", 36)
            self.fonte_grande = pygame.font.SysFont("impact", 72)
        self.fonte_pequena = pygame.font.SysFont(None, 36)

        self.COR_TEXTO = (255, 255, 255)
        self.COR_SOMBRA = (0, 0, 0)

        self.player = Jogador(400, 300)
        self.grupo_projeteis = pygame.sprite.Group()
        self.grupo_inimigos = pygame.sprite.Group()
        self.grupo_coletaveis = pygame.sprite.Group()
        self.inventario = Inventario()

        self.kills = 0
        self.fase_completa1 = False
        self.fase_completa2 = False
        self.fase_completa3 = False

        self.peixeira_coletada = False
        self.revolver_coletado = False
        self.espingarda_coletada = False
        self.revolver_criado = False
        self.espingarda_criada = False

        # controle do arco da peixeira
        self.golpe_peixeira = None  # lista de pontos do polígono
        self.tempo_golpe = 0

        self.grupo_coletaveis.add(Peixeira(400, 250))


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
                self.inventario.trocar_arma()
                if evento.key == pygame.K_SPACE:
                    self._atirar()

    def _atirar(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.player.ultimo_tiro < self.player.cooldown_tiro:
            return

        arma_atual = self.inventario.arma_ativa
        if arma_atual is None:
            return

        px = self.player.x + 15
        py = self.player.y + 15
        direcao = self.player.direcao_da_frente

        if arma_atual == "Peixeira":
            self._atacar_peixeira(direcao)
        elif arma_atual == "Revolver":
            self.grupo_projeteis.add(Projetil(px, py, direcao))
        elif arma_atual == "Espingarda":
            tiros = self._calcular_tiros_espingarda(px, py, direcao, 10, 3)
            self.grupo_projeteis.add(*tiros)

        self.player.ultimo_tiro = tempo_atual

    def _calcular_tiros_espingarda(self, px, py, direcao, v_base, v_diag):
        if direcao == "direita":
            return [Projetil(px, py, direcao, v_base, 0), Projetil(px, py, direcao, v_base, -v_diag), Projetil(px, py, direcao, v_base, v_diag)]
        elif direcao == "esquerda":
            return [Projetil(px, py, direcao, -v_base, 0), Projetil(px, py, direcao, -v_base, -v_diag), Projetil(px, py, direcao, -v_base, v_diag)]
        elif direcao == "cima":
            return [Projetil(px, py, direcao, 0, -v_base), Projetil(px, py, direcao, -v_diag, -v_base), Projetil(px, py, direcao, v_diag, -v_base)]
        elif direcao == "baixo":
            return [Projetil(px, py, direcao, 0, v_base), Projetil(px, py, direcao, -v_diag, v_base), Projetil(px, py, direcao, v_diag, v_base)]
        return []

    def _atacar_peixeira(self, direcao):
        alcance = 55      # distancia do corte 
        angulo_arco = 120 # angulo do corte

        cx = self.player.x + self.player.largura // 2
        cy = self.player.y + self.player.altura // 2

        # angulo central de cada direção 
        angulo_central = {"direita": 0, "baixo": 90, "esquerda": 180, "cima": 270}.get(direcao, 0)
        metade = angulo_arco / 2  # 60 graus para cada lado

        # verifica inimigos dentro do corte
        for inimigo in list(self.grupo_inimigos):
            ex = inimigo.rect.centerx - cx
            ey = inimigo.rect.centery - cy
            distancia = (ex**2 + ey**2) ** 0.5

            if distancia <= alcance:
                angulo_inimigo = math.degrees(math.atan2(ey, ex)) % 360
                diff = (angulo_inimigo - angulo_central) % 360
                if diff > 180:
                    diff -= 360
                if abs(diff) <= metade:
                    inimigo.kill()
                    self.kills += 1

        # gera os pontos do polígono para o efeito visual do corte
        pontos = [(cx, cy)]
        num_segmentos = 16
        for i in range(num_segmentos + 1):
            angulo = math.radians(angulo_central - metade + (angulo_arco / num_segmentos) * i)
            pontos.append((cx + math.cos(angulo) * alcance, cy + math.sin(angulo) * alcance))

        self.golpe_peixeira = pontos
        self.tempo_golpe = pygame.time.get_ticks()

    def atualizar(self):
        if self.player.vida_jogador <= 0:
            self.rodando = False
            return

        self.player.mover()
        self.grupo_projeteis.update()

        for inimigo in self.grupo_inimigos:
            inimigo.update(self.player, self.grupo_inimigos)

        self._checar_colisoes()
        self.player.dano_jogador(self.grupo_inimigos)
        self._processar_coletaveis()
        self._checar_progressao_fases()
        self._spawnar_inimigos()

    def _checar_colisoes(self):
        for projetil in list(self.grupo_projeteis):
            for inimigo in list(self.grupo_inimigos):
                if inimigo.dano_inimigo(projetil):
                    self.kills += 1

    def _processar_coletaveis(self):
        for coletavel in self.grupo_coletaveis:
            coletavel.processar_coleta(self.player, self.inventario)
            if isinstance(coletavel, Peixeira) and coletavel.coletado:
                self.peixeira_coletada = True
            elif isinstance(coletavel, Revolver) and coletavel.coletado:
                self.revolver_coletado = True
            elif isinstance(coletavel, Espingarda) and coletavel.coletado:
                self.espingarda_coletada = True

        if self.fase_completa1 and not self.revolver_criado:
            self.grupo_coletaveis.add(Revolver(400, 250))
            self.revolver_criado = True

        if self.fase_completa2 and not self.espingarda_criada:
            self.grupo_coletaveis.add(Espingarda(400, 250))
            self.espingarda_criada = True

    def _checar_progressao_fases(self):
        if not self.fase_completa1 and self.kills >= 10:
            self.fase_completa1 = True
            self.grupo_inimigos.empty()
            self.kills = 0
        elif self.fase_completa1 and not self.fase_completa2 and self.kills >= 10:
            self.fase_completa2 = True
            self.grupo_inimigos.empty()
            self.kills = 0
        elif self.fase_completa2 and not self.fase_completa3 and self.kills >= 10:
            self.fase_completa3 = True
            self.grupo_inimigos.empty()
            self.kills = 0

    def _spawnar_inimigos(self):
        if len(self.grupo_inimigos) >= 5:
            return
        deve_spawnar = (
            (self.peixeira_coletada and not self.fase_completa1) or
            (self.revolver_coletado and not self.fase_completa2) or
            (self.espingarda_coletada and not self.fase_completa3)
        )
        if not deve_spawnar:
            return
        borda = random.choice(["topo", "baixo", "esquerda", "direita"])
        if borda == "esquerda":
            x, y = -20, random.randint(0, 580)
        elif borda == "direita":
            x, y = 820, random.randint(0, 580)
        elif borda == "topo":
            x, y = random.randint(0, 780), -20
        else:
            x, y = random.randint(0, 780), 620
        self.grupo_inimigos.add(Inimigo(x, y))


    def desenhar(self):
        cor_fundo = (100, 30, 27) if self.player.vida_jogador <= 3 else (242, 133, 0)
        self.tela.fill(cor_fundo)

        self.player.desenhar(self.tela)
        self.grupo_projeteis.draw(self.tela)
        self.grupo_inimigos.draw(self.tela)

        for coletavel in self.grupo_coletaveis:
            coletavel.desenhar(self.tela)

        self._desenhar_hud()
        self._desenhar_mensagens()

        # corte da peixeira (efeito visual)
        if self.golpe_peixeira and pygame.time.get_ticks() - self.tempo_golpe < 150:
            surf_arco = pygame.Surface((800, 600), pygame.SRCALPHA)
            pygame.draw.polygon(surf_arco, (255, 255, 255, 80), self.golpe_peixeira)
            self.tela.blit(surf_arco, (0, 0))

        self.inventario.desenhar_hud(self.tela)
        pygame.display.flip()

    def _desenhar_texto_com_sombra(self, fonte, texto, cor, pos):
        sombra = fonte.render(texto, True, self.COR_SOMBRA)
        surf = fonte.render(texto, True, cor)
        self.tela.blit(sombra, (pos[0] + 2, pos[1] + 2))
        self.tela.blit(surf, pos)

    def _desenhar_hud(self):
        self._desenhar_texto_com_sombra(self.fonte, f"Kills: {self.kills}/10", self.COR_TEXTO, (10, 10))
        self._desenhar_texto_com_sombra(self.fonte, f"Vida: {int(self.player.vida_jogador)}", self.COR_TEXTO, (10, 50))

    def _desenhar_mensagens(self):
        if not self.peixeira_coletada:
            self._desenhar_texto_com_sombra(self.fonte, "Colete a Peixeira para começar!", (255, 255, 0), (150, 150))
        elif self.fase_completa1 and not self.revolver_coletado:
            mensagem = "Você venceu a primeira fase! Colete a arma!"
            surf = self.fonte_pequena.render(mensagem, True, (0, 255, 0))
            x = (800 - surf.get_width()) // 2
            self._desenhar_texto_com_sombra(self.fonte_pequena, mensagem, (0, 255, 0), (x, 150))
        elif self.fase_completa2 and not self.espingarda_coletada:
            mensagem = "Segunda fase vencida! Colete a Espingarda para o inimigo final!"
            surf = self.fonte_pequena.render(mensagem, True, (0, 255, 0))
            x = (800 - surf.get_width()) // 2
            self._desenhar_texto_com_sombra(self.fonte_pequena, mensagem, (0, 255, 0), (x, 150))
        elif self.fase_completa3:
            self._desenhar_texto_com_sombra(self.fonte_grande, "Você venceu!", (255, 215, 0), (200, 250))
        if self.player.vida_jogador <= 0:
            self._desenhar_texto_com_sombra(self.fonte_grande, "Game Over", (255, 0, 0), (200, 250))