import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field

import database

load_dotenv()

CLAVE_SECRETA = os.environ["JWT_SECRET"]
ALGORITMO = "HS256"
MINUTOS_DE_VIDA = 60

app = FastAPI(title="VitalMonitor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

database.crear_tablas()

esquema = HTTPBearer()


class DatosRegistro(BaseModel):
    correo: EmailStr
    contrasena: str = Field(min_length=8, max_length=72)


class DatosLogin(BaseModel):
    correo: EmailStr
    contrasena: str


def crear_token(correo):
    vence = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_DE_VIDA)
    return jwt.encode({"sub": correo, "exp": vence}, CLAVE_SECRETA, algorithm=ALGORITMO)


def usuario_actual(credenciales: HTTPAuthorizationCredentials = Depends(esquema)):
    try:
        datos = jwt.decode(credenciales.credentials, CLAVE_SECRETA, algorithms=[ALGORITMO])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Sesion invalida o vencida")
    return datos["sub"]


@app.get("/api/salud")
def estado():
    return {"estado": "ok", "mensaje": "El backend esta funcionando"}


@app.post("/api/registro", status_code=201)
def registro(datos: DatosRegistro):
    if not database.registrar_usuario(datos.correo, datos.contrasena):
        raise HTTPException(status_code=409, detail="Ese correo ya esta registrado")
    return {"mensaje": "Usuario creado"}


@app.post("/api/login")
def login(datos: DatosLogin):
    if not database.verificar_usuario(datos.correo, datos.contrasena):
        raise HTTPException(status_code=401, detail="Correo o contrasena incorrectos")
    return {"token": crear_token(datos.correo.strip().lower())}


@app.get("/api/yo")
def perfil(correo: str = Depends(usuario_actual)):
    return {"correo": correo}