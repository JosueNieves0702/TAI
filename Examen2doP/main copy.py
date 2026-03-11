from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from fastapi.security import HttpBasic, HTTPBasicCredentials
import secrets

año_actual = datetime.now().year 


class turno(BaseModel):
    id: int
    cliente: cliente
    tipo_tramite: Literal["Consulta", "Deposito", "Retiro"] = Field(..., example="Consulta") 
    fecha_turno: datetime = Field(...,) 

class cliente(BaseModel):
    id: int
    nombre: str = Field(..., min_length= 8, description="Nombre del cliente") 
    


app = FastAPI(title="Api de sistema de turnos bancarios") 

lista_turnos = [
    {id: 1, "cliente": {"id": 1, "nombre": "Juan Perez"}, "tipo_tramite": "Consulta", "fecha_turno": datetime(2026, 3, 11, 10, 0)},
    {id: 2, "cliente": {"id": 2, "nombre": "Joaquin Josue"}, "tipo_tramite": "Deposito", "fecha_turno": datetime(2024, 6, 1, 10, 0)},     
] 