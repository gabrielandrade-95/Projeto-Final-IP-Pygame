# cena_menu.py
import sys
import pygame

# trilha sonora
pygame.mixer.init()
pygame.mixer.music.load("assets/sons/musica_principal.mp3")
pygame.mixer.music.play(-1)  # tocar infinitamente


class CenaMenu:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador

        fundo = pygame.image.load("assets/telas/tela_inicial.png").convert()
        self.fundo = pygame.transform.scale(fundo, (1024, 637))

        play_0 = pygame.image.load("assets/botoes/play_0.png").convert_alpha()
        play_1 = pygame.image.load("assets/botoes/play_1.png").convert_alpha()
        bounding_play = play_0.get_bounding_rect()
        self.play_0 = play_0.subsurface(bounding_play).copy()
        self.play_1 = play_1.subsurface(bounding_play).copy()

        creditos_0 = pygame.image.load(
            "assets/botoes/creditos_0.png").convert_alpha()
        creditos_1 = pygame.image.load(
            "assets/botoes/creditos_1.png").convert_alpha()
        tamanho_creditos = (int(creditos_0.get_width() * 0.7),
                            int(creditos_0.get_height() * 0.7))
        self.creditos_0 = pygame.transform.scale(creditos_0, tamanho_creditos)
        self.creditos_1 = pygame.transform.scale(creditos_1, tamanho_creditos)

        exit_0 = pygame.image.load("assets/botoes/exit_0.png").convert_alpha()
        exit_1 = pygame.image.load("assets/botoes/exit_1.png").convert_alpha()
        bounding_exit = exit_0.get_bounding_rect()
        exit_0_crop = exit_0.subsurface(bounding_exit).copy()
        exit_1_crop = exit_1.subsurface(bounding_exit).copy()
        tamanho_exit = (int(exit_0_crop.get_width() * 0.6),
                        int(exit_0_crop.get_height() * 0.6))
        self.exit_0 = pygame.transform.scale(exit_0_crop, tamanho_exit)
        self.exit_1 = pygame.transform.scale(exit_1_crop, tamanho_exit)

        self.rect_play = self.play_0.get_rect(
            centerx=512, bottom=600)  # posição do botão play
        self.pos_play = self.rect_play.topleft

        self.rect_creditos = self.creditos_0.get_rect(
            right=1010, bottom=625)  # posição do botão créditos
        self.pos_creditos = self.rect_creditos.topleft

        self.rect_exit = self.exit_0.get_rect(topleft=(15, 15))
        self.pos_exit = self.rect_exit.topleft

    def checar_eventos(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_play.collidepoint(evento.pos):

                # PARAR A MUSICA DO MENU
                pygame.mixer.music.stop()

                # INICIA MUSICA DAS FASES
                pygame.mixer.music.load("assets/sons/musica_tema.mp3")
                pygame.mixer.music.play(-1)

                self.gerenciador.iniciar_jogo()
            elif self.rect_creditos.collidepoint(evento.pos):
                self.gerenciador.ir_para_creditos() # para ir aos créditos
            elif self.rect_exit.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()

    def atualizar(self):
        pass

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

        mouse = pygame.mouse.get_pos()

        # mostra sprite pressionado quando o mouse está sobre o botão
        if self.rect_play.collidepoint(mouse):
            tela.blit(self.play_1, self.pos_play)
        else:
            tela.blit(self.play_0, self.pos_play)

        if self.rect_creditos.collidepoint(mouse):
            tela.blit(self.creditos_1, self.pos_creditos)
        else:
            tela.blit(self.creditos_0, self.pos_creditos)

        if self.rect_exit.collidepoint(mouse):
            tela.blit(self.exit_1, self.pos_exit)
        else:
            tela.blit(self.exit_0, self.pos_exit)
