from models import Usuario, Gasto, CartaoDeCredito


def main():

    usuario = Usuario("Lucas Matheus", 1900, 680)
    print(f"Usuário criado com sucesso: {usuario}")

    usuario.cartoes.append(CartaoDeCredito("Visa", 2000, 15))

    print(f"Cartão criado com sucesso: {usuario.cartoes}")

    compra1 = Gasto(
        nome="Mercado",
        valor=200,
        metodo_pagamento="Avista",
        data="20/11/2025",
        periodicidade="Semanal",
        categoria="Alimentação",
    )
    usuario.gastos.append(compra1)

    print(f"Gasto registrado: {compra1}")
    print(f"\nTotal de gastos do usuário {len(usuario.gastos)}")


if __name__ == "__main__":
    main()
