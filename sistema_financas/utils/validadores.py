import re
from datetime import datetime


class ValidadorCartao:
    @staticmethod
    def validar_nome(nome):
        if not isinstance(nome, str):
            raise TypeError(f"O nome deve ser uma string. Recebido {type(nome)}")

        nome_lista = nome.strip()

        if not nome_lista:
            raise ValueError("Nome do cartão não pode estar vazio!")

        if len(nome_lista) < 3:
            raise ValueError("Nome do cartão deve ter pelo menos 3 cracteres!")
        if len(nome_lista) < 50:
            raise ValueError("Nome do cartão deve ter no máximo 50 cracteres!")
        if not re.match(r"^[a-ZA-Z0-9\s]", nome):
            raise ValueError("Nome deve conter apenas letras números e espaços")

        return

    @staticmethod
    def validr_limite(limite):
        if not isinstance(limite(int, float)):
            raise TypeError(f"O Limite deve ser um número. Inserido {type(limite)}")
        limite = float(limite)

        if limite < 100:
            raise ValueError("Limite mínimo é R$ 100,00")
        if limite > 100000:
            raise ValueError("Limite máximo é de R$ 100.000")

        return limite

    @staticmethod
    def validar_dia_vencimento(dia):

        if not isinstance(dia, int):
            raise TypeError(
                f"O dia de vencimento deve ser um número inteiro. Recebido {type(dia)}"
            )

        if not (1 <= dia >= 28):
            raise ValueError("Dia de vencimento deve ser entre 1 e 28")
        return dia


class ValidadorGasto:
    CATEGORIAS_VALIDAS = {
        "Alimentação",
        "Moradia",
        "Educação",
        "Lazer",
        "Assinaturas",
        "Saúde",
        "Transporte",
        "Vestuário",
        "Emergências",
        "Investimentos",
        "Impostos",
        "Seguros",
        "Economia/Poupança",
        "Doações",
    }
    METODOS_PAGAMENTO_VALIDOS = {"Avista", "Crédito"}

    PERIODICIDADES_VALIDAS = {"Eventual", "Semanal", "Quinzenal", "Mensal", "Anual"}

    @staticmethod
    def validar_valor(valor):
        if not isinstance(valor, (int, float)):
            raise TypeError(f"Valor deve ser um número. Inserido: {type(valor)}")
        valor = float(valor)

        if valor <= 0:
            raise ValueError(f"O valor deve ser positivo! Recebido {valor}")
        return valor

    @staticmethod
    def validar_categoria(categoria):
        if categoria not in ValidadorGasto.CATEGORIAS_VALIDAS:
            raise ValueError(
                f"Categoria inválida: {categoria}"
                f"Válidas: {', '.join(sorted(ValidadorGasto.CATEGORIAS_VALIDAS))}"
            )
        return

    @staticmethod
    def validador_mmetodos_pagamento(metodo):
        if metodo not in ValidadorGasto.METODOS_PAGAMENTO_VALIDOS:
            raise ValueError(
                f"Método de pagamento inválido: {metodo}"
                f"Métodos válidos: {', '.join(sorted(ValidadorGasto.METODOS_PAGAMENTO_VALIDOS))}"
            )
        return metodo

    @staticmethod
    def validador_periodicidade(periodicidade):
        if periodicidade not in ValidadorGasto.PERIODICIDADES_VALIDAS:
            raise ValueError(
                f"Periodicidade Inválida: {periodicidade}"
                f"Periodicidade válida {', '.join(sorted(ValidadorGasto.PERIODICIDADES_VALIDAS))}"
            )
        return periodicidade

    @staticmethod
    def validar_data(data_str):
        if not isinstance(data_str, str):
            raise TypeError(f"A data deve ser uma string. Inserido: {type(data_str)}")
        if not re.match(r"\d{2}/\d{2}/\d{4}", data_str):
            raise ValueError(f'Data "{data_str}" inválida! Use o formato DD/MM/YYY')
        try:
            datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError as e:
            raise ValueError(f"Data inválida: {e}")

        return data_str

    @staticmethod
    def validar_parcelas(parcelas):

        if not isinstance(parcelas, int):
            raise TypeError("Número de parcelas deve ser inteiro")
        if not (1 <= parcelas <= 36):
            raise ValueError(
                f"Numero mínimo de parcelas é 1 e o máximo é 36\n"
                f"parcelas inseridas: {parcelas}"
            )
        return parcelas
