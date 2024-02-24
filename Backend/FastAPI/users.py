from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Entidad User
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


# Parametros por PATH
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)


# Parametros por QUERY
@app.get("/user/")
async def user(id: int):
    return search_user(id)


@app.post("/user/", status_code=201)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        return {"error": "El usuario ya Existe"}
    else:
        users_list.append(user)


@app.put("/user/")
async def update_user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "Usuario no Actualizado"}
    else:
        return user


@app.delete("/user/{id}")
async def delete_user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "No se ha eliminado el usuario"}


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el Usuario"}
