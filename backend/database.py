import sqlite3
from pathlib import Path

import bcrypt

RUTA_DB = Path(__file__).parent / "vitalmonitor.db"


def conectar():
    conexion = sqlite3.connect(RUTA_DB)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    with conectar() as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                correo TEXT NOT NULL UNIQUE,
                contrasena_hash BLOB NOT NULL
            )
        """)


def registrar_usuario(correo, contrasena):
    hash_contrasena = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())
    try:
        with conectar() as conexion:
            conexion.execute(
                "INSERT INTO users (correo, contrasena_hash) VALUES (?, ?)",
                (correo.strip().lower(), hash_contrasena),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def verificar_usuario(correo, contrasena):
    with conectar() as conexion:
        fila = conexion.execute(
            "SELECT contrasena_hash FROM users WHERE correo = ?",
            (correo.strip().lower(),),
        ).fetchone()
    if fila is None:
        return False
    return bcrypt.checkpw(contrasena.encode("utf-8"), fila[0])


if __name__ == "__main__":
    crear_tablas()
    print(registrar_usuario("prueba@correo.com", "MiClave123"))
    print(registrar_usuario("prueba@correo.com", "MiClave123"))
    print(verificar_usuario("prueba@correo.com", "MiClave123"))
    print(verificar_usuario("prueba@correo.com", "otraClave"))