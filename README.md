# 1-Projeto-Solver

#Tarefa: Crie um diagrama de fluxo ou processo que represente o ciclo de uma compra no cartão de 
# crédito e o cálculo dos juros, considerando:
# Registro das compras.
# Fechamento da fatura.
# Data de pagamento.
# Cálculo de juros se o pagamento ocorrer após o dia 25.

from graphviz import Digraph
from datetime import datetime

# Adicionar compras
compras = []
while True:
    valor = input("Digite o valor da compra (ou 'done' para finalizar): ")
    if valor.lower() == 'done':
        break
    compras.append(float(valor))

# Data de pagamento
data_pagamento = input("Digite a data de pagamento (dd/mm/aaaa): ")
data_pagamento = datetime.strptime(data_pagamento, '%d/%m/%Y')

# Data de fechamento da fatura
data_fechamento = input("Digite a data de fechamento da fatura (dd/mm/aaaa): ")
data_fechamento = datetime.strptime(data_fechamento, '%d/%m/%Y')

# Cálculo de juros
total_compras = 0
for compra in compras:
    total_compras += compra

if data_pagamento.day <= 25:
    juros = 0
    status_pagamento = 'Pagamento sem juros'
else:
    dias_atraso = data_pagamento.day - 25
    juros = total_compras * (0.03 + dias_atraso * 0.01)
    status_pagamento = 'Cálculo de juros'

total_pagar = total_compras + juros

# Exibir informações
print(f"Compras registradas: {compras}")
print(f"Data de fechamento definida para: {data_fechamento.strftime('%d/%m/%Y')}")
print(f"Data de pagamento definida para: {data_pagamento.strftime('%d/%m/%Y')}")
print(f"Juros aplicados: R$ {juros:.2f}")
print(f"Total a pagar: R$ {total_pagar:.2f}")

# Criação do fluxograma
dot = Digraph()

# Definindo os nós do fluxograma com valores
dot.node('A', f'Registro das compras\nTotal Compras: R$ {total_compras:.2f}')
dot.node('B', f'Fechamento da fatura\n{data_fechamento.strftime("%d/%m/%Y")}')
dot.node('C', 'Emissão da fatura')
dot.node('D', f'Data de pagamento\n{data_pagamento.strftime("%d/%m/%Y")}')
dot.node('E', f'Pagamento sem juros\nTotal a pagar: R$ {total_compras:.2f}')
dot.node('F', f'Cálculo de juros\nJuros: R$ {juros:.2f}\nTotal a pagar: R$ {total_pagar:.2f}')

# Adicionando as arestas (conexões) entre os nós
dot.edges(['AB', 'BC', 'CD'])
dot.edge('D', 'E', label='Pagamento até dia 25')
dot.edge('D', 'F', label='Pagamento após dia 25')

# Renderizando o fluxograma
dot.render('fluxograma', format='pdf', view=True)
