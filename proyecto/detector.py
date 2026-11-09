
from datetime import datetime, timedelta
from pathlib import Path

FORMATO = "%Y-%m-%d %H:%M:%S"
ARCHIVO_EVENTOS = Path("eventos.log")
ARCHIVO_RESPUESTAS = Path("respuesta.log")

# Tiempo de respuesta simulado para el laboratorio
SEGUNDOS_RESPUESTA = 5


def registrar_respuesta(usuario, fecha_deteccion):
    # Simulamos que la respuesta ocurre 5 segundos
    # después de detectar el incidente.
    fecha_respuesta = fecha_deteccion + timedelta(
        seconds=SEGUNDOS_RESPUESTA
    )

    with open(ARCHIVO_RESPUESTAS, "a", encoding="utf-8") as archivo:
        archivo.write(
            f"{fecha_respuesta.strftime(FORMATO)},"
            f"USUARIO_BLOQUEADO,{usuario}\n"
        )

    mttr = (fecha_respuesta - fecha_deteccion).total_seconds()

    print("Respuesta simulada: usuario bloqueado")
    print("MTTR:", mttr, "segundos")

    return mttr


def analizar_eventos():
    if not ARCHIVO_EVENTOS.exists():
        print("No existe eventos.log")
        return

    intentos = {}
    resultados = []

    with open(ARCHIVO_EVENTOS, "r", encoding="utf-8-sig") as archivo:
        for linea in archivo:
            partes = linea.strip().split(",")

            if len(partes) != 3:
                continue

            fecha_texto, evento, usuario = partes

            try:
                fecha = datetime.strptime(fecha_texto, FORMATO)
            except ValueError:
                continue

            if evento == "LOGIN_CORRECTO":
                intentos[usuario] = []
                continue

            if evento != "LOGIN_FALLIDO":
                continue

            if usuario not in intentos:
                intentos[usuario] = []

            intentos[usuario].append(fecha)

            if len(intentos[usuario]) == 3:
                primero = intentos[usuario][0]
                tercero = intentos[usuario][2]

                mttd = (tercero - primero).total_seconds()

                print("\nALERTA: Posible ataque detectado")
                print("Usuario:", usuario)
                print("Intentos fallidos:", 3)
                print("MTTD:", mttd, "segundos")

                mttr = registrar_respuesta(usuario, tercero)
                resultados.append((mttd, mttr))

                # Reiniciamos el contador para el siguiente escenario
                intentos[usuario] = []

    if resultados:
        promedio_mttd = sum(r[0] for r in resultados) / len(resultados)
        promedio_mttr = sum(r[1] for r in resultados) / len(resultados)

        print("\nRESUMEN DE ESCENARIOS")
        print("Escenarios detectados:", len(resultados))
        print("MTTD promedio:", round(promedio_mttd, 2), "segundos")
        print("MTTR promedio:", round(promedio_mttr, 2), "segundos")
    else:
        print("No se detectaron tres intentos fallidos consecutivos.")


if __name__ == "__main__":
    analizar_eventos()
