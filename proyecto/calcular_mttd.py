import sqlite3
from datetime import datetime, timedelta

conexion = sqlite3.connect("usuarios.db")
cursor = conexion.cursor()

cursor.execute("""
    SELECT usuario, fecha_hora
    FROM intentos_login
    WHERE exitoso = 0
    ORDER BY usuario, fecha_hora
""")

registros = cursor.fetchall()
conexion.close()

intentos_por_usuario = {}

for usuario, fecha_hora in registros:
    fecha = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")

    if usuario not in intentos_por_usuario:
        intentos_por_usuario[usuario] = []

    intentos = intentos_por_usuario[usuario]
    intentos.append(fecha)

    intentos = [
        intento for intento in intentos
        if fecha - intento <= timedelta(minutes=5)
    ]

    intentos_por_usuario[usuario] = intentos

    if len(intentos) == 3:
        inicio = intentos[0]
        deteccion = intentos[2]

        segundos = (deteccion - inicio).total_seconds()

        print(f"Usuario: {usuario}")
        print(f"Inicio de actividad sospechosa: {inicio}")
        print(f"Deteccion simulada: {deteccion}")
        print(f"Tiempo de deteccion: {segundos:.0f} segundos")
        print(f"Tiempo de deteccion: {segundos / 60:.2f} minutos")