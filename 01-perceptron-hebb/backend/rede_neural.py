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

primeira_entrada = entradas[0]

somatorio = (
    primeira_entrada[0] * pesos[0]
    + primeira_entrada[1] * pesos[1]
    + primeira_entrada[2] * pesos[2]
    + primeira_entrada[3] * pesos[3]
    + primeira_entrada[4] * pesos[4]
)

print("Primeira entrada:", primeira_entrada)
print("Somatório:", somatorio)