from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import jwt

# Configuraciones OAuth2 y JWT
SECRET_KEY = "tu_clave_secreta_super_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(
    title="Mi API con JWT",
    description="Joaquin Josue Moreno Nieves",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Usuarios = [
    {"id": 1, "nombre": "Diego", "edad": 21},
    {"id": 2, "nombre": "Coral", "edad": 21},
    {"id": 3, "nombre": "Saul", "edad": 21},
]

class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, description="nombre del usuario")
    edad: int = Field(..., ge=1, le=125, description="edad del usuario")

# a. Configuraciones OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# b. Generacion de Tokens (limite 30 min)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoint para login y obtener token
@app.post("/token", tags=['Autenticacion'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "Joaquin Josue" or form_data.password != "123456":
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# c. Implementar validacion de tokens
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Credenciales no autorizadas", headers={"WWW-Authenticate": "Bearer"})
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No cuenta con un token valido o las credenciales no son autorizadas",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/", tags=['Inicio'])
async def bienvenido():
    return {"mensaje": "Bienvenido a FastAPI"}

@app.get("/holaMundo", tags=['Asincronia'])
async def hola():
    await asyncio.sleep(5)
    return {"mensaje": "Hola Mundo FastAPI", "estaus": "200"}

@app.get("/v1/parametroOb/{id}", tags=['Parametro Obligatorio'])
async def ConsultaUno(id: int):
    return {"mensaje": "Usuario Encontrado!!!", "Usuario": id, "Status": "200"}

@app.get("/v1/parametroOp/", tags=['Parametro Opcional'])
async def consultaTodos(id: Optional[int] = None):
    if id is not None:
        for usuarioK in Usuarios:
            if usuarioK["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuarioK, "status": "200"}
        return {"mensaje": "No encontre nada :(", "Status": "200"}
    else:
        return {"mensaje": "No se proporciono una id", "status": "200"}

@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def consultaT():
    return {"status": "200", "total": len(Usuarios), "usuarios": Usuarios}

@app.post("/v1/usuarios/", tags=['CRUD HTTP'])
async def agregar_usuario(usuario: crear_usuario):
    for user in Usuarios:
        if user["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El id ya existe")
    Usuarios.append(usuario.dict())
    return {"mensaje": "usuario agregado", "Usuario": usuario, "status": "200"}

# d. Proteccion de endpoints (PUT y DELETE)
@app.put("/v1/usuarios/{usuario_id}", tags=['CRUD HTTP'])
async def actualizar_usuario(usuario_id: int, usuario: dict, current_user: str = Depends(verificar_token)):
    for i, user in enumerate(Usuarios):
        if user["id"] == usuario_id:
            Usuarios[i] = {
                "id": usuario_id,
                "nombre": usuario.get("nombre", user["nombre"]),
                "edad": usuario.get("edad", user["edad"])
            }
            return {"mensaje": f"usuario actualizado por {current_user}", "usuario": Usuarios[i], "status": "200"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{usuario_id}", tags=['CRUD HTTP'])
async def eliminar_usuario(usuario_id: int, current_user: str = Depends(verificar_token)):
    for i, user in enumerate(Usuarios):
        if user["id"] == usuario_id:
            usuario_eliminado = Usuarios.pop(i)
            return {"mensaje": f"usuario eliminado por {current_user}", "usuario": usuario_eliminado, "status": "200"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.get("/v1/usuarios/{usuario_id}", tags=['CRUD HTTP'])
async def obtener_usuario(usuario_id: int):
    for user in Usuarios:
        if user["id"] == usuario_id:
            return {"status": "200", "usuario": user}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
