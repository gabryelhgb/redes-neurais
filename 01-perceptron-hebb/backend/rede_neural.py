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

def treinar_um_ciclo():
    erros_no_ciclo = 0

    for indice in range(len(entradas)):
        entrada = entradas[indice]
        saida_desejada = saidas_desejadas[indice]
        resposta = fazer_previsao(entrada, pesos)

        erro = atualizar_pesos(
            entrada,
            saida_desejada,
            resposta,
            pesos,
        )

        if erro != 0:
            erros_no_ciclo += 1

    return erros_no_ciclo

erros = treinar_um_ciclo()

print("Erros no ciclo", erros)
print("Pesos após um ciclo:", pesos)