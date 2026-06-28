import pygame

class Inimigos :
    
    lista_fases = []
    inimigos_mortos = 0

    if inimigos_mortos == 10 and len(lista_fases) == 0:
        lista_fases.append("Fase 1")
        inimigos_mortos = 0
    elif inimigos_mortos == 15 and len(lista_fases) == 1:
        lista_fases.append("Fase 2")
        inimigos_mortos = 0
    elif inimigos_mortos == 5 and len(lista_fases) == 2:
        lista_fases.append("Fase 3")
        inimigos_mortos = 0

    def atacar() :
        pass

    def sofrer_dano() :
        pass


class InimigoComum(Inimigos) :
    def __init__(self, vida, dano) :
        self.vida = vida



class Boss(Inimigos) :
    pass
import pygame
import random


class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocidade = 1.5
        self.ultimo_dano = 0
        self.cooldown_dano = 500  # dano a cada meio segundo

    def update(self, jogador, grupo_inimigos):
        # movimento em direção ao jogador
        dx = jogador.rect.centerx - self.rect.centerx
        dy = jogador.rect.centery - self.rect.centery
        distancia = (dx**2 + dy**2) ** 0.5

        if distancia != 0:
            dx /= distancia
            dy /= distancia

        vel_x = dx * self.velocidade
        vel_y = dy * self.velocidade

        # repulsão entre inimigos para não ficar um por cima do outro
        for outro in grupo_inimigos:
            if outro != self and self.rect.colliderect(outro.rect):
                dist_x = self.rect.centerx - outro.rect.centerx
                dist_y = self.rect.centery - outro.rect.centery
                dist = (dist_x**2 + dist_y**2) ** 0.5
                if dist != 0:
                    vel_x += (dist_x / dist) * 3
                    vel_y += (dist_y / dist) * 3

        self.rect.x += vel_x
        self.rect.y += vel_y

    def dano_inimigo(self, projetil):
        if self.rect.colliderect(projetil.rect):
            self.kill()
            projetil.kill()
            return True
        return False


# class Boss(Inimigo):
    