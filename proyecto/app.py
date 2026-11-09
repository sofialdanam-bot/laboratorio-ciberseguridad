from flask import Flask, render_template, request
import sqlite3
import re
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

@app.route("/")
def inicio():
    return "Laboratorio de Ciberseguridad"

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        correo = request.form.get("correo", "").strip()
        password = request.form.get("password", "")

        if not usuario or not correo or not password:
            return "Todos los campos son obligatorios", 400
        if not re.fullmatch(r"[A-Za-z0-9_]{4,20}", usuario):
            return "Usuario inválido: debe tener entre 4 y 20 caracteres, solo letras, números y guion bajo", 400
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            return "Correo electrónico no válido", 400

        if len(password) < 8:
            return "La contraseña debe tener al menos 8 caracteres", 400
        with sqlite3.connect("usuarios.db") as conexion:
            cursor = conexion.execute(
                """
                SELECT id FROM usuarios
                WHERE usuario = ? OR correo = ?
                LIMIT 1
                """,
                (usuario, correo)
            )

            if cursor.fetchone():
                return "El usuario o correo ya está registrado", 409
        password_segura = generate_password_hash(password)

        with sqlite3.connect("usuarios.db") as conexion:
            conexion.execute(
                "INSERT INTO usuarios (usuario, correo, password) VALUES (?, ?, ?)",
                (usuario, correo, password_segura)
            )

        return "Usuario registrado correctamente"

    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")

        with sqlite3.connect("usuarios.db") as conexion:
            cursor = conexion.execute(
                "SELECT password FROM usuarios WHERE usuario = ? ORDER BY id DESC LIMIT 1",
                (usuario,)
            )
            resultado = cursor.fetchone()

            exitoso = int(
                resultado is not None
                and check_password_hash(resultado[0], password)
            )

            conexion.execute(
                """
                INSERT INTO intentos_login (usuario, fecha_hora, exitoso)
                VALUES (?, datetime('now', 'localtime'), ?)
                """,
                (usuario, exitoso)
            )

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if exitoso:
            evento = "LOGIN_CORRECTO"
        else:
            evento = "LOGIN_FALLIDO"

        with open("eventos.log", "a", encoding="utf-8") as archivo:
            archivo.write(f"{fecha},{evento},{usuario}\n")

        if exitoso:
            return "Inicio de sesión exitoso"

        return "Usuario o contraseña incorrectos", 401

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)