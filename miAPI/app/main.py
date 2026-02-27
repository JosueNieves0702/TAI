#importaciones
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import Optional
from pydantic import BaseModel,Field

#instancia
app = FastAPI(
    title = "Mi primer API",
    description= "Joaquin Josue Moreno Nieves",
    version = "1.0"
)

# Habilitar CORS para que el frontend pueda acceder
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#TB ficticia
Usuarios = [
    {"id":1,"nombre":"Diego","edad":21},
    {"id":2,"nombre":"Coral","edad":21},
    {"id":3,"nombre":"Saul","edad":21},
]


class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, description="nombre del usuario")
    edad: int = Field(..., ge=1, le=125, description="edad del usuario")


#endPoints
@app.get("/",tags=['Inicio'])
async def bienvenido():
    return {"mensaje":"Bienvenido a FastAPI"}

@app.get("/holaMundo",tags=['Asincronia'])
async def hola():
    await asyncio.sleep(5)
    return {"mensaje":"Hola Mundo FastAPI",
            "estaus":"200"}

@app.get("/v1/parametroOb/{id}",tags=['Parametro Obligatorio'])
async def ConsultaUno(id:int):

    return {"mensaje":"Usuario Encontrado!!!",
            "Usuario":id,
            "Status":"200"}

@app.get("/v1/parametroOp/",tags=['Parametro Opcional'])
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
    
@app.get("/v1/usuarios/",tags=['CRUD HTTP'])
async def consultaT():
    return {"status":"200",
            "total":len(Usuarios),
            "usuarios":Usuarios}    

@app.post("/v1/usuarios/",tags=['CRUD HTTP'])
async def agregar_usuario(usuario:crear_usuario):
    for user in Usuarios:
        if user["id"] == usuario.id:
            raise HTTPException(
                status_code = 400,
                detail = "El id ya existe" 
            )
    Usuarios.append(usuario.dict())
    return {
        "mensaje":"usuario agregado",
        "Usuario" : usuario,
        "status" : "200"
        }

@app.put("/v1/usuarios/{usuario_id}",tags=['CRUD HTTP'])
async def actualizar_usuario(usuario_id:int, usuario:dict):
    for i, user in enumerate(Usuarios):
        if user["id"] == usuario_id:
            Usuarios[i] = {
                "id": usuario_id,
                "nombre": usuario.get("nombre", user["nombre"]),
                "edad": usuario.get("edad", user["edad"])
            }
            return {
                "mensaje":"usuario actualizado",
                "usuario": Usuarios[i],
                "status" : "200"
            }
    
    raise HTTPException(
        status_code = 404,
        detail = "Usuario no encontrado" 
    )

@app.delete("/v1/usuarios/{usuario_id}",tags=['CRUD HTTP'])
async def eliminar_usuario(usuario_id:int):
    for i, user in enumerate(Usuarios):
        if user["id"] == usuario_id:
            usuario_eliminado = Usuarios.pop(i)
            return {
                "mensaje":"usuario eliminado",
                "usuario": usuario_eliminado,
                "status" : "200"
            }
    
    raise HTTPException(
        status_code = 404,
        detail = "Usuario no encontrado" 
    )

# Endpoint para obtener un usuario específico
@app.get("/v1/usuarios/{usuario_id}",tags=['CRUD HTTP'])
async def obtener_usuario(usuario_id:int):
    for user in Usuarios:
        if user["id"] == usuario_id:
            return {
                "status":"200",
                "usuario":user
            }
    
    raise HTTPException(
        status_code = 404,
        detail = "Usuario no encontrado" 
    )