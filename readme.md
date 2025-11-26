# 📊 Projeto de Controle de Finanças Pessoais

Projeto para portfólio de controle de gastos pessoais, que permite gerenciar rendas, gastos e cartões de crédito de um usuário. Este projeto simula o comportamento real de um controle financeiro pessoal, utilizando **Python 3.10+** e conceitos de **Programação Orientada a Objetos (POO)**.

## 🚧 Status do Projeto

🟡 **Em desenvolvimento**

O projeto atualmente possui uma estrutura funcional que já permite cadastrar usuários, inserir cartões de crédito, registrar gastos e exibir resumos financeiros básicos. Funcionalidades novas estão sendo adicionadas conforme o desenvolvimento avança.

---

## 🧩 Funcionalidades

### ✅ Funcionalidades já implementadas:

#### 👤 Usuário
- **Cadastro** de informações do usuário (nome, remuneração fixa e variável);
- **Adição de cartões de crédito**;
- Registro de **gastos à vista e no crédito**;
- Visualização de **resumos e listas de gastos**.

#### 💳 Cartão de Crédito
- Armazena informações como nome, limite e dia de vencimento do cartão;
- Guarda compras e faturas associadas.

#### 📄 Fatura
- Representa a fatura mensal de um cartão;
- Armazena os gastos daquele período;
- Suporte a registro de pagamento (manual).

#### 💸 Gasto
- Representa cada despesa, com informações de:
  - Nome, valor, data, categoria, periodicidade e parcelas (para gastos no crédito);
  - Método de pagamento (à vista ou crédito).

### 🔄 Funcionalidades em desenvolvimento:
- **Cálculo automático** de limites e restituição de crédito conforme pagamento das faturas.
- **Controle automático** de faturas mensais (criação e fechamento mensais automáticos).
- **Classificação e relatórios** de gastos baseados em categorias.
- **Persistência dos dados**: salvar e carregar dados em arquivo JSON.
- Integração de uma interface de interação:
  - **CLI (Terminal)** ou
  - **Interface gráfica (GUI)**.

---

## 🧪 Exemplo de Uso Atual

```python
# Criação do usuário
lucas = Usuario('Lucas', 1800, 700)

# Adição de cartões
lucas.adicionarCartao('Visa', 2000, 10)
lucas.adicionarCartao('Master', 1500, 5)

# Registro de gastos
gasto1 = Gasto('Mercado', 350, 'Avista', '10/11/2025', 'Semanal', 'Alimentação')
lucas.adicionar_gasto(gasto1)

gasto2 = Gasto('Cinema', 120, 'Crédito', '10/11/2025', 'Mensal', 'Lazer')
lucas.adicionar_gastos_cartao(gasto2, 'Visa')

# Visualizações
lucas.meus_gastos()
lucas.resumo_cartao('Visa')
lucas.todos_gastos()
```

---

## 💻 Tecnologias Utilizadas

- **Python 3.10+**
- Módulo `datetime` para manipulação de datas.
- Conceitos de **Programação Orientada a Objetos (POO)**.

---

## 🌟 Próximos Passos

Planejamos implementar as seguintes funcionalidades e melhorias no projeto:

- Automação do **cálculo de limites e controle mensal** de faturas.
- **Relatórios detalhados**: análises e gráficos de gastos por categoria.
- **Persistência de dados**: salvar e carregar informações em arquivos JSON.
- **Interface de interação**: CLI para terminais ou GUI com bibliotecas como `tkinter` ou `PyQt`.

---

## 🎯 Sobre o Projeto

Este é um projeto pessoal desenvolvido como parte de estudos e para compor um portfólio demonstrativo. O objetivo é aprimorar habilidades com **Python** e **POO**, além de explorar boas práticas de desenvolvimento de sistemas.
