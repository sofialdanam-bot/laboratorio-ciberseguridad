# Laboratorio: Código Seguro y Modelo OWASP

## 1. Datos generales

- **Nombre completo:** Stephanie Sofia Aldana Monico
- **Carné:** 05101230-1
- **Correo institucional:**  sofialdanam@gmail.com
- **Asignatura:** Lenguajes de Programación con Aspectos de Seguridad
- **Fecha:** 08/11/2026

## 2. Descripción

Este laboratorio consiste en desarrollar una aplicación web utilizando Python, implementando controles básicos de seguridad basados en buenas prácticas y el modelo OWASP. Se aplican mecanismos de validación de entradas, consultas parametrizadas, protección de contraseñas, registro de eventos de autenticación y detección de incidentes, incluyendo el cálculo de las métricas MTTD y MTTR.

## 3. Estructura del proyecto

```text
repositorio/
├── proyecto/
│   ├── app.py
│   ├── requirements.txt
│   └── otros archivos
└── README.md
```

## 4. Ejecución del proyecto

**Paso 1.** Clonar el repositorio.

```bash
git clone https://github.com/sofialdanam-bot/laboratorio-ciberseguridad.git
```

**Paso 2.** Ingresar a la carpeta del proyecto.

```bash
cd laboratorio-ciberseguridad/proyecto
```

**Paso 3.** Instalar las dependencias.

```bash
pip install -r requirements.txt
```

**Paso 4.** Crear la base de datos.

```bash
python crearDB.py
```

**Paso 5.** Ejecutar la aplicación web.

```bash
python app.py
```

**Paso 6.** Abrir en el navegador:

http://127.0.0.1:5000

**Paso 7.** Ejecutar el detector de incidentes desde otra terminal, dentro de la carpeta `proyecto`.

```bash
python detector.py
```

## 5. Resultados de las pruebas

Se realizaron tres escenarios de intentos fallidos de inicio de sesión para comprobar la detección de incidentes.

| Escenario | MTTD | MTTR simulado |
|---|---|---|
| 1 | 12 segundos | 5 segundos |
| 2 | 25 segundos | 5 segundos |
| 3 | 20 segundos | 5 segundos |
| **Promedio** | **19 segundos** | **5 segundos** |

El sistema detectó tres escenarios con múltiples intentos fallidos de autenticación y registró respuestas simuladas de bloqueo de usuario.