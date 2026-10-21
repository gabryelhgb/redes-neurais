# Redes Neurais

Projeto acadêmico de Inteligência Artificial com quatro exercícios de redes neurais. A lógica de treinamento e classificação foi implementada manualmente em Python, sem NumPy ou bibliotecas prontas de aprendizado de máquina. As interfaces foram desenvolvidas em Next.js.

## Exercícios

### 01 — Perceptron com Regra de Hebb

Um neurônio recebe quatro características de um aluno e classifica seu perfil como compatível com Computação/Sistemas de Informação ou Humanas. O treinamento é supervisionado e ajusta os pesos pela Regra de Hebb apresentada em aula.

### 02 — Perceptron para diagnóstico

Reaproveita a estrutura do primeiro exercício com novos dados de treinamento. O perceptron analisa quatro características de pacientes fictícios e produz uma classificação entre “Doente” e “Saudável”. Os pesos são ajustados com uma taxa de aprendizagem.

### 03 — Adaline para reconhecimento de letras

Uma rede com sete neurônios reconhece as letras A, B, C, D, E, J e K. O treinamento usa três fontes para cada letra, totalizando 21 padrões em grades de 9 × 7 pixels. A atualização dos pesos usa o erro da saída linear; o treinamento acompanha o erro quadrático médio (EQM) até atingir o critério de parada ou o limite de ciclos. A interface permite selecionar uma amostra ou desenhar uma letra clicando e arrastando pelos pixels, além de exibir a curva do EQM.

### 04 — Aproximação de função com Backpropagation

Rede neural com uma entrada, dez neurônios ocultos e uma saída para aproximar a função f(x) = sen(x) × sen(2x). O algoritmo foi implementado manualmente em Python, com atualização dos pesos por backpropagation e momento.

Foram realizados 16 testes comparando taxa de aprendizagem, momento, intervalo dos pesos iniciais, quantidade de ciclos e sementes. A interface exibe a função real, a previsão da rede, o histórico do EQM e os pesos finais.

Os resultados, a planilha e o relatório estão em `04-backpropagation-funcao/docs/`. O menor EQM de treinamento observado foi aproximadamente 0,000385. Esse valor não representa percentual de acerto nem avaliação em dados inéditos.

## Estrutura

Cada exercício possui um `backend` em Python e um `frontend` em Next.js:

- `01-perceptron-hebb/`
- `02-perceptron-diagnostico/`
- `03-adaline-letras/`
- `04-backpropagation-funcao/`

As bibliotecas usadas para a API e a interface não implementam a matemática das redes neurais: somas, previsões, cálculo do erro e atualização dos pesos estão no código Python do projeto.