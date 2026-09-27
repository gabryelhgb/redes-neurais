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

padrao_a_fonte_1 = [
    "...#...",
    "...#...",
    "...#...",
    "..#.#..",
    "..#.#..",
    ".#...#.",
    ".#####.",
    ".#...#.",
    ".#...#.",
]

amostras_treinamento = [
    {
        "letra": "A",
        "fonte": 1,
        "grade": padrao_a_fonte_1,
    }
]


def converter_grade_para_entrada(grade):
    if len(grade) != linhas_grade:
        raise ValueError("A grade precisa ter 9 linhas.")

    entrada = []

    for linha in grade:
        if len(linha) != colunas_grade:
            raise ValueError("Cada linha precisa ter 7 pixels.")

        for pixel in linha:
            if pixel == "#":
                entrada.append(1)
            elif pixel == ".":
                entrada.append(-1)
            else:
                raise ValueError("Use somente '#' e '.' na grade.")

    entrada.append(1)  # bias
    return entrada

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

if __name__ == "__main__":
    print("Letras:", letras)
    print("Quantidade de fontes:", quantidade_fontes)
    print("Padrões de treinamento:", quantidade_padroes)
    print("Pixels por letra:", quantidade_pixels)
    print("Entradas com bias:", quantidade_entradas)
    print("Neurônios de saída:", quantidade_neuronios)
    print("Taxa de aprendizagem:", taxa_aprendizagem)
    print("Erro mínimo:", erro_minimo)
    print("Limite de ciclos:", quantidade_maxima_ciclos)
    print("Saída desejada para A:", saidas_desejadas[0])

    entrada_a = converter_grade_para_entrada(padrao_a_fonte_1)

    print("Linhas da grade:", len(padrao_a_fonte_1))
    print("Pixels na primeira linha:", len(padrao_a_fonte_1[0]))
    print("Tamanho do vetor com bias:", len(entrada_a))
    print("Valor do bias:", entrada_a[indice_bias])

    entradas_treinamento, saidas_treinamento = preparar_treinamento(
        amostras_treinamento
    )

    print("Amostras preparadas:", len(entradas_treinamento))
    print("Tamanho da entrada:", len(entradas_treinamento[0]))
    print("Saída desejada:", saidas_treinamento[0])

    print("Quantidade de neurônios na matriz:", len(pesos))
    print("Pesos por neurônio", len(pesos[0]))
    print("Primeiro peso do neurônio A:", pesos[0][0])
    print("Peso do bias do neurônio A:", pesos[0][indice_bias])