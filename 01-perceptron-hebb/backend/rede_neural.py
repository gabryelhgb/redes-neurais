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

def atualizar_pesos(entrada, saida_desejada, resposta, pesos_atuais):
    erro = saida_desejada - resposta

    if erro!= 0:
        for indice in range(len(entrada)):
            delta_peso = entrada[indice] * saida_desejada
            pesos_atuais[indice] += delta_peso

    return erro


primeira_entrada = entradas[0]

resposta_rede = fazer_previsao(primeira_entrada, pesos)

print("Primeira entrada:", primeira_entrada)
print("Resposta da rede:", resposta_rede)

indice_teste = 2
entrada_teste = entradas[indice_teste]
saida_teste = saidas_desejadas[indice_teste]

resposta_antes = fazer_previsao(entrada_teste, pesos)

print()
print("Entrada de teste:", entrada_teste)
print("Saída desejada:", saida_teste)
print("Resposta da rede antes do ajuste:", resposta_antes)

erro = atualizar_pesos(
    entrada_teste,
    saida_teste,
    resposta_antes,
    pesos,
)

print("Erro", erro)
print("Pesos após o ajuste:", pesos)
print("Resposta da rede após o ajuste:", fazer_previsao(entrada_teste, pesos))