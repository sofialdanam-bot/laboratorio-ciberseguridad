import sqlite3

conexion = sqlite3.connect("usuarios.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    correo TEXT,
    password TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS intentos_login (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    fecha_hora TEXT NOT NULL,
    exitoso INTEGER NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS incidentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    inicio TEXT NOT NULL,
    deteccion TEXT NOT NULL,
    resolucion TEXT,
    accion TEXT
)
""")
conexion.commit()
conexion.close()

print("Base de datos y tabla creadas correctamente.")