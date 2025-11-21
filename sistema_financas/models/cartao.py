class CartaoDeCredito:

    def __init__(self, nome, limite, dia_vencimento):
        self._nome = nome
        self._limite_total = self.__validar_limite(limite)
        self._limite_disponivel = self._limite_total
        self._dia_vencimento = self.__validar_dia_vencimento(dia_vencimento)
        self._faturas = []
        self._compras = []

    # validações privadas---------------------------------
    def __validar_limite(self, limite):
        if limite <= 0:
            raise ValueError(f"Limite deve ser maior que 0. Limite recebido {limite}")
        return float(limite)

    def __validar_dia_vencimento(self, dia):
        if dia <= 0 and dia > 31:
            raise ValueError(
                f"O dia de vencimento deve estar entre 1 e 31. Dia inserido: {dia}"
            )
        return int(dia)

    # properties---------------------------------
    @property
    def nome(self):
        return self._nome

    @property
    def limite_total(self):
        return self._limite_total

    @property
    def limite_disponivel(self):
        return self._limite_disponivel

    @property
    def dia_vencimento(self):
        return self._dia_vencimento

    @property
    def faturas(self):
        return self._faturas.copy()

    @property
    def compras(self):
        return self._compras.copy()

    # metodos publicos---------------------------------
    def consumir_limite(self, valor):

        if valor > self._limite_disponivel:
            raise ValueError(
                f"Limite Insuficiente!"
                f"Disponível: R$ {self._limite_disponivel:.2f},"
                f"Necessário: R$ {valor:.2f}"
            )
        self._limite_disponivel -= valor

    def liberar_limite(self, valor):
        novo_limite = self._limite_disponivel + valor

        if novo_limite > self._limite_total:
            raise ValueError(
                f"Liberar o valor do pagamento R$ {valor:.2f} excederá o limite total do cartão {self._nome}"
                f"Limite total: R$ {self._limite_total:.2f}"
                f"Limite com excedente: R$ {novo_limite:.2f}"
            )
        self._limite_disponivel = novo_limite

    def adicionar_fatura(self, fatura):

        self._faturas.append(fatura)

    def adicionar_compras(self, compra):

        self._compras.append(compra)

    def percentual_utilizado(self):

        utilizado = self._limite_total - self._limite_disponivel
        return (utilizado / self.limite_total) * 100

    # representações

    def __repr__(self):

        return (
            f"CartaoDeCredito(nome='{self._nome}', "
            f"limite={self._limite_disponivel:.2f}/{self._limite_total:.2f}, "
            f"utilização={self.percentual_utilizado():.1f}%)"
        )

    def __str__(self):

        return (
            f"{self._nome} - "
            f"Disponível: R$ {self._limite_disponivel:.2f} / "
            f"Total: R$ {self._limite_total:.2f}"
        )
