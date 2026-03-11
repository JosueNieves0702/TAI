from fastapi import FastAPI, HTTPException, status
from typing import List, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

año_actual = datetime.now().year 

#modelos
class cliente(BaseModel):
    id: int
    nombre: str = Field(..., min_length= 8, description="Nombre del cliente")

class turno(BaseModel):
    id: int
    cliente: cliente
    tipo_tramite: Literal["Consulta", "Deposito", "Retiro"] = Field(..., description= "tipo de tramites: deposito, retiro o consulta" )
    fecha_turno: datetime = Field(..., description="Fecha y hora del turno futura entre las 9 am y 3 pm")
    status: Literal["Pendiente", "Atendido"] = Field(default="Pendiente", description="Estado del turno: Pendiente o Atendido")
    
app = FastAPI(title="Api de sistema de turnos bancarios.") 

lista_turnos = [
    turno(id=1, cliente=cliente(id=1, nombre="Juan Perez"), tipo_tramite="Consulta", fecha_turno=datetime(2026, 4, 11, 10, 0)),
    turno(id=2, cliente=cliente(id=2, nombre="Joaquin Josue"), tipo_tramite="Deposito", fecha_turno=datetime(2026, 4, 11, 10, 0)),
] 

@app.post("/turnos", status_code=status.HTTP_201_CREATED, tags=["Turnos"])  
def create_turno(turno: turno):
    turnos_cliente = [t for t in lista_turnos if t.cliente.id == turno.cliente.id]
    if len(turnos_cliente) >= 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El cliente ya tiene 5 turnos asignados")
    if turno.fecha_turno < datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La fecha del turno debe ser futura")
    if turno.fecha_turno.hour < 9 or turno.fecha_turno.hour >= 15:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La fecha del turno debe estar entre las 9 am y 3 pm")
    lista_turnos.append(turno)
    return {"message": "Turno creado exitosamente", "turno": turno}


@app.get("/listaTurnos", response_model=List[turno], tags=["Turnos"])
def list_turnos():
    return {"mensaje": "Lista de turnos", "turnos": lista_turnos, "status": status.HTTP_200_OK}



@app.get("/turnos/{turno_id}", response_model=turno, tags=["Turnos"])
def get_turno(turno_id: int):
    for turno in lista_turnos:
        if turno.id == turno_id:
            return {"mensaje": "turno encontrado","turno": turno, "status": status.HTTP_200_OK}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Turno no encontrado")



security = HTTPBasic()


@app.put("/turnos/{turno_id}/atender", tags=["Turnos"])
def atender_turno(turno_id: int, credentials: HTTPBasicCredentials = security):
    correct_username = secrets.compare_digest(credentials.username, "banco")
    correct_password = secrets.compare_digest(credentials.password, "24468")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")  
    
    for turno in lista_turnos:
        if turno.id == turno_id:
            if turno.status == "Atendido":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El turno ya ha sido atendido")
            turno.status = "Atendido"
            return {"mensaje": "Turno marcado como atendido", "turno": turno, "status": status.HTTP_200_OK}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Turno no encontrado") 


@app.delete("/turnos/{turno_id}", tags=["Turnos"])
def eliminar_turno(turno_id: int, credentials: HTTPBasicCredentials = security):
    correct_username = secrets.compare_digest(credentials.username, "banco")
    correct_password = secrets.compare_digest(credentials.password, "24468")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")  
    
    for turno in lista_turnos:
        if turno.id == turno_id:
            lista_turnos.remove(turno)
            return {"mensaje": "Turno eliminado exitosamente", "status": status.HTTP_200_OK}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Turno no encontrado")


