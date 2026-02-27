from pydantic import BaseModel, Field, EmailStr
from typing import Literal, Optional
from datetime import datetime

current_year = datetime.now().year

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del usuario")
    correo: EmailStr = Field(..., description="Correo electrónico válido del usuario")

class Libro(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del libro")
    anio: int = Field(..., gt=1450, le=current_year, description="Año de publicación del libro")
    paginas: int = Field(..., gt=1, description="Número de páginas del libro")
    estado: Literal["disponible", "prestado"] = "disponible"

class Prestamo(BaseModel):
    id: Optional[int] = None
    libro_id: int
    usuario: Usuario
