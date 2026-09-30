from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import rede_neural


app = FastAPI(title="API Adaline - Reconhecimento de Letras")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

treinamento_concluido = False


class DadosTeste(BaseModel):
    grade: list[list[int]]


@app.get("/amostras")
def listar_amostras():
    return {
        "letras": rede_neural.letras,
        "fontes": [1, 2, 3],
        "amostras": rede_neural.amostras_treinamento,
    }


@app.post("/treinar")
def treinar():
    global treinamento_concluido

    treinamento_concluido = False
    historico_eqm = rede_neural.treinar_rede()
    variacao_final = abs(historico_eqm[-1] - historico_eqm[-2])
    treinamento_concluido = True

    return {
        "ciclos": len(historico_eqm) - 1,
        "eqm_final": historico_eqm[-1],
        "convergiu": variacao_final <= rede_neural.erro_minimo,
        "historico_eqm": historico_eqm,
    }


@app.post("/testar")
def testar(dados: DadosTeste):
    if not treinamento_concluido:
        raise HTTPException(
            status_code=409,
            detail="Treine a rede antes de testar uma letra.",
        )

    try:
        resposta = rede_neural.reconhecer_grade(dados.grade)
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro)) from erro

    return {"letras_reconhecidas": resposta}