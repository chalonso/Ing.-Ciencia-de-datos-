# Revisión del código: Correcciones y mejoras en la gestión del DataFrame y paso de referencias

import pandas as pd
import os

COLUMNAS = [
    "gym_nip", "nombre", "ape_paterno", "ape_materno",
    "nacimiento", "sexo", "telefono", "dia_registro",
    "paquete", "cont_emergencias", "tel_emergencia",
    "parentesco", "estatus"
]

# Lee el CSV de usuarios si existe, sino crea un DataFrame vacío
if os.path.exists("usuarios.csv"):
    df_usuarios = pd.read_csv("usuarios.csv")
else:
    df_usuarios = pd.DataFrame(columns=COLUMNAS)

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

def registro(df):
    print("\n--- REGISTRO DE USUARIO ---")
    while True:
        nuevo_usuario = {}

        # Generar gym_nip incremental único
        if df.empty:
            gym_nip = 1
        else:
            gym_nip = int(df["gym_nip"].astype(int).max()) + 1
        nuevo_usuario["gym_nip"] = gym_nip

        # Solicitar datos del usuario excepto campos protegidos
        for col in COLUMNAS:
            if col not in ["gym_nip", "estatus"]:
                nuevo_usuario[col] = input(f"{col.replace('_', ' ').capitalize()}: ")

        nuevo_usuario["estatus"] = "ACTIVO"

        df = pd.concat([df, pd.DataFrame([nuevo_usuario])], ignore_index=True)
        df.to_csv("usuarios.csv", index=False)

        print(f"✅ Usuario registrado correctamente. Gym NIP asignado: {gym_nip}")

        continuar = input("¿Desea registrar otro usuario? (s/n): ").strip().lower()
        if continuar != "s":
            break

    return df

def baja(df):
    print("\n--- Baja de usuario ---")
    while True:
        try:
            nip = int(input("Ingrese el gym_nip del usuario para dar de baja: "))
        except ValueError:
            print("❌ El valor ingresado no es un número válido.")
            continue

        if nip in df["gym_nip"].astype(int).values:
            idx = df.index[df["gym_nip"].astype(int) == nip][0]
            if df.at[idx, "estatus"] == "ACTIVO":
                df.at[idx, "estatus"] = "INACTIVO"
                df.to_csv("usuarios.csv", index=False)
                print("🛑 Usuario cambiado a estado INACTIVO correctamente.")
            else:
                print("⚠️ El usuario ya está inactivo.")
        else:
            print("❌ No existe un usuario con ese gym_nip.")

        continuar = input("¿Desea eliminar otro usuario? (s/n): ").strip().lower()
        if continuar != "s":
            break

    return df

def modificacion(df):
    print("\n----Modificaciones de usuario----")
    while True:
        try:
            nip = int(input("Ingrese el gym_nip del usuario a modificar: "))
        except ValueError:
            print("❌ El valor ingresado no es un número válido.")
            continue

        if nip in df["gym_nip"].astype(int).values:
            idx = df.index[df["gym_nip"].astype(int) == nip][0]
            print("Columnas disponibles para modificar:")
            columnas_modificables = [col for col in df.columns if col != "gym_nip"]
            while True:
                for i, col in enumerate(columnas_modificables, 1):
                    print(f"{i}. {col}")
                seleccion = input("Ingrese el número de la columna que desea modificar (o '0' para salir): ")
                if seleccion == "0":
                    break
                try:
                    seleccion_int = int(seleccion)
                    if 1 <= seleccion_int <= len(columnas_modificables):
                        columna_a_modificar = columnas_modificables[seleccion_int - 1]
                        nuevo_valor = input(f"Ingrese el nuevo valor para '{columna_a_modificar}': ")
                        df.at[idx, columna_a_modificar] = nuevo_valor
                        df.to_csv("usuarios.csv", index=False)
                        print(f"✅ '{columna_a_modificar}' actualizado correctamente.")
                    else:
                        print("Selección inválida. Intente de nuevo.")
                except ValueError:
                    print("Por favor, ingrese un número válido.")
                continuar = input("¿Desea modificar otra columna de este usuario? (s/n): ").strip().lower()
                if continuar != "s":
                    break
        else:
            print("❌ No existe un usuario con ese gym_nip.")

        continuar = input("¿Desea modificar otro usuario? (s/n): ").strip().lower()
        if continuar != "s":
            break

    return df

def consulta(df):
    usuarios_activos = df[df["estatus"] == "ACTIVO"]
    if usuarios_activos.empty:
        print("No hay usuarios con estatus 'activo'.")
    else:
        print("Usuarios con estatus 'activo':")
        print(usuarios_activos.drop(columns=["estatus"]))
    return df

if __name__ == "__main__":
    menu(df_usuarios)