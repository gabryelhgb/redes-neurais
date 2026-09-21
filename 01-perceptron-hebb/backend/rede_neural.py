entradas = [
    [1, 1, 1, 1, 1],
    [-1, 1, -1, -1, 1],
    [1, 1, 1, -1, 1],
    [1, -1, -1, 1, 1],
]

saidas_desejadas = [1, 1, -1, -1]

pesos = [0, 0, 0, 0, 0]

print("Entradas:", entradas)
print("Saídas desejadas:", saidas_desejadas)
print("Pesos iniciais:", pesos)

def calcular_somatoria(entrada, pesos_atuais):
    somatorio = 0

    for indice in range(len(entrada)):
        somatorio += entrada[indice] * pesos_atuais[indice]

    return somatorio

def funcao_ativacao(somatorio):
    if somatorio >= 0:
        return 1
    else:
        return -1

def fazer_previsao(entrada, pesos_atuais):
    somatorio = calcular_somatoria(entrada, pesos_atuais)
    resposta = funcao_ativacao(somatorio)

    return resposta

primeira_entrada = entradas[0]

resposta_rede = fazer_previsao(primeira_entrada, pesos)

print("Primeira entrada:", primeira_entrada)
print("Resposta da rede:", resposta_rede)

