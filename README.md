# 1-Projeto-Solver

#Tarefa: Crie um diagrama de fluxo ou processo que represente o ciclo de uma compra no cartão de 
# crédito e o cálculo dos juros, considerando:
# Registro das compras.
# Fechamento da fatura.
# Data de pagamento.
# Cálculo de juros se o pagamento ocorrer após o dia 25.

def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    return imc

def classificar_imc(imc):
    if imc < 18.5:
        return "Não desista, liberte o monstro dentro de você!"
    elif 18.5 <= imc < 24.9:
        return "Você está bem, continue se cuidando!"
    elif 25 <= imc < 29.9:
        return "Você está um pouco acima do peso, vamos treinar ^_-!"
    else:
        return "Está em uma zona perigosa, vamos lutar juntos!"

peso = float(input("Digite seu peso em kg: "))
altura = float(input("Digite sua altura em metros: "))

imc = calcular_imc(peso, altura)
classificacao = classificar_imc(imc)

print(f"Seu IMC é: {imc:.2f}")
print(f"Classificação: {classificacao}")
