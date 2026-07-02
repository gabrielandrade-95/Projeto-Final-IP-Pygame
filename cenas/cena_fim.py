from cenas.telas_temporizadas import TelaTemporizada


class CenaFim(TelaTemporizada):
    def __init__(self, gerenciador):
        super().__init__(gerenciador, "assets/telas/tela_fim.png")

    def ao_terminar(self):
        self.gerenciador.ir_para_menu()