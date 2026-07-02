
from cenas.telas_temporizadas import TelaTemporizada


class CenaCreditos(TelaTemporizada):
    def __init__(self, gerenciador):
        super().__init__(gerenciador, "assets/telas/tela_creditos.png")

    def ao_terminar(self):
        self.gerenciador.creditos_terminou()