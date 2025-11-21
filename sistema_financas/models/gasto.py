class Gasto:

    def __init__(
        self, nome, valor, metodo_pagamento, data, periodicidade, categoria, parcelas=1
    ):
        self.nome = nome
        self.valor = valor
        self.metodo_pagamento = metodo_pagamento
        self.data = data
        self.periodicidade = periodicidade
        self.categoria = categoria
        self.parcelas = parcelas

    def __repr__(self):
        return f"Gasto('{self.nome}', R$ {self.valor:.2f}, {self.parcelas}x)"
