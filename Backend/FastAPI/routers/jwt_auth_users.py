from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN__DURATION = 1
SECRET = "5649979124c93afae2c115a477d7c91f78cb5a07936f2e76c0e073b86a9ab41f"

router = APIRouter(prefix="/v2")

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "JuanP": {
        "username": "JuanP",
        "full_name": "Juan Pérez",
        "email": "juanp@example.com",
        "disabled": False,
        "password": "$2a$12$b65tg8/qGvpEBdtuetSpnOVIhmF3DcpUsxn0jYubOnoLo33Uzi6YO",
    },
    "AnaM": {
        "username": "AnaM",
        "full_name": "Ana Martinez",
        "email": "AnaM@example.com",
        "disabled": False,
        "password": "$2a$12$RXanmB6/oXQThIlGdVcNKurIFD/XGGJzJWeG6ifMVVyhzLdPLNqKu",
    },
}


def serch_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def serch_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticacion invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return serch_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUESTHTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
        )

    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto"
        )

    user = serch_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta",
        )

    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN__DURATION),
    }

    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer",
    }


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
