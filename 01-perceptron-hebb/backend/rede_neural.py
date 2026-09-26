entradas = [
    [1, 1, 1, 1, 1],
    [-1, 1, -1, -1, 1],
    [1, 1, 1, -1, 1],
    [1, -1, -1, 1, 1],
]

saidas_desejadas = [1, 1, -1, -1]

pesos = [0, 0, 0, 0, 0]

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

def calcular_erro(saida_desejada, resposta_rede):
    erro = saida_desejada - resposta_rede
    return erro

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

def treinar_rede():
    ciclos = 0
    limite_ciclos = 100

    while True:
        ciclos += 1

        erros_no_ciclo = treinar_um_ciclo()

        print("Ciclo:", ciclos)
        print("Erros no ciclo:", erros_no_ciclo)
        print("Pesos atuais:", pesos)
        print()

        if erros_no_ciclo == 0:
            break

        if ciclos >= limite_ciclos:
            print("Limite de ciclos atingido. A rede não convergiu.")
            break

    return ciclos

def verificar_rede():
    acertos = 0

    for indice in range(len(entradas)):
        entrada = entradas[indice]
        saida_desejada = saidas_desejadas[indice]

        resposta = fazer_previsao(entrada, pesos)
        erro = calcular_erro(saida_desejada, resposta)

        if erro == 0:
            acertos += 1

        print("Padrao:", indice + 1)
        print("Saida desejada:", saida_desejada)
        print("Resposta da rede", resposta)
        print("Erro:", erro)
        print()

    return acertos

def classificar_perfil(caracteristicas):
    entrada = caracteristicas + [1]
    resposta = fazer_previsao(entrada, pesos)

    return resposta

def testar_novo_perfil():
    print("Digite 1 para sim e -1 para não")

    raciocinio_logico = int(input("Raciocínio lógico: "))
    persistente = int(input("Persistente: "))
    estudioso = int(input("Estudioso: "))
    dicidido = int(input("Decidido: "))

    caracteristicas = [
        raciocinio_logico,
        persistente,
        estudioso,
        dicidido,
    ]

    entrada_teste = caracteristicas + [1]
    resposta = classificar_perfil(caracteristicas)

    print()
    print("Entrada de teste:", entrada_teste)
    print("Resposta da rede:", resposta)

    if resposta == 1:
        print("Perfil compatível com Sistemas de Informação ou Computação.")
    else:
        print("Perfil compatível com Humanas.")

def main():
    print("\n=== Treinamento ===")
    quantidade_ciclos = treinar_rede()

    print("Treinamento Finalizado")
    print("\n=== Resultado final ===")
    print("Quantidade de ciclos:", quantidade_ciclos)
    print("Pesos finais:", pesos)

    acertos = verificar_rede()

    print("Quantidade de acertos:", acertos)
    print("Quantidade de padrões:", len(entradas))

    print("\n=== Teste de novo perfil ===")
    testar_novo_perfil()

if __name__=="__main__":
    main()