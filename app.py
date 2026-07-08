# item3_app.py
import sqlite3
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_NAME = "usuarios_examen.db"

def inicializar_db():
    """Crea la tabla e inserta a los integrantes con contraseñas en hash"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    integrantes_credenciales = [
        ("Cristopher Martinez", "Cisco123!"),
    ]
    
    for nombre, password_plana in integrantes_credenciales:
        hash_pass = generate_password_hash(password_plana)
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", 
                (nombre, hash_pass)
            )
            print(f"[BD] Usuario '{nombre}' insertado exitosamente con hash.")
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "mensaje": "Bienvenido al servicio web del Examen Transversal DRY7122",
        "puerto": 5800
    }), 200

@app.route('/login', methods=['POST'])
def login():
    """Endpoint para validar usuarios mediante JSON payload"""
    datos = request.get_json()
    
    if not datos or 'username' not in datos or 'password' not in datos:
        return jsonify({"status": "error", "mensaje": "Se requieren 'username' y 'password'"}), 400

    username = datos['username']
    password = datos['password']
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE nombre = ?", (username,))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado and check_password_hash(resultado[0], password):
        return jsonify({
            "status": "exito",
            "mensaje": f"Autenticacion exitosa. Bienvenido {username}."
        }), 200
    else:
        return jsonify({
            "status": "fallo",
            "mensaje": "Credenciales inválidas o usuario no encontrado."
        }), 401

if __name__ == '__main__':
    inicializar_db()
    print("\nIniciando servidor web en http://0.0.0.0:5800 ...")
    app.run(host='0.0.0.0', port=5800, debug=True)
