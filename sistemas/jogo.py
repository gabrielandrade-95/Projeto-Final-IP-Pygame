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
        
        self.fonte_pequena = pygame.font.SysFont(None, 36)

        #cria o player
        self.player = Jogador(400, 300)

        #sprite
        self.grupo_projeteis = pygame.sprite.Group()
        self.grupo_inimigos = pygame.sprite.Group()
        self.grupo_coletaveis = pygame.sprite.Group()

        #inv
        self.inventario = Inventario()

        #contadores
        self.kills = 0
        self.fase_completa1 = False
        self.fase_completa2 = False
        self.fase_completa3 = False

        self.peixeira_coletada = False
        self.revolver_coletado = False
        self.espingarda_coletada = False

        #cria a peixeira no chão 
        peixeira = Peixeira(400, 250)
        self.grupo_coletaveis.add(peixeira)
        
        


        caminho_fonte = "assets/Smokum.ttf"

        try:
            self.fonte = pygame.font.Font(caminho_fonte, 36)
            self.fonte_grande = pygame.font.Font(caminho_fonte, 72)
        except FileNotFoundError:

            #por a fonte
            self.fonte = pygame.font.SysFont("impact", 36)
            self.fonte_grande = pygame.font.SysFont("impact", 72)

        #cor dos texto
        self.COR_TEXTO = (255, 255, 255)  #branco
        self.COR_SOMBRA = (0, 0, 0)       #preto para sombra

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

                #troca de arma se tiver arma
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
        #spawnar os bixo
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
        #ve se a bala pegou no inimigo
        for projetil in self.grupo_projeteis:
            for inimigo in self.grupo_inimigos:
                if inimigo.dano_inimigo(projetil):
                    self.kills += 1

    def checar_vida(self):
        #ver se morreu
        if self.player.vida_jogador <= 0:
            return True
        return False
    
    def criar_revolver(self):
        if (self.fase_completa1) and (not self.fase_completa2) and (not self.revolver_coletado):
            revolver = Revolver(400, 250)
            self.grupo_coletaveis.add(revolver)
        
    def criar_espingarda(self):
        if (self.fase_completa2) and (not self.fase_completa3) and (not self.espingarda_coletada):
            espingarda = Espingarda(400, 250)
            self.grupo_coletaveis.add(espingarda)

    def atualizar(self):
        #se morrer para tudo
        if self.player.vida_jogador <= 0:
            self.rodando = False
            return

        #movimento
        self.player.mover()
        self.grupo_projeteis.update()

        #colisoes
        self.checar_colisoes()
        self.player.dano_jogador(self.grupo_inimigos)
        
        

        #atualizar inimigos
        for inimigo in self.grupo_inimigos:
            inimigo.update(self.player, self.grupo_inimigos)
            
        #vendo se já pode criar revolver ou espingarda
        self.criar_revolver()
        self.criar_espingarda()

        #processar a coleta de itens
        for coletavel in self.grupo_coletaveis:
            coletavel.processar_coleta(self.player, self.inventario)

            #se coletou a peixeira ativa os inimigos
            if isinstance(coletavel, Peixeira) and coletavel.coletado:
                self.peixeira_coletada = True
            
            elif isinstance(coletavel, Revolver) and coletavel.coletado:
                self.revolver_coletado = True
            
            elif isinstance(coletavel, Espingarda) and coletavel.coletado:
                self.espingarda_coletada = True

        # verificando se a fase foi completada
        if self.fase_completa1 == False and self.kills >= 10:
            self.fase_completa1 = True
            self.grupo_inimigos.empty()
            self.kills = 0
        elif (self.fase_completa2 == False) and (self.fase_completa1 == True) and self.kills >= 10:
            self.fase_completa2 = True
            self.grupo_inimigos.empty()
            self.kills = 0
        elif (self.fase_completa3 == False) and (self.fase_completa2 == True) and self.kills >= 10:
            self.fase_completa3 = True
            self.grupo_inimigos.empty()
            self.kills = 0

        #so aparece os inimigos se tiver coletado a arma da fase E não estiver na fase completa
        if self.peixeira_coletada and not self.fase_completa1:
            self.onda_inimigos(self.grupo_inimigos, self.player)
        
        elif self.revolver_coletado and not self.fase_completa2:
            self.onda_inimigos(self.grupo_inimigos, self.player)

    def desenhar(self):
        #fundo do jogo
        if self.player.vida_jogador <= 3:
            self.tela.fill((100, 30, 27))  #vermelho quando ta baixa
        else:
            self.tela.fill((242, 133, 0))  #laranja com a vida cheia

        #desenhar o jogador
        self.player.desenhar(self.tela)

        #desenhar os tiros
        self.grupo_projeteis.draw(self.tela)

        #desenhar os inimigos
        self.grupo_inimigos.draw(self.tela)

        #desenhar o coletavel da faca
        for coletavel in self.grupo_coletaveis:
            coletavel.desenhar(self.tela)

        #mostrar a hud
        kills_surf = self.fonte.render(f"Kills: {self.kills}/10", True, self.COR_TEXTO)     #kills
        kills_sombra = self.fonte.render(f"Kills: {self.kills}/10", True, self.COR_SOMBRA)

        self.tela.blit(kills_sombra, (12, 12))
        self.tela.blit(kills_surf, (10, 10))

     
        vida_surf = self.fonte.render(f"Vida: {int(self.player.vida_jogador)}", True, self.COR_TEXTO)  #vida
        vida_sombra = self.fonte.render(f"Vida: {int(self.player.vida_jogador)}", True, self.COR_SOMBRA)

        self.tela.blit(vida_sombra, (12, 52))
        self.tela.blit(vida_surf, (10, 50))

     
       
     
        if not self.peixeira_coletada and not self.fase_completa1:           #msg antes de pegara pexeira
            msg_surf = self.fonte.render(f"Colete a Peixeira para começar!", True, (255, 255, 0))
            msg_sombra = self.fonte.render(f"Colete a Peixeira para começar!", True, self.COR_SOMBRA)
            self.tela.blit(msg_sombra, (152, 152))
            self.tela.blit(msg_surf, (150, 150))

     
        elif self.fase_completa1 and not self.revolver_coletado:
            
            mensagem = "Você venceu a primeira fase! Colete a arma!"
                      
            fase_texto_surf = self.fonte_pequena.render(mensagem, True, (0, 255, 0))
            fase_texto_sombra = self.fonte_pequena.render(mensagem, True, self.COR_SOMBRA)
            
            largura_texto = fase_texto_surf.get_width() #witdth descobre quantos pixels de largura tem o texto, pra centralizar
            posicao_x = (800 - largura_texto) // 2 #800 é a largura da tela
            posicao_y = 150

            self.tela.blit(fase_texto_sombra, (posicao_x + 2, posicao_y + 2))
            self.tela.blit(fase_texto_surf, (posicao_x, posicao_y))

        elif self.fase_completa2 and not self.espingarda_coletada:
            mensagem = "Você venceu a segunda fase! Colete a arma! Agora você vai enfrentar o inimigo final!"
            fase_texto_surf = self.fonte_pequena.render(mensagem, True, (0, 255, 0))
            fase_texto_sombra = self.fonte_pequena.render(mensagem, True, self.COR_SOMBRA)
            largura_texto = fase_texto_surf.get_width()
            posicao_x = (800 - largura_texto) // 2
            posicao_y = 150

            self.tela.blit(fase_texto_sombra, (posicao_x + 2, posicao_y + 2))
            self.tela.blit(fase_texto_surf, (posicao_x, posicao_y))
        
        if self.player.vida_jogador == 0:           #derrota
            texto_fim = self.fonte_grande.render("Game Over", True, (255, 0, 0))
            fim_sombra = self.fonte_grande.render("Game Over", True, self.COR_SOMBRA)

            self.tela.blit(fim_sombra, (203, 253))      #bagulho de sombra do game over
            self.tela.blit(texto_fim, (200, 250))

        self.inventario.desenhar_hud(self.tela)          #desenha o inventário (HUD das armas)

        pygame.display.flip()
