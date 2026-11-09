from flask import Flask, render_template, request
import sqlite3
import re
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

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            return "Correo electrónico no válido", 400

        if len(password) < 8:
            return "La contraseña debe tener al menos 8 caracteres", 400

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

        if exitoso:
            return "Inicio de sesión exitoso"

        return "Usuario o contraseña incorrectos", 401

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)