# GYM Equinox
# Desarrollo de la primera parte del proyecto.

import pandas as pd

# --- Base de datos vacía como DataFrame ---
COLUMNAS = [
    "gym_nip", "nombre", "ape_paterno", "ape_materno",
    "nacimiento", "sexo", "telefono", "dia_registro",
    "paquete", "cont_emergencias", "tel_emergencia",
    "parentesco", "estatus"
]

df_usuarios = pd.DataFrame(columns=COLUMNAS)


# ---------------- MENÚ PRINCIPAL ----------------
def menu(df):

    while True:
        print("\n====== MENÚ PRINCIPAL ======")
        print("1. Registro de usuario")
        print("2. Baja de usuario")
        print("3. Modificación de usuario")
        print("4. Consulta de usuarios activos")
        print("5. Salir")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            df = registro(df)
        elif opcion == "2":
            df = baja(df)
        elif opcion == "3":
            df = modificacion(df)
        elif opcion == "4":
            consulta(df)
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("❌ Opción no válida, intente de nuevo.")

    return df



# ---------------- REGISTRO ----------------
def registro(df):

    print("\n--- REGISTRO DE USUARIO ---")

    while True:
        nuevo_usuario = {}

        # Generar gym_nip automático
        gym_nip = 1 if df.empty else int(df["gym_nip"].max()) + 1
        nuevo_usuario["gym_nip"] = gym_nip

        # Pedir datos (excepto gym_nip y estatus)
        for col in COLUMNAS:
            if col not in ["gym_nip", "estatus"]:
                nuevo_usuario[col] = input(f"{col.replace('_', ' ').capitalize()}: ")

        nuevo_usuario["estatus"] = "ACTIVO"

        df = pd.concat([df, pd.DataFrame([nuevo_usuario])], ignore_index=True)

        print(f"✅ Usuario registrado correctamente. Gym NIP asignado: {gym_nip}")

        continuar = input("¿Registrar otro usuario? (s/n): ").strip().lower()
        if continuar != "s":
            break

    return df



# ---------------- BAJA ----------------
def baja(df):
    print("\n--- BAJA DE USUARIO ---")

    while True:
        try:
            nip = int(input("Ingrese el gym_nip del usuario a dar de baja: "))
        except ValueError:
            print("❌ Ingrese un número válido.")
            continue

        if nip in df["gym_nip"].values:
            idx = df.index[df["gym_nip"] == nip][0]

            if df.at[idx, "estatus"] == "ACTIVO":
                df.at[idx, "estatus"] = "INACTIVO"
                print("🛑 Usuario marcado como INACTIVO correctamente.")
            else:
                print("⚠️ El usuario ya está inactivo.")
        else:
            print("❌ No existe un usuario con ese gym_nip.")

        if input("¿Dar de baja otro usuario? (s/n): ").lower() != "s":
            break

    return df



# ---------------- MODIFICACIÓN ----------------
def modificacion(df):

    print("\n--- MODIFICAR USUARIO ---")

    while True:
        try:
            nip = int(input("Ingrese el gym_nip del usuario a modificar: "))
        except ValueError:
            print("❌ Ingrese un número válido.")
            continue

        if nip not in df["gym_nip"].values:
            print("❌ No existe un usuario con ese gym_nip.")
            continue

        idx = df.index[df["gym_nip"] == nip][0]
        columnas_modificables = [c for c in COLUMNAS if c != "gym_nip"]

        print("\nColumnas disponibles para modificar:")

        for i, col in enumerate(columnas_modificables, 1):
            print(f"{i}. {col}")

        seleccion = input("Seleccione columna (0 para salir): ")

        if seleccion == "0":
            break

        try:
            seleccion = int(seleccion)
            col = columnas_modificables[seleccion - 1]
        except:
            print("❌ Selección inválida.")
            continue

        nuevo_valor = input(f"Nuevo valor para {col}: ")
        df.at[idx, col] = nuevo_valor

        print("✅ Campo actualizado.")

        if input("¿Modificar otra columna? (s/n): ").lower() != "s":
            break

    return df



# ---------------- CONSULTA ----------------
def consulta(df):
    print("\n--- USUARIOS ACTIVOS ---")
    activos = df[df["estatus"] == "ACTIVO"]

    if activos.empty:
        print("No hay usuarios activos.")
    else:
        print(activos)



# --- EJECUCIÓN DEL SISTEMA ---
if __name__ == "__main__":
    df_usuarios = menu(df_usuarios)
