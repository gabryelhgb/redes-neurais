from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal

import rede_neural


app = FastAPI(title="API do Perceptron de Diagnóstico")

origens_permitidas = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

@app.post("/treinar")
def treinar():
    rede_neural.pesos = [0, 0, 0, 0, 0]

    ciclos = rede_neural.treinar_rede()

    global treinamento_concluido
    treinamento_concluido = True

    return {
        "mensagem": "Treinamento concluído",
        "ciclos": ciclos,
        "pesos": [round(peso, 2) for peso in rede_neural.pesos],
    }

treinamento_concluido = False


class DadosPaciente(BaseModel):
    febre: Literal[-1, 1]
    nausea: Literal[-1, 1]
    manchas: Literal[-1, 1]
    dor: Literal[-1, 1]


@app.post("/testar")
def testar(dados: DadosPaciente):
    if not treinamento_concluido:
        return {"erro": "Treine a rede antes de testar um paciente."}

    caracteristicas = [
        dados.febre,
        dados.nausea,
        dados.manchas,
        dados.dor,
    ]

    resposta = rede_neural.classificar_paciente(caracteristicas)
    diagnostico = "Doente" if resposta == 1 else "Saudável"

    return {
        "resposta": resposta,
        "diagnostico": diagnostico,
    }