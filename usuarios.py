import datetime

class Usuario:
    # Método constructor
    def __init__(self, nome, remuneracao_fixa, remuneracao_variavel):
        self.nome = nome
        self.remuneracao_fixa = remuneracao_fixa
        self.remuneracao_variavel = remuneracao_variavel
        self.cartoes = []
        self.gastos = []

    # Métodos de utilidade

    #Adiciona gastos ao usuário, diferenciando por método de pagamento
    def adicionar_gasto(self, gasto,nome_cartao=None):
        if gasto.metodo_pagamento == 'Crédito' and nome_cartao is not None:
            for cartao in self.cartoes:
                if cartao.nome == nome_cartao:
                    cartao.compras.append(gasto)
                    return
        else: 
            self.gastos.append(gasto)

    #Adicionar gastos ao cartão
    def adicionar_gastos_cartao(self, gasto,nome_cartao=None):
        if gasto.metodo_pagamento != 'Crédito' or nome_cartao is None:
            self.gastos.append(gasto)

        for cartao in self.cartoes:
            if cartao.nome == nome_cartao:
                data = datetime.datetime.strptime(gasto.data, 'd%/m%/Y%')
                for p in range(gasto.parcelas):
                    mes_fatura = (data.month +p-1)%12 +1
                    ano_fatura = data.year +((data.month+p-1)//12)

                    
                    parcela = Gasto(
                    nome=f"{gasto.nome} - Parcela {p+1}/{gasto.parcelas}",
                    valor=gasto.valor/gasto.parcelas,
                    metodo_pagamento=gasto.metodo_pagamento,
                    data=f"{gasto.data_pagamento}",
                    periodicidade=gasto.periodicidade,
                    categoria=gasto.categoria,
                    parcelas=1)

                    fatura_existente = None
                    for fatura in cartao.fatura:
                        if fatura.mes == mes_fatura and fatura.ano == ano_fatura:
                            fatura_existente = fatura
                            break
                    if not fatura_existente:
                        fatura_existente = Fatura(cartao,cartao.dia_vencimento,mes_fatura,ano_fatura)
                        fatura_existente.gastos.append(parcela)
                        cartao.compras.append(parcela)
                        return
                        


            return

        pass

    #Instancia um cartão e o adiciona a lista de cartões do usuário
    def adicionarCartao(self,nome,limite,vencimento):
        self.cartoes.append(CartaoDeCredito(nome, limite, vencimento))


    #Métodos de exibição

    #Resumo das infomações do usuário
    def resumo(self):
        return (
            f'Usuário: {self.nome}\n'
            f'Remuneração: {self.remuneracao_fixa}\n'
            f'Remuneração variável: {self.remuneracao_variavel}\n'
            f'Catões: {[cartao.nome for cartao in self.cartoes]}\n')    

    #Exibe gastos avista           
    def meus_gastos(self):
        for gasto in self.gastos:
            print(gasto.detalhes_gasto())
            print()

    #Exibe gastos cartão
    def resumo_cartao(self,nome):
        for cartao in self.cartoes:
            if cartao.nome == nome:
                for compra in cartao.compras:
                    print(compra.detalhes_gasto())
                    print()
                    print()

    #Exibe gastos totais
    def todos_gastos(self):
        print('Gastos pagos avista:')
        for gasto in self.gastos:
            print(gasto.detalhes_gasto())
            print()
        print('Gastos via Cartão:')
        for cartao in self.cartoes:
            for compra in cartao.compras:
                print(f'Cartão: {cartao.nome}')
                print(compra.detalhes_gasto())
                print()              
    

class Gasto:

    #Método construtor
    
    def __init__(self, nome,valor, metodo_pagamento,data,periodicidade,categoria, parcelas =1):
        self.nome = nome
        self.valor = valor
        self.metodo_pagamento = metodo_pagamento
        self.data = data
        self.periodicidade = periodicidade
        self.categoria = categoria
        self.parcelas = parcelas

    #Métodos de exibição

    #Exibe detalhes do gasto   
    def detalhes_gasto(self):
        return (
            f'Gasto: {self.nome}\n'
            f'valor: {self.valor}\n'
            f'Método de pagamento: {self.metodo_pagamento}\n'
            f'Data do pagamento: {self.data}\n'
            f'Categoria: {self.categoria}\n'
            f'Parcelas: {self.parcelas}\n'
            f'Periodicidade: {self.periodicidade}'
        )


class CartaoDeCredito:

    #Método construtor
    
    def __init__(self, nome,limite,dia_vencimento):
        self.nome = nome
        self.limite = limite
        self.dia_vencimento = dia_vencimento
        self.fatura = []
        self.compras = []

class Fatura:

    #Método construtor

    def __init__(self,cartao,dia_vencimento,mes,ano):
        self.cartao = cartao
        self.dia_vencimento = dia_vencimento
        self.mes = mes
        self.ano = ano
        self.gastos = []
        self.valor_pago = 0
        self.paga = False
        
        
            
        

lucas = Usuario('Lucas', 1800, 700)
lucas.adicionarCartao('Visa', 2000, 10)
lucas.adicionarCartao('Master', 1500, 5)

gasto1 = Gasto('Mercado', 350, 'Avista', '10/11/2025', 'Semanal', 'Alimentação')
lucas.adicionar_gasto(gasto1)
gasto2 = Gasto('Ganja', 150, 'Avista', '10/11/2025', 'Quinzanal', 'Lazer')
lucas.adicionar_gasto(gasto2)
lucas.meus_gastos()  # Deve imprimir 2 gastos

gasto3 = Gasto('Cinema', 120, 'Crédito', '10/11/2025', 'Mensal', 'Lazer')
lucas.adicionar_gastos_cartao(gasto3, 'Visa')

lucas.resumo_cartao('Visa')  # Deve imprimir o gasto do cartão
lucas.todos_gastos()


