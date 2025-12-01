Automatización de Captura de Facturas XML (CFDI 3.3 / 4.0)
Python + Tkinter + PostgreSQL

Este proyecto es una herramienta desarrollada en Python que permite:

✔ Leer uno o varios XML de facturas CFDI
✔ Parsear su contenido (emisor, receptor, UUID, conceptos, totales, IVA, descuentos)
✔ Validar la estructura
✔ Guardar la información automáticamente en PostgreSQL
✔ Proveer una interfaz gráfica sencilla con Tkinter

🚀 Objetivo

Eliminar la captura manual en el área contable y reducir errores de transcripción, optimizando tiempos y garantizando una base de datos confiable para reportes.

🧰 Tecnologías utilizadas

Python 3

Tkinter (interfaz gráfica)
<p align="center">
  <img src="logo.png" width="200">
</p>

xml.etree.ElementTree para parseo de XML

psycopg2 para conexión a PostgreSQL

PostgreSQL

requirements.txt para dependencias

📁 Estructura del proyecto
xml_facturas_automacion/
│
├── app_xml.py              # Interfaz y lógica principal
├── parser_xml.py           # Funciones de lectura y parseo de XML
├── db_connection.py        # Conexión a PostgreSQL (sin datos sensibles)
├── README.md               # Documentación del proyecto

🧩 Ejemplo de código
Extracción básica del XML:
import xml.etree.ElementTree as ET

def leer_xml(ruta):
    tree = ET.parse(ruta)
    root = tree.getroot()
    ns = {"cfdi": "http://www.sat.gob.mx/cfd/4"}

    emisor = root.find("cfdi:Emisor", ns).attrib.get("Nombre")
    receptor = root.find("cfdi:Receptor", ns).attrib.get("Nombre")
    total = root.attrib.get("Total")

    return {
        "emisor": emisor,
        "receptor": receptor,
        "total": total
    }

🗄 Conexión a PostgreSQL (sin datos sensibles)
import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

▶ Cómo ejecutar el proyecto

Clona el repo:

git clone [https://github.com/chalonso/Ing.-Ciencia-de-datos-.git](https://github.com/chalonso/Ing.-Ciencia-de-datos-/tree/main/xml_facturas_automacion)


Instala dependencias:

pip install -r requirements.txt


Configura tus variables de entorno:

DB_HOST=localhost
DB_NAME=mi_base
DB_USER=postgres
DB_PASS=*****


Ejecuta la app:

python app_xml.py

📌 Notas importantes

No se incluyen credenciales ni rutas reales.

Los XML de ejemplo no contienen datos sensibles.

Funciona con CFDI 3.3 y 4.0.

🤝 Contribuciones

Puedes abrir issues o enviar mejoras vía Pull Request.

📬 Contacto

Si te interesa implementar una solución similar para tu empresa, puedes contactarme vía LinkedIn  https://www.linkedin.com/in/christopher-ivan-perez-alonso-a283b3129/
