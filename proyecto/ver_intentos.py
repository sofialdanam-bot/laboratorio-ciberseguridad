import sqlite3

conexion = sqlite3.connect("usuarios.db")
cursor = conexion.cursor()

cursor.execute("""
    SELECT id, usuario, fecha_hora, exitoso
    FROM intentos_login
    ORDER BY id DESC
""")

registros = cursor.fetchall()

for registro in registros:
    id_intento, usuario, fecha_hora, exitoso = registro
    estado = "Exitoso" if exitoso == 1 else "Fallido"

    print(f"ID: {id_intento} | Usuario: {usuario} | Fecha: {fecha_hora} | Estado: {estado}")

conexion.close()