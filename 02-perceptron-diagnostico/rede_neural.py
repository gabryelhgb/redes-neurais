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