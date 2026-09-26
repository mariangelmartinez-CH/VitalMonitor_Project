from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

import database

app = FastAPI(title="VitalMonitor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

database.crear_tablas()


class DatosRegistro(BaseModel):
    correo: EmailStr
    contrasena: str = Field(min_length=8, max_length=72)


class DatosLogin(BaseModel):
    correo: EmailStr
    contrasena: str


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
    return {"mensaje": "Inicio de sesion correcto"}