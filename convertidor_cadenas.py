#Convertidor_cadenas
def convertir_cadena():
    texto = input("Ingresa una cadena de texto: ")
    print("Elige una opción:")
    print("1. Convertir a mayúsculas")
    print("2. Convertir a minúsculas")
    opcion = input("Opción: ")

    if opcion == "1":
        print("Resultado:", texto.upper())
    elif opcion == "2":
        print("Resultado:", texto.lower())
    else:
        print("Opción no válida")

if __name__ == "__main__":
    convertir_cadena()