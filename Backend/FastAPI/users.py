from fastapi import FastAPI
from pydantic import  BaseModel

app = FastAPI()

#Entidad User
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [
    User(id=1, name="Juan", surname="Pablo", url="https://Juan.dev", age=28),
    User(id=2, name="Ana", surname="Maria", url="https://Amaria.co", age=26),
    User(id=3, name="Joy", surname="Steven", url="https://Steven.es", age=18),
]


@app.get("/usersjson")
async def usersjson():
    return [
        {"name": "Juan", "surname": "Pablo", "url": "https://Juan.dev", "age": 28},
        {"name": "Ana", "surname": "Maria", "url": "https://Amaria.co", "age": 26},
        {"name": "Joy", "surname": "Steven", "url": "https://Steven.es", "age": 18},
    ]

@app.get("/users")
async def users():
    return users_list