#Programa para detectar si un número es par o impar

def par_impar(numero):
    if numero % 2 == 0:
        return f"El numero {numero} es par"
    else:
        return f"El numero {numero} es impar"

#Solicitar el numero al usuario
try:
    numero = int(input("Ingrese un numero entero: "))   
    print(par_impar(numero))
except ValueError:
    print("Error: Ingrese un numero entero valido") 
        