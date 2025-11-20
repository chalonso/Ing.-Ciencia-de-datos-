#Par e impar con funcion def y main 

def es_par(numero):
    return numero % 2 == 0

def main():
    print("El siguiente programa le ayudar a identificar \n si un número es par o impar.")
    print("Ingrese el numero a evaluar", end=" ")

    try:
        numero = int(input())
    except ValueError:
        print("Error: Debe ingresar un número entero.")
        return
    
    #Uso de la función es_par()
    if es_par(numero):
        print(f"El numero {numero} es par.")
    else:
        prin(f"El numero {numero} es impar.")

if __name__ == "__main__":
    main()