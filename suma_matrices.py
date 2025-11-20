# Arreglo bidimensional
#Suma de matrices

def llenar_matriz(m,n, nombre):
    print(f"\n--Llenar matriz {nombre}---")
    matriz = []
    for i in range (m):
        fila = []
        for j in range (n):
            valor = float(input(f"Ingrese el valorde [{i+1},{j+1}] de la matriz {nombre} :"))
            fila.append(valor)
        matriz.append(fila)
    return matriz

def sumar_matrices(A, B, m, n):
    matriz_suma = []
    for i in range(m):
        fila = []
        for j in range(n):
            fila.append(A[i][j] + B[i][j])
        matriz_suma.append(fila)
    return matriz_suma


def mostrar_matriz(matriz, titulo="Resultado"):
    print(f"\n--- {titulo} ---")
    for fila in matriz:
        print(" ".join([f"{valor:.2f}" for valor in fila]))


def main():
    print("Programa para sumar dos matrices")

    m = int(input("Número de filas (m): "))
    n = int(input("Número de columnas (n): "))

    matrizA = llenar_matriz(m, n, "A")
    matrizB = llenar_matriz(m, n, "B")

    matriz_resultado = sumar_matrices(matrizA, matrizB, m, n)

    mostrar_matriz(matriz_resultado, "Suma de matrices")


if __name__ == "__main__":
    main()