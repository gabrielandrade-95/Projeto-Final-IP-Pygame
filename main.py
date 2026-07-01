#main.py
#esse arquivo será onde o jogo irá ser inicializado
import sys
from cenas.gerenciador import Gerenciador

if __name__ == "__main__":
    gerenciador = Gerenciador()
    gerenciador.rodar()