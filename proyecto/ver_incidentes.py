import sqlite3

conexion = sqlite3.connect("usuarios.db")
cursor = conexion.cursor()

cursor.execute("""
    SELECT id, usuario, inicio, deteccion, resolucion, accion
    FROM incidentes
    ORDER BY id DESC
""")

for incidente in cursor.fetchall():
    print("ID:", incidente[0])
    print("Usuario:", incidente[1])
    print("Inicio:", incidente[2])
    print("Deteccion:", incidente[3])
    print("Resolucion:", incidente[4])
    print("Accion:", incidente[5])
    print("-------------------------")

conexion.close()