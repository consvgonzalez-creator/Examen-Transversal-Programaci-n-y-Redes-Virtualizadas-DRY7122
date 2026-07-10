import sqlite3
import hashlib
from flask import Flask, request, render_template_string

app = Flask(__name__)

def inicializar_bd():
    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    integrantes = [
        ("Constanza Gonzalez", "clave123"),
        ("Yo y mi otro Yol", "prueba456"),
    ]
    
    for nombre, password in integrantes:
        hash_pw = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor.execute('INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)', (nombre, hash_pw))
        except sqlite3.IntegrityError:
            pass
            
    conexion.commit()
    conexion.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje = ""
    if request.method == 'POST':
        usuario_ingresado = request.form.get('usuario')
        password_ingresada = request.form.get('password')
        
        hash_ingresado = hashlib.sha256(password_ingresada.encode()).hexdigest()
        
        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT password_hash FROM usuarios WHERE nombre = ?', (usuario_ingresado,))
        resultado = cursor.fetchone()
        conexion.close()
        
        if resultado and resultado[0] == hash_ingresado:
            mensaje = f"¡Validación exitosa! Bienvenido al sistema, {usuario_ingresado}."
        else:
            mensaje = "Error: Usuario o contraseña incorrectos."

    html_template = '''
    <!DOCTYPE html>
    <html>
    <head><title>Validación de Integrantes</title></head>
    <body style="font-family: Arial, sans-serif; margin: 40px;">
        <h2>Login - Examen Transversal</h2>
        <form method="POST">
            <label>Nombre del Integrante:</label><br>
            <input type="text" name="usuario" required><br><br>
            <label>Contraseña:</label><br>
            <input type="password" name="password" required><br><br>
            <button type="submit">Validar Usuario</button>
        </form>
        <br>
        <h3 style="color: #333;">{{ mensaje }}</h3>
    </body>
    </html>
    '''
    return render_template_string(html_template, mensaje=mensaje)

if __name__ == '__main__':
    inicializar_bd()
    print("Base de datos lista. Iniciando el servidor en el puerto 7500...")
    app.run(port=7500)
