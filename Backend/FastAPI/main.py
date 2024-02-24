from fastapi import FastAPI
from routers import products

app = FastAPI()

# Importar Router
app.include_router(products.router)


@app.get("/")
async def root():
    return "Hola FastAPI"


@app.get("/url")
async def url():
    return {"url": "https://mouredev.com/python"}
