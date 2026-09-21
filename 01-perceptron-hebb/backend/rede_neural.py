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

primeira_entrada = entradas[0]
somatorio = calcular_somatoria(primeira_entrada, pesos)

print("Primeira entrada:", primeira_entrada)
print("Somatório:", somatorio)