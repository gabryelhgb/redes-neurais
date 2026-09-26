from fastapi import FastAPI

app = FastAPI(title="API do Perceptron Hebb")

@app.get("/")
def verificar_servidor():
    return{"status": "online"}