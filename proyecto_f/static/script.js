function fetchHello() {
    fetch('/api/hello')
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').textContent = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response').textContent = 'Error al llamar la API';
        });
}
