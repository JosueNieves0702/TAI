FROM python:3.12-slim

#creamos carpeta de trabajo del contenedor
WORKDIR /app

#copiamos los requerimientos del servidor
COPY requirements.txt .

#instalamos los requerimientos
RUN pip install --no-cache-dir -r requirements.txt

#copiar el codigo de API
COPY . .

#exponer el puerto
EXPOSE 8000

#comando de ejecuccion FASTAPI
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000","--reload"]
