import pygame
import sys
import random
from Mecanicas.mecanicaPlayer import Jogador 
from entidades.projetil import Projetil
from entidades.novo_inimigo import Inimigo

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("O Cangaço")
        self.rodando = True
        self.relogio = pygame.time.Clock()

        # Cria o jogador usando a classe que veio da Mecanicas
        self.player = Jogador(400, 300)
        
        #grupos de sprites para os projeteis e inimigos
        self.grupo_projeteis = pygame.sprite.Group() 
        self.grupo_inimigos = pygame.sprite.Group()
        
        #contadores e estados
        self.kills = 0 
        self.fase_completa = False
        
        #spawna a primeira onda
        self.onda_inimigos(self.grupo_inimigos, self.player) # criando a primeira onda de inimigos

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
                        novo_tiro = Projetil(px + 15, py + 15, direcao)
                        self.grupo_projeteis.add(novo_tiro)
                        self.player.ultimo_tiro = tempo_atual

    def onda_inimigos(self, grupo_inimigos, jogador): # Método para criar uma onda de inimigos
        if len(grupo_inimigos) < 5: # Se tiver menos de 5 inimigos na tela
            x = 0
            y = 0
            borda = random.choice(["topo", "baixo", "esquerda", "direita"]) # Escolhe uma borda aleatória para o inimigo aparecer
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
    
    #verifica se o projetil colidiu com algum inimigo
    def checar_colisoes(self):
        for projetil in self.grupo_projeteis:
            for inimigo in self.grupo_inimigos:
                if inimigo.dano_inimigo(projetil):
                    self.kills += 1
                    
    def checar_vida(self):
        if self.player.vida_jogador <= 0:
            return True
        return False
    
    def atualizar(self):
        if self.player.vida_jogador <= 0:
            self.rodando = False
            return  # ← SAI DA FUNÇÃO AQUI
        
        # Movimento
        self.player.mover()
        self.grupo_projeteis.update()
        
        # Colisões
        self.checar_colisoes()
        self.player.dano_jogador(self.grupo_inimigos)
        
        # Atualizar inimigos (movimento + repulsão)
        for inimigo in self.grupo_inimigos:
            inimigo.update(self.player, self.grupo_inimigos)
        
        # Estados
        if self.kills >= 10:
            self.fase_completa = True
            self.grupo_inimigos.empty()
        
        # Spawn de inimigos        
        if not self.fase_completa:
            self.onda_inimigos(self.grupo_inimigos, self.player)
            
    def desenhar(self):
        self.tela.fill((40, 44, 52)) # cor de fundo
        #desenhar sprites
        self.player.desenhar(self.tela)
        self.grupo_projeteis.draw(self.tela)
        self.grupo_inimigos.draw(self.tela)
        
        #hud (texto de kills e fase)
        fonte = pygame.font.SysFont(None, 36)
        kills_texto = fonte.render(f"Kills: {self.kills}/10", True, (255, 255, 255))
        vida_texto = fonte.render(f"Vida: {int(self.player.vida_jogador)}", True, (255, 255, 255))
        self.tela.blit(vida_texto, (10, 50))
        self.tela.blit(kills_texto, (10, 10))

        #mensagem de fase completa
        if self.fase_completa:
            fase_texto = fonte.render("Você venceu! Colete a pistola!", True, (0, 255, 0))
            self.tela.blit(fase_texto, (200, 50))
        
        # Mensagem de derrota
        if self.player.vida_jogador <= 0:
            fonte_grande = pygame.font.SysFont(None, 72)
            texto_fim = fonte_grande.render("Game Over", True, (255, 0, 0))
            self.tela.blit(texto_fim, (200, 250))
        
        pygame.display.flip()

        