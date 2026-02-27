# Mi Proyecto Flask

Un proyecto básico de Flask con estructura estándar.

## Estructura del Proyecto

```
proyecto_f/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias
├── README.md          # Este archivo
├── templates/         # Plantillas HTML
│   └── index.html
└── static/            # Archivos estáticos
    ├── style.css      # Estilos CSS
    └── script.js      # JavaScript del cliente
```

## Instalación

1. Crear un entorno virtual:
```bash
python -m venv venv
```

2. Activar el entorno virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## Rutas Disponibles

- `/` - Página principal
- `/api/hello` - Endpoint API que retorna un mensaje JSON

## Desarrollo

Para agregar nuevas rutas, edita el archivo `app.py` y agrega nuevas funciones decoradas con `@app.route()`.
