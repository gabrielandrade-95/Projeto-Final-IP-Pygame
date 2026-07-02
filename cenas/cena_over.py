#cena_over.py
import pygame
import sys


class CenaOver:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador

        fundo = pygame.image.load("assets/telas/tela_over.png").convert()
        self.fundo = pygame.transform.scale(fundo, (1024, 637))

        # botão de reiniciar
        reset_0 = pygame.image.load("assets/botoes/reset_0.png").convert_alpha()
        reset_1 = pygame.image.load("assets/botoes/reset_1.png").convert_alpha()
        bounding_reset = reset_0.get_bounding_rect()
        self.reset_0 = reset_0.subsurface(bounding_reset).copy()
        self.reset_1 = reset_1.subsurface(bounding_reset).copy()

        # botão de menu
        menu_0 = pygame.image.load("assets/botoes/menu_0.png").convert_alpha()
        menu_1 = pygame.image.load("assets/botoes/menu_1.png").convert_alpha()
        bounding_menu = menu_0.get_bounding_rect()
        self.menu_0 = menu_0.subsurface(bounding_menu).copy()
        self.menu_1 = menu_1.subsurface(bounding_menu).copy()

        # botão de sair
        exit_0 = pygame.image.load("assets/botoes/exit_0.png").convert_alpha()
        exit_1 = pygame.image.load("assets/botoes/exit_1.png").convert_alpha()
        bounding_exit = exit_0.get_bounding_rect()
        exit_0_crop = exit_0.subsurface(bounding_exit).copy()
        exit_1_crop = exit_1.subsurface(bounding_exit).copy()
        tamanho_exit = (int(exit_0_crop.get_width() * 0.6), int(exit_0_crop.get_height() * 0.6))
        self.exit_0 = pygame.transform.scale(exit_0_crop, tamanho_exit)
        self.exit_1 = pygame.transform.scale(exit_1_crop, tamanho_exit)

        largura_btn = self.reset_0.get_width()
        gap = 450
        total = largura_btn * 2 + gap
        start_x = (1024 - total) // 2
        y_botoes = 500

        self.rect_reset = self.reset_0.get_rect(topleft=(start_x, y_botoes))
        self.pos_reset  = self.rect_reset.topleft

        self.rect_menu = self.menu_0.get_rect(topleft=(start_x + largura_btn + gap, y_botoes))
        self.pos_menu  = self.rect_menu.topleft

        self.rect_exit = self.exit_0.get_rect(topleft=(15, 15))
        self.pos_exit  = self.rect_exit.topleft

    def checar_eventos(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_reset.collidepoint(evento.pos):

                #TOCAR MUSICA TEMA DAS FASES
                pygame.mixer.music.stop()
                pygame.mixer.music.load("assets/sons/musica_tema.mp3")
                pygame.mixer.music.play(-1)

                self.gerenciador.reiniciar_jogo()
                
            elif self.rect_menu.collidepoint(evento.pos):
                self.gerenciador.ir_para_menu()
            elif self.rect_exit.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()

    def atualizar(self):
        pass

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

        mouse = pygame.mouse.get_pos()

        # mostra sprite pressionado quando o mouse está sobre o botão
        if self.rect_reset.collidepoint(mouse):
            tela.blit(self.reset_1, self.pos_reset)
        else:
            tela.blit(self.reset_0, self.pos_reset)

        if self.rect_menu.collidepoint(mouse):
            tela.blit(self.menu_1, self.pos_menu)
        else:
            tela.blit(self.menu_0, self.pos_menu)

        if self.rect_exit.collidepoint(mouse):
            tela.blit(self.exit_1, self.pos_exit)
        else:
            tela.blit(self.exit_0, self.pos_exit)