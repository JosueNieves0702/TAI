from fastapi import FastAPI
from typing import Optional
app = FastAPI(title = "api de prueba", description = "joaquin josue moreno nieves", version = "1.0")

@app.get("/", tags= ['root'])
def root():
    return {"mensaje": "Bienvenido a la prueba"}

# endpoint que muestra el id ingresada
@app.get("/usuario/{id}", tags= ['usuario'])
def get_usuario_id(id: int):
    return {"mensaje": "id ingresado", "id": id, "status": "200"}

#endpoint de parameto opcional
@app.get("/parametroOpcional/", tags = ['usuario'])
def Consulta_opcional(id: Optional[int] = None):
    if id is not None:
        return {"mensaje": "id ingresado",
                 "id": id,
                 "status": "200"}
    else :
        return {"mensaje": "no se ingreso un id",
                 "status": "200"}
    
#litsta de usuarios
usuarios = [
    {"id": 1, "nombre": "juan", "apellido": "perez"},
    {"id": 2, "nombre": "maria", "apellido": "lopez"},
    {"id": 3, "nombre": "carlos", "apellido": "garcia"}
]
#endoint que muestra la lista de usuarios




