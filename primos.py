#Ejercicio 3 Estructura de repetición
# numeros primos dentro de los primeros n numeros naturales

def primos(limite):
    cantidad_primos = 0
    for i in range(1, limite + 1):
        if es_primo(i):
            print(f"{i} - Rosa")
            cantidad_primos += 1
        else:
            print(f"{i} - Azul")
    return cantidad_primos

def es_primo(numero):
    if numero < 2:
        return False
    for i in range(2, numero):
        if numero % i == 0:
            return False
    return True

#Programa principal
try:
    limite = int(input("Ingrese el limite: "))
    cantidad_primos = primos(limite)
    print(f"La cantidad de numeros primos es: {cantidad_primos}")
except ValueError:
    print("Error: Ingrese un numero valido")

    
    
    