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