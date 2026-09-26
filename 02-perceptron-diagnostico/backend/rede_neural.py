nomes_pacientes = [
    "João",
    "Pedro",
    "Maria",
    "José",
    "Ana",
    "Leila",
]

entradas = [
    [1, 1, 1, 1, 1],     # João
    [-1, -1, -1, -1, 1], # Pedro
    [1, 1, 1, -1, 1],    # Maria
    [1, -1, -1, 1, 1],   # José
    [1, -1, 1, 1, 1],    # Ana
    [-1, -1, -1, 1, 1],  # Leila
]

saidas_desejadas = [1, -1, -1, 1, -1, 1]

pesos = [0, 0, 0, 0, 0]
taxa_aprendizagem = 0.02

print("Quantidade de pacientes: ", len(entradas))
print("Quantidade de saídas: ", len(saidas_desejadas))
print("Pesos iniciais: ", pesos)
print("Taxa de aprendizagem: ", taxa_aprendizagem)

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
    return funcao_ativacao(somatorio)


def treinar_rede():
    ciclos = 0
    tem_erro = True

    while tem_erro:
        tem_erro = False

        for indice in range(len(entradas)):
            entrada = entradas[indice]
            saida_desejada = saidas_desejadas[indice]
            resposta = fazer_previsao(entrada, pesos)

            erro = saida_desejada - resposta

            if erro != 0:
                tem_erro = True

            for indice_peso in range(len(pesos)):
                delta_peso = (
                    entrada[indice_peso]
                    * erro
                    * taxa_aprendizagem
                )
                pesos[indice_peso] += delta_peso

        ciclos += 1

    return ciclos


ciclos = treinar_rede()

print("Ciclos até convergência:", ciclos)
print("Pesos finais:", [round(peso, 2) for peso in pesos])