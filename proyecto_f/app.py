from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('usuarios'))

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@app.route('/api/hello')
def hello():
    return {'message': 'Hello from Flask!'}

# Proxy para redirigir solicitudes a miAPI si es necesario
@app.route('/api/usuarios', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/usuarios/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/usuarios/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_usuarios(path):
    """Proxy que redirige las solicitudes a la API de miAPI incluyendo subpaths/IDs"""
    try:
        api_base = 'http://localhost:8000/v1/usuarios/'
        target_url = api_base + path

        if request.method == 'GET':
            response = requests.get(target_url, params=request.args)
        elif request.method == 'POST':
            response = requests.post(target_url, json=request.get_json())
        elif request.method == 'PUT':
            response = requests.put(target_url, json=request.get_json())
        elif request.method == 'DELETE':
            response = requests.delete(target_url)

        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
