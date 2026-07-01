import pygame

def checar_colisao_retangulos(rect1, rect2):
    # Verifica se dois retângulos colidem
    return rect1.colliderect(rect2)