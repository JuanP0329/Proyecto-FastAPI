from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import products, users

app = FastAPI()

# Importar Router
app.include_router(products.router)
app.include_router(users.router)

# configuracion de los staticos para exponer img, videos, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return "Hola FastAPI"


@app.get("/url")
async def url():
    return {"url": "https://mouredev.com/python"}
