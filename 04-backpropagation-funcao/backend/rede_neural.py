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



def criar_variacoes_zeradas():
    return {
        "v": [0.0] * QUANTIDADE_NEURONIOS_OCULTOS,
        "bias_v": [0.0] * QUANTIDADE_NEURONIOS_OCULTOS,
        "w": [0.0] * QUANTIDADE_NEURONIOS_OCULTOS,
        "bias_w": 0.0,
    }



def treinar_amostra(x, desejado, rede, anteriores, taxa, momento):
    ocultas, previsto = propagar_entrada(x, rede)

    delta_saida = (
        (desejado - previsto)
        * derivada_pela_saida(previsto)
    )

    # Usamos os pesos atuais, antes de atualizar eles.
    deltas_ocultos = []

    for indice in range(QUANTIDADE_NEURONIOS_OCULTOS):
        delta = (
            delta_saida
            * rede["w"][indice]
            * derivada_pela_saida(ocultas[indice])
        )
        deltas_ocultos.append(delta)

    #Agora podemos atualizar os pesos
    for indice in range(QUANTIDADE_NEURONIOS_OCULTOS):
        variacao_w = (
            taxa * delta_saida * ocultas[indice]
            + momento * anteriores["w"][indice]
        )

        variacao_v = (
            taxa * deltas_ocultos[indice] * x
            + momento * anteriores["v"][indice]
        )

        variacao_bias_v = (
            taxa * deltas_ocultos[indice]
            + momento * anteriores["bias_v"][indice]
        )

        rede["w"][indice] += variacao_w
        rede["v"][indice] += variacao_v
        rede["bias_v"][indice] += variacao_bias_v

        # Guardamos os ajustes para a proxima amostra
        anteriores["w"][indice] = variacao_w
        anteriores["v"][indice] = variacao_v
        anteriores["bias_v"][indice] = variacao_bias_v

    variacao_bias_w = (
        taxa * delta_saida
        + momento * anteriores["bias_w"]
    )

    rede["bias_w"] += variacao_bias_w
    anteriores["bias_w"] = variacao_bias_w



def treinar_rede(
        taxa = TAXA_APRENDIZAGEM,
        momento = MOMENTO,
        ciclos = QUANTIDADE_CICLOS,
        limite_pesos = LIMITE_PESOS,
        semente = 42
):
    amostras = gerar_amostras()
    rede = inicializar_rede(limite_pesos, semente)
    anteriores = criar_variacoes_zeradas()

    historico = [calcular_eqm(amostras, rede)]

    for ciclo in range(1, ciclos + 1):
        for x, desejado in amostras:
            treinar_amostra(x, desejado, rede, anteriores, taxa, momento)

        eqm = calcular_eqm(amostras, rede)

        if not math.isfinite(eqm):
            raise ValueError("O treinamento gerou valores inválidos. "
            "Reduza a taxa de aprendizagem ou o momento.")

        historico.append(eqm)

        if ciclo % 5000 == 0:
            print(f"Ciclo {ciclo}: EQM = {eqm:.8f}")

    return rede, historico

if __name__ == "__main__":
    print("Iniciando treinamento...")

    rede, historico = treinar_rede()

    print("\nTreinamento finalizado")
    print("Ciclos:", len(historico) - 1)
    print(f"EQM inicial: {historico[0]:.8f}")
    print(f"EQM final: {historico[-1]:.8f}")

    print("\nComparação de algumas amostras:")
    print("x       desejado   previsto")

    amostras = gerar_amostras()

    for indice in (0, 10, 25, 40, 50, 75, 90, 99):
        x, desejado = amostras[indice]
        _, previsto = propagar_entrada(x, rede)

        print(f"{x:.4f}  {desejado: .5f}   {previsto: .5f}")