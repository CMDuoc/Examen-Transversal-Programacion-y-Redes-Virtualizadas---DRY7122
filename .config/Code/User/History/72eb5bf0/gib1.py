import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = "usuarios.db"

# --- CONFIGURACIÓN INICIAL DE LA BASE DE DATOS SQLITE ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Crear tabla si no existe para guardar usuarios y claves en texto plano
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credenciales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Insertar los integrantes de la evaluación por defecto (Paso requerido)
    # NOTA: Reemplaza 'Integrante1' e 'Integrante2' por tus nombres reales si lo deseas
    integrantes = [
        ('marcos', 'clave123'),
        ('martinez', 'secreta456')
    ]
    try:
        cursor.executemany('INSERT INTO credenciales (usuario, password) VALUES (?, ?)', integrantes)
        conn.commit()
        print("[DB] Usuarios de la evaluación cargados con éxito.")
    except sqlite3.IntegrityError:
        # Ya estaban creados, no hacemos nada
        pass
    finally:
        conn.close()

# --- RUTA RAÍZ (Primera fase del contenido web) ---
@app.route("/", methods=["GET"])
def index():
    return "Servidor Flask de Control de Credenciales Operativo - Puerto 5000\n"

# --- RUTA DE VERIFICACIÓN DE SESIÓN (Leer parámetros HTTP) ---
@app.route("/login", methods=["POST"])
def login():
    # Leer parámetros de la solicitud HTTP (ya sea por JSON o por Formulario)
    data = request.get_json() if request.is_json else request.form
    
    username = data.get("usuario", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"status": "Error", "message": "Faltan parámetros"}), 400

    # Conectar a la base de datos SQL para verificar credenciales
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM credenciales WHERE usuario = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    # Verificar si el usuario existe y si la contraseña coincide (Texto plano)
    if row and row[0] == password:
        return jsonify({
            "status": "Exitoso",
            "message": f"Bienvenido {username.upper()}. Sesión verificada correctamente."
        }), 200
    else:
        return jsonify({
            "status": "Rechazado",
            "message": "Credenciales inválidas. Intente nuevamente."
        }), 401

if __name__ == "__main__":
    init_db()
    # El sitio web utilizará el puerto 5000 de manera nativa
    app.run(host="0.0.0.0", port=5000, debug=True)