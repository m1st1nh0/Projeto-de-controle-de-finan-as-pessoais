from utils.validadores import ValidadorGasto


def solicitar_gasto_interativo():
    print("\n=== CADASTRO DE NOVO GASTO ===\n")

    while True:
        nome = input("Nome do gasto:  ").strip()
        if nome:
            break
        print("❌ Erro: Descrição não pode ser vazia!\n")

    while True:
        try:
            valor_str = input("Valor (R$):  ")
            valor = float(valor_str)
            valor = ValidadorGasto.validar_valor(valor)
            break
        except ValueError as e:
            print(f"❌ Erro: {e}\n")
        except TypeError as e:
            print(f"❌ Erro: {e}\n")

    print(f"\nCategorias disponíveis")
    categorias = sorted(ValidadorGasto.CATEGORIAS_VALIDAS)
    for i, cat in enumerate(categorias, 1):
        print(f"{i}. {cat}")

    while True:
        try:
            opcao = int(input("\nEscolha o numero da categoria: "))
            if 1 <= opcao <= len(categorias):
                categoria = categorias[opcao - 1]
                break
            else:
                print(f"❌ Escolha entre 1 e {len(categorias)}!\n")
        except ValueError:
            print("❌ Digite um número válido!\n")

    print(f"\nMétodos de pagamento:")
    print(" 1. À vista")
    print(" 2. Crédito")

    while True:
        try:
            opcao = int(input("\nDigite sua escolha: "))
            if opcao == 1:
                metodo = "Avista"
                break
            elif opcao == 2:
                metodo = "Crédito"
                break
            else:
                print("❌ Escolha 1 ou 2!\n")
        except ValueError:
            print("❌ Digite um número válido!\n")

    while True:
        try:
            data = input("\nData da compra DD/MM/AAAA:  ")
            data = ValidadorGasto.validar_data(data)
            break
        except (ValueError, TypeError) as e:
            print(f"❌ Erro: {e}\n")

    print("\nPeriodicidade:")
    periodicidades = sorted(ValidadorGasto.PERIODICIDADES_VALIDAS)
    for i, per in enumerate(periodicidades, 1):
        print(f"{i}. {per}")

    while True:
        try:
            opcao = int(input("\nDigite sua opção de periodicidade: "))
            if 1 <= opcao <= len(periodicidades):
                periodicidade = periodicidades[opcao - 1]
                break
            else:
                print(f"Digite um número entre 1 e {len(periodicidades)}\n")
        except ValueError:
            print("❌ Digite um número válido!\n")

    parcelas = 1
    if metodo == "Crédito":
        while True:
            try:
                parcelas_str = input("\nNúmero de parcelas (1/36):  ")
                parcelas = int(parcelas_str)
                parcelas = ValidadorGasto.validar_parcelas(parcelas)
                break
            except (ValueError, TypeError) as e:
                print(f"❌ Erro: {e}\n")

    return {
        "nome": nome,
        "valor": valor,
        "metodo_pagamento": metodo,
        "data": data,
        "periodicidade": periodicidade,
        "categoria": categoria,
        "parcelas": parcelas,
    }


if __name__ == "__main__":
    try:
        dados_gasto = solicitar_gasto_interativo()
        print("\n✅ Gasto cadastrado com sucesso!")
        print("\nDados:")
        for chave, valor in dados_gasto.items():
            print(f"  {chave}: {valor}")
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
