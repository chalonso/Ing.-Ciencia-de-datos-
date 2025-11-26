#Convertidor_cadenas
# Análisis de sintaxis:
# 1. Definición de función: def convertir_cadena():
# 2. Solicita una cadena por input y muestra un menú de opciones.
# 3. Utiliza if-elif-else para determinar la opción del usuario:
#    a. Opción 1: llama texto.upper() pero el mensaje menciona "minusculas" (debe ser mayúsculas).
#    b. Opción 2: llama texto.lower() pero el mensaje menciona "mayusculas" (debe ser minúsculas).
#    c. Opción 3: usa len(texto) para contar caracteres.
#    d. Opción 4: pide subcadenas e implementa replace().
#    e. Opción 5: define función interna compare() (podría estar afuera), compara igualdad de dos cadenas.
# 4. else captura opción no válida.
# 5. Estructura principal con if __name__ == "__main__":

def convertir_cadena():
    texto = input("Ingresa una cadena de texto: ")
    print("Elige una opción:")
    print("1. Convertir a mayúsculas")        # opción 1: .upper()
    print("2. Convertir a minúsculas")        # opción 2: .lower()
    print("3. Cantidad de caracteres")        # opción 3: len(texto)
    print("4. Sustituir parte de la cadena por otra") # opción 4: replace()
    print("5. Compara dos cadenas")           # opción 5: comparación de igualdad
    opcion = input("Opción: ")

    if opcion == "1":
        print("El texto se convierte a mayúsculas:", texto.upper())
    elif opcion == "2":
        print("El texto se convierte a minúsculas:", texto.lower())
    elif opcion == "3":
        largo = len(texto)
        print(f"La cadena de texto tiene {largo} caracteres")
    elif opcion == "4":
        buscar = input("Ingresa la palabra o frase a buscar: ")
        reemplazo = input("Ingresa el texto de reemplazo: ")
        nuevo_texto = texto.replace(buscar, reemplazo)
        print("Texto resultante:", nuevo_texto)
    elif opcion == "5":
        def compare(cad1, cad2):
            return cad1 == cad2
        cadena2 = input("Ingresa la segunda cadena para comparar: ")
        if compare(texto, cadena2):
            print("Las cadenas son iguales.")
        else:
            print("Las cadenas son diferentes.")
    else:
        print("Opción no válida")

if __name__ == "__main__":
    convertir_cadena()