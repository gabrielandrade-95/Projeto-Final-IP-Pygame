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
