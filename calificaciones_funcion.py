#Calificaciones con funcion

def arreglo(n):
    calificaciones = []
    for i in range (n):
        valor = float(input(f"Ingrese la calificación {i+1}: "))
        calificaciones.append(valor)
    return calificaciones

def calcular_promedio(lista):
    if len(lista) == 0:
        return 0
    return sum(lista)/len(lista)

def main():
    n = int(input("Cuantas calificaciones desea registrar: "))
    calificaciones = arreglo(n)
    promedio = calcular_promedio(calificaciones)
    print(f"El promedio es: {promedio:.2f}")

if __name__ == "__main__":
    main()