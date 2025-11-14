🏋️‍♂️ Sistema de Gestión de Usuarios — GYM Equinox
Proyecto de Lógica y Programación Estructurada (Python)

Este proyecto implementa un sistema básico de control de usuarios para un gimnasio.
Permite registrar, consultar, modificar y dar de baja usuarios mediante un menú interactivo en consola.
Los datos se almacenan en un DataFrame de pandas, simulando una base de datos.

📌 Funciones principales del sistema

El programa está compuesto por cuatro módulos principales:

✔ 1. Registro de usuario

Permite capturar los datos de un nuevo usuario.

El sistema genera automáticamente el gym_nip (ID único incremental).

Se solicitan datos personales como:

nombre, apellidos

fecha de nacimiento

sexo

teléfono

fecha de registro

paquete contratado

contacto de emergencia, teléfono y parentesco

El usuario se registra con estatus ACTIVO.

✔ 2. Baja de usuario

Permite cambiar el estatus de un usuario de ACTIVO → INACTIVO.

Se busca mediante el gym_nip.

No se eliminan los datos; solo se modifica el estado.

Valida si el usuario existe y si ya está inactivo.

✔ 3. Modificación de usuario

Permite actualizar cualquier campo de un usuario registrado, excepto su gym_nip.

Se despliega un menú con las columnas modificables.

El usuario selecciona qué campo quiere editar.

Se actualiza el DataFrame en tiempo real.

✔ 4. Consulta de usuarios activos

Muestra únicamente los registros cuyo estatus es ACTIVO.

Filtra el DataFrame.

Muestra los usuarios en formato tabular.

🧠 Estructuras de programación utilizadas

Este proyecto utiliza los dos tipos principales de estructuras vistas en clase:

🔹 Estructuras Selectivas (if / elif / else)

Usadas para:

Determinar si un usuario existe.

Validar entradas incorrectas.

Verificar estatus antes de dar de baja.

Elegir opciones del menú.

🔹 Estructuras Repetitivas (while True)

Usadas para:

Mantener el menú principal activo.

Registrar múltiples usuarios.

Repetir acciones como modificaciones o bajas.

🧱 Estructura de Datos (DataFrame)

Se utiliza un DataFrame con las siguientes columnas:

gym_nip
nombre
ape_paterno
ape_materno
nacimiento
sexo
telefono
dia_registro
paquete
cont_emergencias
tel_emergencia
parentesco
estatus


Esto permite manipular la información como si fuera una base de datos.

🚀 Cómo ejecutar el proyecto
1️⃣ Instalar dependencias
pip install pandas

2️⃣ Ejecutar el programa
python equinox.py

📂 Estructura del repositorio
/Ing.-Ciencia-de-datos-
│── LPE/
│   ├── equinox.py
│── README.md   ← este archivo
