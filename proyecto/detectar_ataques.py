import sqlite3
from datetime import datetime, timedelta
def registrar_respuesta(usuario, fecha_deteccion):
    fecha_respuesta = datetime.now()

    with open("respuesta.log", "a", encoding="utf-8") as archivo:
        archivo.write(
            f"{fecha_respuesta:%Y-%m-%d %H:%M:%S},"
            f"USUARIO_BLOQUEADO,{usuario}\n"
        )

    mttr = (fecha_respuesta - fecha_deteccion).total_seconds()

    print("Respuesta simulada: usuario bloqueado")
    print("MTTR:", mttr, "segundos")
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

alertas = 0
usuarios = {}

for usuario, fecha_hora in registros:
    fecha = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")

    if usuario not in usuarios:
        usuarios[usuario] = []

    usuarios[usuario].append(fecha)

    recientes = [
        intento for intento in usuarios[usuario]
        if fecha - timedelta(minutes=5) <= intento <= fecha
    ]

    usuarios[usuario] = recientes

    if len(recientes) == 3:
        alertas += 1
        print(f"ALERTA: Posible ataque contra {usuario}")
        print(f"Detectado: {fecha_hora}")
        print("Motivo: 3 intentos fallidos en 5 minutos")

if alertas == 0:
    print("No se detectaron ataques sospechosos.")