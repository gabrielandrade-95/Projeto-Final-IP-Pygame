#jogo.py
import pygame
import sys
import random
import math

from entidades.jogador import Jogador
from entidades.projetil import Projetil
from entidades.inimigos import Inimigo, InimigoRapido, Boss
from sistemas.coletaveis import Peixeira, Revolver, Espingarda, Inventario, Pitu


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((1024, 637))
        pygame.display.set_caption("O Cangaço")
        self.rodando = True
        self.relogio = pygame.time.Clock()

        # cria o player
        self.player = Jogador(512, 430)

        # sprite
        self.grupo_projeteis = pygame.sprite.Group()
        self.grupo_inimigos = pygame.sprite.Group()
        self.grupo_coletaveis = pygame.sprite.Group()

        # inv
        self.inventario = Inventario()

        # contadores
        self.kills = 0
        self.fase_completa1 = False
        self.fase_completa2 = False
        self.fase_completa3 = False
        self.inicio_fase_3 = False  # sinaliza quando o boss deve ser criado

        self.peixeira_coletada = False
        self.revolver_coletado = False
        self.espingarda_coletada = False
        self.revolver_criado = False
        self.espingarda_criada = False
        self.pitu_coletada = False
        self.pitu_fase1 = False
        self.pitu_fase2 = False

        # controle do arco da peixeira
        self.golpe_peixeira = None
        self.tempo_golpe = 0
        self.pausado = False
        self.game_over = False

        # cria a peixeira no chão
        self.grupo_coletaveis.add(Peixeira(512, 318))

        caminho_fonte = "assets/Smokum.ttf"
        try:
            self.fonte = pygame.font.Font(caminho_fonte, 36)
            self.fonte_grande = pygame.font.Font(caminho_fonte, 72)
        except FileNotFoundError:
            # por a fonte
            self.fonte = pygame.font.SysFont("impact", 36)
            self.fonte_grande = pygame.font.SysFont("impact", 72)
        self.fonte_pequena = pygame.font.SysFont(None, 36)

        # cor dos textos
        self.COR_TEXTO = (255, 255, 255)  # branco
        self.COR_SOMBRA = (0, 0, 0)       # preto para sombra
        
        self.imagem_fundo = pygame.image.load("assets/telas/fundo.png").convert()
        #dimensiona a imagem para o tamanho da tela
        self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, (1024, 637))

    def rodar(self):
        while self.rodando:
            self.checar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(60)

    def checar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.pausado = True
                    self.rodando = False

                # troca de arma se tiver arma
                self.inventario.trocar_arma()
                if self.inventario.arma_ativa is None :
                    self.player.atualizar_arma("desarmado")
                else :
                    self.player.atualizar_arma(self.inventario.arma_ativa)

                if evento.key == pygame.K_SPACE:
                    self.atirar()

    def atirar(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.player.ultimo_tiro < self.player.cooldown_tiro:
            return

        arma_atual = self.inventario.arma_ativa
        if arma_atual is None:
            return

        px = self.player.x + 15
        py = self.player.y + 15
        direcao = self.player.direcao_da_frente
        
        # comportamento da peixeira (corpo a corpo)
        if arma_atual == "Peixeira":
            self.atacar_peixeira(direcao)

        # comportamento da pistola
        elif arma_atual == "Revolver":
            self.grupo_projeteis.add(Projetil(px, py, direcao))

        # comportamento da espingarda/doze/shotgun
        elif arma_atual == "Espingarda":
            v_base = 10  # velocidade principal
            v_diag = 3   # desvio da diagonal
            tiros = self.calcular_tiros_espingarda(px, py, direcao, v_base, v_diag)
            # adiciona os 3 tiros ao grupo
            self.grupo_projeteis.add(*tiros)

        self.player.ultimo_tiro = tempo_atual

    def onda_inimigos(self, grupo_inimigos, jogador, inimigo=None):
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

            if not self.fase_completa1:
                novo_inimigo = Inimigo(x, y)
            
            elif self.fase_completa1 and not self.fase_completa2:
                novo_inimigo = InimigoRapido(x, y)
            
            elif inimigo == "boss":
                novo_inimigo = Boss(x, y)
                
            grupo_inimigos.add(novo_inimigo)

    def calcular_tiros_espingarda(self, px, py, direcao, v_base, v_diag):
        if direcao == "direita":
            return [
                Projetil(px, py, direcao, v_base, 0),        # reto
                Projetil(px, py, direcao, v_base, -v_diag),  # diagonal cima
                Projetil(px, py, direcao, v_base,  v_diag),  # diagonal baixo
            ]
        elif direcao == "esquerda":
            return [
                Projetil(px, py, direcao, -v_base, 0),
                Projetil(px, py, direcao, -v_base, -v_diag),
                Projetil(px, py, direcao, -v_base,  v_diag),
            ]
        elif direcao == "cima":
            return [
                Projetil(px, py, direcao, 0,       -v_base),
                Projetil(px, py, direcao, -v_diag, -v_base),  # diagonal esquerda
                Projetil(px, py, direcao,  v_diag, -v_base),  # diagonal direita
            ]
        elif direcao == "baixo":
            return [
                Projetil(px, py, direcao, 0,       v_base),
                Projetil(px, py, direcao, -v_diag, v_base),
                Projetil(px, py, direcao,  v_diag, v_base),
            ]
        return []

    def atacar_peixeira(self, direcao):
        alcance = 80      # distância do corte em pixels
        angulo_arco = 120 # graus totais do arco

        cx = self.player.x + self.player.largura // 2
        cy = self.player.y + self.player.altura // 2

        # ângulo central de cada direção
        angulo_central = {"direita": 0, "baixo": 90, "esquerda": 180, "cima": 270}.get(direcao, 0)
        metade = angulo_arco / 2  # 60 graus para cada lado

        # ve se a peixeira pegou no inimigo
        dano_peixeira = 1  # 1 de dano por golpe (inimigo tem 2 de vida = 2 hits)
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
                    # Aplica o dano no inimigo e computa a kill se ele morrer
                    if inimigo.receber_dano(dano_peixeira):
                        self.kills += 1

        # gera os pontos do polígono para o efeito visual do arco
        pontos = [(cx, cy)]
        num_segmentos = 16
        for i in range(num_segmentos + 1):
            angulo = math.radians(angulo_central - metade + (angulo_arco / num_segmentos) * i)
            pontos.append((cx + math.cos(angulo) * alcance, cy + math.sin(angulo) * alcance))

        self.golpe_peixeira = pontos
        self.tempo_golpe = pygame.time.get_ticks()

    def checar_vida(self):
        # ver se morreu
        if self.player.vida_jogador <= 0:
            return True
        return False
    
    def criar_revolver(self):
        # Corrigido: adicionado 'and not self.revolver_criado' para evitar travamento por spawn infinito
        if (self.fase_completa1) and (not self.fase_completa2) and (not self.revolver_coletado) and (not self.revolver_criado):
            revolver = Revolver(400, 250)
            self.grupo_coletaveis.add(revolver)
            self.revolver_criado = True
        
    def criar_espingarda(self):
        # Corrigido: adicionado 'and not self.espingarda_criada' para evitar travamento por spawn infinito
        if (self.fase_completa2) and (not self.fase_completa3) and (not self.espingarda_coletada) and (not self.espingarda_criada):
            espingarda = Espingarda(400, 250)
            self.grupo_coletaveis.add(espingarda)
            self.espingarda_criada = True
            
    def criar_pitu(self):
        # Corrigido: adicionado 'and not self.pitu_fase1' para evitar spawn infinito da garrafa
        if (self.fase_completa1) and (not self.fase_completa2) and (not self.pitu_coletada) and (not self.pitu_fase1):
            pitu = Pitu(350, 125)
            self.grupo_coletaveis.add(pitu)
            self.pitu_fase1 = True
            
        # Corrigido: adicionado 'and not self.pitu_fase2' para evitar spawn infinito da garrafa
        if (self.fase_completa2) and (not self.fase_completa3) and (not self.pitu_coletada) and (not self.pitu_fase2):
            pitu = Pitu(350, 125)
            self.grupo_coletaveis.add(pitu)
            self.pitu_fase2 = True

    def criar_boss(self):
        self.onda_inimigos(self.grupo_inimigos, self.player, inimigo="boss")
    
    def barrinha_vida_player(self):
        largura = 300
        altura = 20
        
        # Corrigido de 1000 para 10 para preencher de forma correta e proporcional à vida real do player
        preenchimento = (self.player.vida_jogador / 10) * largura
        preenchimento = min(preenchimento, largura)
        
        pygame.draw.rect(self.tela, (100, 0, 0), (10, 10, largura, altura))          # fundo vermelho escuro
        pygame.draw.rect(self.tela, (0, 255, 0), (10, 10, preenchimento, altura))    # vida atual verde
        pygame.draw.rect(self.tela, (255, 255, 255), (10, 10, largura, altura), 2)   # borda branca
        
    def barrinha_vida_boss(self):
        for inimigo in self.grupo_inimigos:
            if isinstance(inimigo, Boss):
                boss = inimigo
                
                largura = 150
                altura = 15
                x = boss.rect.centerx - (largura // 2)
                y = boss.rect.y - 30
                
                # Verifique se o boss tem o atributo 'vida', ajustado para valor máximo (30)
                if hasattr(boss, 'vida'):
                    preenchimento = (boss.vida / 30) * largura
                    preenchimento = min(preenchimento, largura)
                    
                    pygame.draw.rect(self.tela, (100, 0, 0), (x, y, largura, altura))         # fundo vermelho escuro
                    pygame.draw.rect(self.tela, (255, 0, 0), (x, y, preenchimento, altura))   # vida atual vermelha
                    pygame.draw.rect(self.tela, (255, 255, 255), (x, y, largura, altura), 2)  # borda branca

    def atualizar(self):
        # se morrer para tudo
        if self.player.vida_jogador <= 0:
            self.game_over = True
            self.rodando = False
            return

        # movimento
        self.player.mover(self.grupo_inimigos)
        self.grupo_projeteis.update()

        # atualizar inimigos
        for inimigo in self.grupo_inimigos:
            inimigo.update(self.player, self.grupo_inimigos)

        # colisoes
        self.checar_colisoes()
        self.player.dano_jogador(self.grupo_inimigos)

        self.processar_coletaveis()
        self.checar_progressao_fases()
        self.spawnar_inimigos()

        # spawna o boss uma única vez após coletar a espingarda
        if self.espingarda_coletada and not self.fase_completa3 and self.inicio_fase_3:
            self.criar_boss()
            self.inicio_fase_3 = False

    def checar_colisoes(self):
        # ve se a bala pegou no inimigo
        for projetil in list(self.grupo_projeteis):
            for inimigo in list(self.grupo_inimigos):
                if inimigo.dano_inimigo(projetil):
                    self.kills += 1

    def processar_coletaveis(self):
        # processar a coleta de itens
        for coletavel in list(self.grupo_coletaveis):
            coletavel.processar_coleta(self.player, self.inventario)

            if coletavel.coletado:
                # se coletou a peixeira ativa os inimigos
                if isinstance(coletavel, Peixeira) and coletavel.coletado:
                    self.peixeira_coletada = True
                    
                elif isinstance(coletavel, Revolver) and coletavel.coletado:
                    self.revolver_coletado = True
                    
                elif isinstance(coletavel, Espingarda) and coletavel.coletado:
                    self.espingarda_coletada = True
                    
                elif isinstance(coletavel, Pitu) and coletavel.coletado:
                    self.player.vida_jogador += (self.player.vida_jogador) * 0.5
                    self.player.vida_jogador = min(self.player.vida_jogador, 10) # limita a vida do jogador a 10
                    self.pitu_coletada = True
                
                coletavel.kill()  # remove o coletável do grupo após a coleta para deixar o jogo mais limpo

    def checar_progressao_fases(self):
        # verificando se a fase foi completada
        if not self.fase_completa1 and self.kills >= 10:
            self.fase_completa1 = True
            self.grupo_inimigos.empty()
            self.kills = 0
        elif self.fase_completa1 and not self.fase_completa2 and self.kills >= 10:
            self.fase_completa2 = True
            self.inicio_fase_3 = True  # sinaliza para criar o boss na próxima fase
            self.pitu_coletada = False
            self.grupo_inimigos.empty()
            self.kills = 0
        elif self.fase_completa2 and not self.fase_completa3 and self.kills >= 1:  # basta matar o boss
            self.fase_completa3 = True
            self.grupo_inimigos.empty()
            self.kills = 0

    def spawnar_inimigos(self):
        # spawnar os bixo (só para fase 1 e 2, fase 3 usa criar_boss)
        self.criar_revolver()
        self.criar_espingarda()
        self.criar_pitu()
        
        if len(self.grupo_inimigos) >= 5:
            return

        # só aparece os inimigos se tiver coletado a arma da fase E não estiver na fase completa
        if self.peixeira_coletada and not self.fase_completa1:
            tipo_inimigo = Inimigo
        elif self.revolver_coletado and not self.fase_completa2:
            tipo_inimigo = InimigoRapido
        else:
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

        self.grupo_inimigos.add(tipo_inimigo(x, y))

    def desenhar(self):
        
        # fundo do jogo
        self.tela.blit(self.imagem_fundo, (0, 0))
        
        #filtro vermelho se a vida dele tiver baixa
        if self.player.vida_jogador <= 3:
            #cria uma superfície transparente
            surf_filtro = pygame.Surface((1024, 637), pygame.SRCALPHA)
            surf_filtro.fill((255, 0, 0, 40))
            self.tela.blit(surf_filtro, (0, 0)) 

        # desenhar o jogador
        self.player.desenhar(self.tela)

        # desenhar os tiros
        self.grupo_projeteis.draw(self.tela)

        # desenhar os inimigos
        self.grupo_inimigos.draw(self.tela)
        
        # desenhar os coletaveis
        for coletavel in self.grupo_coletaveis:
            coletavel.desenhar(self.tela)
        
        # mostrar a hud
        self._desenhar_hud()
        self.desenhar_mensagens()

        # efeito visual do arco da peixeira (dura 150ms)
        if self.golpe_peixeira and pygame.time.get_ticks() - self.tempo_golpe < 150:
            surf_arco = pygame.Surface((1024, 637), pygame.SRCALPHA)
            pygame.draw.polygon(surf_arco, (255, 255, 255, 80), self.golpe_peixeira)
            self.tela.blit(surf_arco, (0, 0))

        # barrinha de vida do boss
        self.barrinha_vida_boss()

        # desenha o inventário (HUD das armas)
        self.inventario.desenhar_hud(self.tela)

        pygame.display.flip()

    def _desenhar_texto_com_sombra(self, fonte, texto, cor, pos):
        sombra = fonte.render(texto, True, self.COR_SOMBRA)
        surf = fonte.render(texto, True, cor)
        self.tela.blit(sombra, (pos[0] + 2, pos[1] + 2))
        self.tela.blit(surf, pos)

    def _desenhar_hud(self):
        # barrinha de vida do player
        self.barrinha_vida_player()

        # kills (só mostra nas fases 1 e 2)
        if not self.fase_completa2:
            self._desenhar_texto_com_sombra(self.fonte, f"Kills: {self.kills}/10", self.COR_TEXTO, (10, 48))

    def desenhar_mensagens(self):        
        # msg antes de pegar a peixeira
        if not self.peixeira_coletada:
            surf = self.fonte.render("Colete a Peixeira para começar!", True, (255, 255, 0))
            x = (1024 - surf.get_width()) // 2
            self._desenhar_texto_com_sombra(self.fonte, "Colete a Peixeira para começar!", (255, 255, 0), (x, 150))

        elif self.fase_completa1 and not self.revolver_coletado:
            mensagem = "Você venceu a primeira fase! Colete a arma!"
            mensagem2 = "Clique '2' para usar a pistola e '1' para usar a faca."
            surf = self.fonte_pequena.render(mensagem, True, (0, 255, 0))
            # width descobre quantos pixels de largura tem o texto, pra centralizar
            posicao_x = (1024 - surf.get_width()) // 2
            posicao_y = 150
            self._desenhar_texto_com_sombra(self.fonte_pequena, mensagem, (0, 255, 0), (posicao_x, posicao_y))
            
            #segunda mensagem
            surf2 = self.fonte_pequena.render(mensagem2, True, (0, 255, 0))
            posicao_x2 = (1024 - surf2.get_width()) // 2
            posicao_y2 = posicao_y + 40 
            
            # Desenha a mensagem 2 na tela
            self._desenhar_texto_com_sombra(self.fonte_pequena, mensagem2, (0, 255, 0), (posicao_x2, posicao_y2))

        elif self.fase_completa2 and not self.espingarda_coletada:
            mensagem = "Você venceu a segunda fase! Colete a arma! Agora você vai enfrentar o inimigo final!"
            mensagem2 = "Clique '3' para usar a espingarda."
            surf = self.fonte_pequena.render(mensagem, True, (0, 255, 0))
            posicao_x = (1024 - surf.get_width()) // 2
            posicao_y = 150
            self._desenhar_texto_com_sombra(self.fonte_pequena, mensagem, (0, 255, 0), (posicao_x, posicao_y))
            
            #segunda mensagem
            surf2 = self.fonte_pequena.render(mensagem2, True, (0, 255, 0))
            posicao_x2 = (1024 - surf2.get_width()) // 2
            posicao_y2 = posicao_y + 40 
            
            # Desenha a mensagem 2 na tela
            self._desenhar_texto_com_sombra(self.fonte_pequena, mensagem2, (0, 255, 0), (posicao_x2, posicao_y2))

        elif self.fase_completa3:
            surf_v = self.fonte_grande.render("Você venceu!", True, (255, 215, 0))
            x_v = (1024 - surf_v.get_width()) // 2
            self._desenhar_texto_com_sombra(self.fonte_grande, "Você venceu!", (255, 215, 0), (x_v, 250))

        # derrota
        if self.player.vida_jogador <= 0:
            # bagulho de sombra do game over
            surf_g = self.fonte_grande.render("Game Over", True, (255, 0, 0))
            x_g = (1024 - surf_g.get_width()) // 2
            self._desenhar_texto_com_sombra(self.fonte_grande, "Game Over", (255, 0, 0), (x_g, 250))