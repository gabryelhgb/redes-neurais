from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from rede_neural import classificar_perfil, treinar_rede


@asynccontextmanager
async def lifespan(app: FastAPI):
    treinar_rede()
    yield


app = FastAPI(
    title="API do Perceptron Hebb",
    lifespan=lifespan,
)

class DadosPerfil(BaseModel):
    raciocinio_logico: Literal[-1, 1]
    persistente: Literal[-1, 1]
    estudioso: Literal[-1, 1]
    decidido: Literal[-1, 1]

@app.post("/classificar")
def classificar(dados: DadosPerfil):
    caracteristicas = [
        dados.raciocinio_logico,
        dados.persistente,
        dados.estudioso,
        dados.decidido,
    ]

    resposta = classificar_perfil(caracteristicas)

    if resposta == 1:
        perfil = "Sistemas de Informação ou Computação"
    else:
        perfil = "Humanas"

    return {
        "resposta": resposta,
        "perfil": perfil,
    }