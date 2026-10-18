import math
import random

QUANTIDADE_AMOSTRAS = 100
QUANTIDADE_NEURONIOS_OCULTOS = 10

TAXA_APRENDIZAGEM = 0.5
MOMENTO = 0.05
QUANTIDADE_CICLOS = 35000

LIMITE_PESOS = 1 / 3



def funcao_alvo(x):
    return math.sin(x) * math.sin(2 * x)



def gerar_amostras():
    amostras = []

    for indice in range(QUANTIDADE_AMOSTRAS):
        x = indice * (2 * math.pi) / QUANTIDADE_AMOSTRAS
        desejado = funcao_alvo(x)

        amostras.append((x, desejado))
    return amostras



def funcao_ativacao(valor):
    if valor >= 0:
        return 2 / (1 + math.exp(-valor)) - 1

    exponencial = math.exp(valor)
    return (exponencial - 1) / (exponencial + 1)



def derivada_pela_saida(saida):
    return 0.5 * (1 + saida) * (1 - saida)



def inicializar_rede(limite_pesos=LIMITE_PESOS, semente=42):
    sorteador = random.Random(semente)

    rede = {
        "v": [],
        "bias_v": [],
        "w": [],
        "bias_w": 0.0,
    }

    for __ in range(QUANTIDADE_NEURONIOS_OCULTOS):
        rede["v"].append(sorteador.uniform(-limite_pesos, limite_pesos))
        rede["bias_v"].append(sorteador.uniform(-limite_pesos, limite_pesos))
        rede["w"].append(sorteador.uniform(-limite_pesos, limite_pesos))

    rede["bias_w"] = sorteador.uniform(-limite_pesos, limite_pesos)
    return rede



def propagar_entrada(x, rede):
    saidas_ocultas = []

    for indice in range(QUANTIDADE_NEURONIOS_OCULTOS):
        soma = (
            x * rede["v"][indice]
            + rede["bias_v"][indice]
        )

        saidas_ocultas.append(funcao_ativacao(soma))

    soma_saida = rede["bias_w"]

    for indice in range(QUANTIDADE_NEURONIOS_OCULTOS):
        soma_saida += saidas_ocultas[indice] * rede["w"][indice]

    saida = funcao_ativacao(soma_saida)
    return saidas_ocultas, saida



def calcular_eqm(amostras, rede):
    soma_erros = 0.0

    for x, desejado in amostras:
        _, previsto = propagar_entrada(x, rede)
        soma_erros += (desejado - previsto) ** 2

    return soma_erros / len(amostras)



if __name__ == "__main__":
    amostras = gerar_amostras()
    rede = inicializar_rede()

    ocultas, previsao = propagar_entrada(amostras[25][0], rede)

    print("Amostras: ", len(amostras))
    print("Primeiro x: ", amostras[0][0])
    print("Último x: ", amostras[-1][0])
    print("Neurônios ocultos: ", len(ocultas))

    quantidade_parametros = (
        len(rede["v"])
        + len(rede["bias_v"])
        + len(rede["w"])
        + 1 # bias_w
    )

    print("Parâmetros ajustáveis: ", quantidade_parametros)
    print("Ativação em zero: ", funcao_ativacao(0))
    print("Derivada em zero: ", derivada_pela_saida(0))
    print("Previsão antes do treino: ", previsao)
    print("EQM antes do treino: ", calcular_eqm(amostras, rede))