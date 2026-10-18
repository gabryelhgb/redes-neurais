from time import perf_counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import rede_neural


app = FastAPI(title="API Backpropagation - Aproximação de função", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class ConfiguracaoTreino(BaseModel):
    taxa: float = Field(
        default=rede_neural.TAXA_APRENDIZAGEM,
        gt=0,
        allow_inf_nan=False,
    )

    momento: float = Field(
        default=rede_neural.MOMENTO,
        ge=0,
        lt=1,
    )

    ciclos: int = Field(
        default=rede_neural.QUANTIDADE_CICLOS,
        gt=0,
    )

    limite_pesos: float = Field(
        default=rede_neural.LIMITE_PESOS,
        gt=0,
        allow_inf_nan=False,
    )

    semente: int = 42



@app.get("/amostras")
def listar_amostras():
    return {
        "amostras": [
            {"x": x, "desejado": desejado}
            for x, desejado in rede_neural.gerar_amostras()
        ]
    }



@app.post("/treinar")
def treinar(config: ConfiguracaoTreino):
    inicio = perf_counter()

    try:
        rede, historico = rede_neural.treinar_rede(
            **config.model_dump()
        )
    except (ValueError, OverflowError) as erro:
        raise HTTPException(
            status_code=422,
            detail=(
                "Não foi possível treinar a rede com esses parâmetros. "
                "Reduza a taxa, o momento ou limite dos pesos. "
            ),
        ) from erro

    comparacao = []

    for x, desejado in rede_neural.gerar_amostras():
        _, previsto = rede_neural.propagar_entrada(x, rede)

        comparacao.append({
            "x": x,
            "desejado": desejado,
            "previsto": previsto,
        })

    return {
        "parametros": config.model_dump(),
        "ciclos": len(historico) - 1,
        "eqm_inicial": historico[0],
        "eqm_final": historico[-1],
        "historico_eqm": historico,
        "comparacao": comparacao,
        "pesos": rede,
        "tempo_segundos": perf_counter() - inicio,
    }