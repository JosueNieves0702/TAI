from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import List, Optional
import asyncio
from models import Libro, Usuario, Prestamo

app = FastAPI(title="API de Biblioteca Digital")

# Base de datos en memoria
libros_db = [
    Libro(id=1, nombre="El Quijote", anio=1605, paginas=863, estado="disponible"),
    Libro(id=2, nombre="Cien años de soledad", anio=1967, paginas=417, estado="disponible"),
    Libro(id=3, nombre="1984", anio=1949, paginas=328, estado="disponible")
]
prestamos_db = []
libro_id_counter = 4
prestamo_id_counter = 1


# Manejador de excepciones para devolver 400 en lugar de 422 cuando faltan datos o son inválidos
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Faltan datos o los datos proporcionados no son válidos", "errors": exc.errors()},
    )


# endPoints
# Endpoint de inicio que devuelve un mensaje de bienvenida
@app.get("/", tags=['Inicio'])
async def bienvenido():
    return {"mensaje": "Bienvenido a FastAPI"}

# a. Registrar un libro
# Endpoint para agregar un nuevo libro a la base de datos en memoria
@app.post("/registrarLibro/", tags=['Libros'])
async def registrar_libro(libro: Libro):
    global libro_id_counter
    libro.id = libro_id_counter
    libros_db.append(libro)
    libro_id_counter += 1
    return {
        "mensaje": "libro registrado",
        "libro": libro,
        "status": "201"
    }

# Endpoint para obtener la lista completa de todos los libros registrados
@app.get("/listaLibros/", tags=['Libros'])
async def consultar_libros():
    return {
        "status": "200",
        "total": len(libros_db),
        "libros": libros_db
    }

# c. Buscar un libro por su nombre
# Endpoint para buscar libros que contengan una cadena de texto específica en su nombre
@app.get("/buscarLibro/", tags=['Libros'])
async def buscar_libro_por_nombre(nombre: str):
    if not nombre or len(nombre) < 2 or len(nombre) > 100:
        raise HTTPException(
            status_code=400, 
            detail="Nombre de libro inválido"
        )
    
    libros_encontrados = [libro for libro in libros_db if nombre.lower() in libro.nombre.lower()]
    return {
        "status": "200",
        "total": len(libros_encontrados),
        "libros": libros_encontrados
    }

# d. Registrar el préstamo de un libro a un usuario
# Endpoint para registrar un nuevo préstamo, cambiando el estado del libro a "prestado"
@app.post("/registrarPrestamo/", tags=['Prestamos'])
async def registrar_prestamo(libro_id: int, usuario: Usuario):
    global prestamo_id_counter
    
    # Buscar el libro
    libro = next((l for l in libros_db if l.id == libro_id), None)
    if not libro:
        raise HTTPException(
            status_code=404, 
            detail="Libro no encontrado"
        )
    
    if libro.estado == "prestado":
        raise HTTPException(
            status_code=409, 
            detail="El libro ya está prestado"
        )
    
    # Cambiar estado del libro
    libro.estado = "prestado"
    
    # Crear registro de préstamo
    prestamo = Prestamo(id=prestamo_id_counter, libro_id=libro_id, usuario=usuario)
    prestamos_db.append(prestamo)
    prestamo_id_counter += 1
    
    return {
        "mensaje": "prestamo registrado",
        "prestamo": prestamo,
        "status": "201"
    }

# e. Marcar un libro como devuelto
# Endpoint para procesar la devolución de un libro, cambiando su estado de vuelta a "disponible"
@app.post("/devolverLibro/{prestamo_id}", tags=['Prestamos'])
async def devolver_libro(prestamo_id: int):
    prestamo = next((p for p in prestamos_db if p.id == prestamo_id), None)
    if not prestamo:
        raise HTTPException(
            status_code=409, 
            detail="El registro de préstamo ya no existe"
        )
    
    libro = next((l for l in libros_db if l.id == prestamo.libro_id), None)
    if libro:
        libro.estado = "disponible"
        
    return {
        "mensaje": "Libro devuelto con éxito",
        "status": "200"
    }

# f. Eliminar el registro de un préstamo
# Endpoint para eliminar el historial de un préstamo específico mediante su ID
@app.delete("/eliminarPrestamo/{prestamo_id}", tags=['Prestamos'])
async def eliminar_prestamo(prestamo_id: int):
    global prestamos_db
    prestamo = next((p for p in prestamos_db if p.id == prestamo_id), None)
    if not prestamo:
        raise HTTPException(
            status_code=404, 
            detail="Préstamo no encontrado"
        )
    
    prestamos_db = [p for p in prestamos_db if p.id != prestamo_id]
    return {
        "mensaje": "Registro de préstamo eliminado",
        "prestamo": prestamo,
        "status": "200"
    }
