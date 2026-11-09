import sqlite3
from datetime import datetime, timedelta

conexion = sqlite3.connect("usuarios.db")
cursor = conexion.cursor()

inicio = datetime(2026, 11, 8, 19, 1, 9)
deteccion = datetime(2026, 11, 8, 19, 1, 31)

# Simulamos una recuperacion 5 minutos despues de la deteccion
resolucion = deteccion + timedelta(minutes=5)

accion = "Bloqueo temporal de cuenta y revision de intentos fallidos"

cursor.execute("""
INSERT INTO incidentes (usuario, inicio, deteccion, resolucion, accion)
VALUES (?, ?, ?, ?, ?)
""", (
    "prueba123",
    inicio.isoformat(sep=" "),
    deteccion.isoformat(sep=" "),
    resolucion.isoformat(sep=" "),
    accion
))

conexion.commit()

tiempo_respuesta = resolucion - deteccion

print("INCIDENTE REGISTRADO")
print("Usuario: prueba123")
print("Deteccion:", deteccion)
print("Resolucion simulada:", resolucion)
print("Accion:", accion)
print("Tiempo de respuesta:", tiempo_respuesta.total_seconds() / 60, "minutos")

conexion.close()