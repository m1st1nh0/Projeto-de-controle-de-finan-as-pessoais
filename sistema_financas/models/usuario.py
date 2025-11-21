class Usuario:

    def __init__(self, nome, remuneracao_fixa, remuneracao_variavel):
        self.nome = nome
        self.remuneracao_fixa = remuneracao_fixa
        self.remuneracao_variavel = remuneracao_variavel
        self.cartoes = []
        self.gastos = []

    def __repr__(self):
        return f"Usuario(nome='{self.nome}', cartoes={len(self.cartoes)}, gastos={len(self.gastos)})"
