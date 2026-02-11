#importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

#instancia
app = FastAPI(
    title = "Mi primer API",
    description= "Joaquin Josue Moreno Nieves",
    version = "1.0"
)

#TB ficticia
Usuarios = [
    {"id":1,"nombre":"Diego","edad":21},
    {"id":2,"nombre":"Coral","edad":21},
    {"id":3,"nombre":"Saul","edad":21},
]


#endPoints
@app.get("/",tags=['Inicio'])
async def bienvenido():
    return {"mensaje":"Bienvenido a FastAPI"}

@app.get("/holaMundo",tags=['Asincronia'])
async def hola():
    await asyncio.sleep(5)
    return {"mensaje":"Hola Mundo FastAPI",
            "estaus":"200"}

@app.get("/v1/usuario/{id}",tags=['Parametro Obligatorio'])
async def ConsultaUno(id:int):

    return {"mensaje":"Usuario Encontrado!!!",
            "Usuario":id,
            "Status":"200"}

@app.get("/v1/usuarios/",tags=['Parametro Opcional'])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuarioK in Usuarios:
            if usuarioK["id"] == id:
                return {"mensaje":"usuario encontrado",
                        "usuario":usuarioK,
                        "status":"200"}

        return {"mensaje":"No encontre nada :(",
                "Status":"200"}

    else:
        return {"mensaje": "No se proporciono una id",
                "status":"200"}

