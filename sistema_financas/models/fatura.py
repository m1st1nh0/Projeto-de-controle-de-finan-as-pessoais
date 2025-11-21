class Fatura:

    def __init__(self, cartao, mes, ano):
        self._cartao = cartao
        self._dia_vencimento = cartao._dia_vencimento
        self._mes = self.__validar_mes(mes)
        self._ano = self.__validar_ano(ano)
        self._gastos = []
        self._valor_pago = 0
        self._paga = False

    # validações privadas
    def __validar_mes(self, mes):

        if mes < 0 and mes > 12:
            raise ValueError(
                f"Mês inserido inválido: {mes}" f"Insira um mês entre 1 e 12"
            )
        return int(mes)

    def __validar_ano(self, ano):

        if ano < 2000 and ano > 2100:
            raise ValueError(f"Ano inserido inválido: {ano}")
        return int(ano)

    def __calcular_valor_total(self):

        return sum(gasto.valor for gasto in self._gastos)

    # properties---------------------------------
    @property
    def mes(self):
        return self._mes

    @property
    def ano(self):
        return self._ano

    @property
    def dia_vencimento(self):
        return self._dia_vencimento

    @property
    def gastos(self):
        return self._gastos.copy()

    @property
    def valor_total(self):
        return self.__calcular_valor_total()

    @property
    def valor_pago(self):
        return self._valor_pago

    @property
    def valor_restante(self):
        return self.valor_total - self._valor_pago

    @property
    def paga(self):

        return self._paga

    # metodos publicos

    def adicionar_gasto(self, gasto):
        self._gastos.append(gasto)

        if self._paga and self.valor_restante > 0:
            self._paga = False

    def registrar_pagamento(self, valor):

        if valor <= 0:
            raise ValueError(f"Valor de pagamento deve ser positivo!")
        if valor > self.valor_restante:
            raise ValueError(
                f" Pagamento de R$ {valor:.2f} excede valor atual da fatura: R$ {self.valor_restante:.2f}!"
            )
        self._valor_pago += valor

        if self.valor_restante <= 0.01:
            self._paga = True

    def esta_vencida(self, data_atual):
        from datetime import date

        data_vencimento = date(self._ano, self._mes, self._dia_vencimento)
        return data_atual < data_vencimento and not self._paga

    def __repr__(self):

        status = "PAGA" if self._paga else f"R$ {self.valor_restante:.2f} restante"
        return f"Fatura({self._mes:02d}/{self._ano}, Total: R$ {self.valor_total:.2f}, {status})"

    def __str__(self):

        return (
            f"Fatura {self._mes:02d}/{self._ano} - "
            f"Vencimento: dia {self._dia_vencimento} - "
            f"Total: R$ {self.valor_total:.2f} - "
            f"Pago: R$ {self._valor_pago:.2f} - "
            f"Restante: R$ {self.valor_restante:.2f}"
        )
