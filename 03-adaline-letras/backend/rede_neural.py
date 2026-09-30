letras = ["A", "B", "C", "D", "E", "J", "K"]


quantidade_fontes = 3
quantidade_padroes = quantidade_fontes * len(letras)


linhas_grade = 9
colunas_grade = 7
quantidade_pixels = linhas_grade * colunas_grade
indice_bias = quantidade_pixels
quantidade_entradas = quantidade_pixels + 1


quantidade_neuronios = len(letras)


taxa_aprendizagem = 0.002
erro_minimo = 0.0001
quantidade_maxima_ciclos = 1000


saidas_desejadas = [
    [ 1, -1, -1, -1, -1, -1, -1],  # A
    [-1,  1, -1, -1, -1, -1, -1],  # B
    [-1, -1,  1, -1, -1, -1, -1],  # C
    [-1, -1, -1,  1, -1, -1, -1],  # D
    [-1, -1, -1, -1,  1, -1, -1],  # E
    [-1, -1, -1, -1, -1,  1, -1],  # J
    [-1, -1, -1, -1, -1, -1,  1],  # K
]


pesos = []


for indice_neuronio in range(quantidade_neuronios):
    pesos_do_neuronio = []

    for indice_entrada in range(quantidade_entradas):
        pesos_do_neuronio.append(0.0)

    pesos.append(pesos_do_neuronio)


amostras_treinamento = [
    # Fonte 1: A, B, C, D, E, J, K
    {
        "letra": "A",
        "fonte": 1,
        "grade": [
            [-1, -1, 1, 1, -1, -1, -1],
            [-1, -1, -1, 1, -1, -1, -1],
            [-1, -1, -1, 1, -1, -1, -1],
            [-1, -1, 1, -1, 1, -1, -1],
            [-1, -1, 1, -1, 1, -1, -1],
            [-1, 1, 1, 1, 1, 1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [1, 1, 1, -1, 1, 1, 1],
        ],
    },
    {
        "letra": "B",
        "fonte": 1,
        "grade": [
            [1, 1, 1, 1, 1, 1, -1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, 1, 1, 1, 1, -1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [1, 1, 1, 1, 1, 1, -1],
        ],
    },
    {
        "letra": "C",
        "fonte": 1,
        "grade": [
            [-1, -1, 1, 1, 1, 1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, -1, 1, 1, 1, 1, -1],
        ],
    },
    {
        "letra": "D",
        "fonte": 1,
        "grade": [
            [1, 1, 1, 1, 1, -1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, 1, -1],
            [1, 1, 1, 1, 1, -1, -1],
        ],
    },
    {
        "letra": "E",
        "fonte": 1,
        "grade": [
            [1, 1, 1, 1, 1, 1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, -1],
            [-1, 1, -1, 1, -1, -1, -1],
            [-1, 1, 1, 1, -1, -1, -1],
            [-1, 1, -1, 1, -1, -1, -1],
            [-1, 1, -1, -1, -1, -1, -1],
            [-1, 1, -1, -1, -1, -1, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ],
    },
    {
        "letra": "J",
        "fonte": 1,
        "grade": [
            [-1, -1, -1, 1, 1, 1, 1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
        ],
    },
    {
        "letra": "K",
        "fonte": 1,
        "grade": [
            [1, 1, 1, -1, -1, 1, 1],
            [-1, 1, -1, -1, 1, -1, -1],
            [-1, 1, -1, 1, -1, -1, -1],
            [-1, 1, 1, -1, -1, -1, -1],
            [-1, 1, 1, -1, -1, -1, -1],
            [-1, 1, -1, 1, -1, -1, -1],
            [-1, 1, -1, -1, 1, -1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [1, 1, 1, -1, -1, 1, 1],
        ],
    },
    # Fonte 2: A, B, C, D, E, J, K
    {
        "letra": "A",
        "fonte": 2,
        "grade": [
            [-1, -1, -1, 1, -1, -1, -1],
            [-1, -1, -1, 1, -1, -1, -1],
            [-1, -1, -1, 1, -1, -1, -1],
            [-1, -1, 1, -1, 1, -1, -1],
            [-1, -1, 1, -1, 1, -1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, 1, 1, 1, 1, 1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
        ],
    },
    {
        "letra": "B",
        "fonte": 2,
        "grade": [
            [1, 1, 1, 1, 1, 1, -1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, 1, 1, 1, 1, 1, -1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, 1, 1, 1, 1, 1, -1],
        ],
    },
    {
        "letra": "C",
        "fonte": 2,
        "grade": [
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
        ],
    },
    {
        "letra": "D",
        "fonte": 2,
        "grade": [
            [1, 1, 1, 1, 1, -1, -1],
            [1, -1, -1, -1, -1, 1, -1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, 1, -1],
            [1, 1, 1, 1, 1, -1, -1],
        ],
    },
    {
        "letra": "E",
        "fonte": 2,
        "grade": [
            [1, 1, 1, 1, 1, 1, 1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, 1, 1, 1, 1, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, 1, 1, 1, 1, 1, 1],
        ],
    },
    {
        "letra": "J",
        "fonte": 2,
        "grade": [
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
        ],
    },
    {
        "letra": "K",
        "fonte": 2,
        "grade": [
            [1, -1, -1, -1, -1, 1, -1],
            [1, -1, -1, -1, 1, -1, -1],
            [1, -1, -1, 1, -1, -1, -1],
            [1, -1, 1, -1, -1, -1, -1],
            [1, 1, -1, -1, -1, -1, -1],
            [1, -1, 1, -1, -1, -1, -1],
            [1, -1, -1, 1, -1, -1, -1],
            [1, -1, -1, -1, 1, -1, -1],
            [1, -1, -1, -1, -1, 1, -1],
        ],
    },
    # Fonte 3: A, B, C, D, E, J, K
    {
        "letra": "A",
        "fonte": 3,
        "grade": [
            [-1, -1, -1, 1, -1, -1, -1],
            [-1, -1, -1, 1, -1, -1, -1],
            [-1, -1, 1, -1, 1, -1, -1],
            [-1, -1, 1, -1, 1, -1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, 1, 1, 1, 1, 1, -1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, 1, -1, -1, -1, 1, 1],
        ],
    },
    {
        "letra": "B",
        "fonte": 3,
        "grade": [
            [1, 1, 1, 1, 1, 1, -1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, 1, 1, 1, 1, -1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [1, 1, 1, 1, 1, 1, -1],
        ],
    },
    {
        "letra": "C",
        "fonte": 3,
        "grade": [
            [-1, -1, 1, 1, 1, -1, 1],
            [-1, 1, -1, -1, -1, 1, 1],
            [1, -1, -1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
        ],
    },
    {
        "letra": "D",
        "fonte": 3,
        "grade": [
            [1, 1, 1, 1, 1, -1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, -1, 1, -1],
            [1, 1, 1, 1, 1, -1, -1],
        ],
    },
    {
        "letra": "E",
        "fonte": 3,
        "grade": [
            [1, 1, 1, 1, 1, 1, 1],
            [-1, 1, -1, -1, -1, -1, 1],
            [-1, 1, -1, -1, 1, -1, -1],
            [-1, 1, 1, 1, 1, -1, -1],
            [-1, 1, -1, -1, 1, -1, -1],
            [-1, 1, -1, -1, -1, -1, -1],
            [-1, 1, -1, -1, -1, -1, -1],
            [-1, 1, -1, -1, -1, -1, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ],
    },
    {
        "letra": "J",
        "fonte": 3,
        "grade": [
            [-1, -1, -1, -1, 1, 1, 1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
        ],
    },
    {
        "letra": "K",
        "fonte": 3,
        "grade": [
            [1, 1, 1, -1, -1, 1, 1],
            [-1, 1, -1, -1, -1, 1, -1],
            [-1, 1, -1, -1, 1, -1, -1],
            [-1, 1, -1, 1, -1, -1, -1],
            [-1, 1, 1, -1, -1, -1, -1],
            [-1, 1, -1, 1, -1, -1, -1],
            [-1, 1, -1, -1, 1, -1, -1],
            [-1, 1, -1, -1, -1, 1, -1],
            [1, 1, 1, -1, -1, 1, 1],
        ],
    },
]




def converter_grade_para_entrada(grade, permitir_ruido=False):
    if len(grade) != linhas_grade:
        raise ValueError("A grade precisa ter 9 linhas.")

    entrada = []
    valores_permitidos = (-1, 0, 1) if permitir_ruido else(-1, 1)

    for linha in grade:
        if len(linha) != colunas_grade:
            raise ValueError("Cada linha precisa ter 7 pixels.")

        for pixel in linha:
            if pixel not in valores_permitidos:
                raise ValueError("Pixel inválido na grade.")
            entrada.append(pixel)

    entrada.append(1) # Um único bias por letra
    return entrada




def calcular_saida_linear(entrada, pesos_neuronio):
    if len(entrada) != len(pesos_neuronio):
        raise ValueError("A entrada e os pesos precisam ter o mesmo tamanho.")

    somatorio = 0.0

    for indice in range(len(entrada)):
        somatorio += entrada[indice] * pesos_neuronio[indice]

    return somatorio




def calcular_erro_quadratico_medio(
        entradas_treinamento,
        saidas_treinamento,
        pesos_atuais,
):
    if len(entradas_treinamento) != len(saidas_treinamento):
        raise ValueError("Cada entrada precisa ter uma saída desejada.")

    if len(entradas_treinamento) == 0:
        raise ValueError("A lista de treinamento não pode estar vazia.")

    soma_erros_quadrados = 0.0
    quantidade_respostas = 0

    for indice_padrao in range(len(entradas_treinamento)):
        entrada = entradas_treinamento[indice_padrao]
        saida_desejada = saidas_treinamento[indice_padrao]

        for indice_neuronio in range(len(pesos_atuais)):
            saida_calculada = calcular_saida_linear(
                entrada,
                pesos_atuais[indice_neuronio],
            )

            erro = saida_desejada[indice_neuronio] - saida_calculada
            soma_erros_quadrados += erro ** 2
            quantidade_respostas += 1

    return soma_erros_quadrados / quantidade_respostas




def atualizar_pesos(entrada, saida_desejada, pesos_atuais):
    for indice_neuronio in range(len(pesos_atuais)):
        saida_calculada = calcular_saida_linear(
            entrada,
            pesos_atuais[indice_neuronio],
        )

        erro = saida_desejada[indice_neuronio] - saida_calculada

        for indice_entrada in range(len(entrada)):
            delta_peso = (taxa_aprendizagem * erro * entrada[indice_entrada])

            pesos_atuais[indice_neuronio][indice_entrada] += delta_peso




def preparar_treinamento(amostras):
    entradas_treinamento = []
    saidas_treinamento = []

    for amostra in amostras:
        entrada = converter_grade_para_entrada(amostra["grade"])
        indice_letra = letras.index(amostra["letra"])
        saida_desejada = saidas_desejadas[indice_letra]

        entradas_treinamento.append(entrada)
        saidas_treinamento.append(saida_desejada)

    return entradas_treinamento, saidas_treinamento




def treinar_rede():
    entradas, saidas = preparar_treinamento(amostras_treinamento)

    # Cada treinamento começa novamente com pesos zerados
    for indice_neuronio in range(quantidade_neuronios):
        for indice_entrada in range(quantidade_entradas):
            pesos[indice_neuronio][indice_entrada] = 0.0

    historico_eqm = []

    for ciclo in range(1, quantidade_maxima_ciclos + 1):
        for indice_padrao in range(len(entradas)):
            atualizar_pesos(
                entradas[indice_padrao],
                saidas[indice_padrao],
                pesos,
            )

        eqm = calcular_erro_quadratico_medio(entradas, saidas, pesos)
        historico_eqm.append(eqm)

        if eqm <= erro_minimo:
            break

    return historico_eqm




def reconhecer_grade(grade):
    entrada = converter_grade_para_entrada(grade, permitir_ruido=True)
    letras_reconhecidas = []

    for indice_neuronio in range(quantidade_neuronios):
        saida = calcular_saida_linear(
            entrada,
            pesos[indice_neuronio],
        )

        if saida >= 0:
            letras_reconhecidas.append(letras[indice_neuronio])

    return letras_reconhecidas




if __name__ == "__main__":
    historico_eqm = treinar_rede()

    print("Ciclos:", len(historico_eqm))
    print("EQM final:", historico_eqm[-1])

    acertos = 0

    for amostra in amostras_treinamento:
        resposta = reconhecer_grade(amostra["grade"])
        esperado = [amostra["letra"]]

        print(
            f"Fonte {amostra['fonte']} - "
            f"esperando {amostra['letra']}: {resposta}"
        )

        if resposta == esperado:
            acertos += 1

    print(f"Acertos: {acertos}/{len(amostras_treinamento)}")