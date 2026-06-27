import pygame
#função generica pra detectar colisão entre dois objetos
def checar_colisao_retangulos(rect_um, rect_dois):
    return rect_um.colliderect(rect_dois)
