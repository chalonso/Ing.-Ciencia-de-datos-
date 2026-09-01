#Ejercicio 4
#Supermercado- ticket
#Programa para generar un ticket de compra dado n articulos pedir de cada uno la cantidad y el precio unitario para calcular el total de la compra

# Pedir el nombre del cliente
def nombre_cliente():
    return input("Ingrese el nombre del cliente: ")

# Generar el ticket de compra con ciclo para ingresar cada artículo
def ticket_compra():
    cliente = nombre_cliente()
    articulos = []
    while True:
        agregar = input("¿Desea ingresar un artículo? (s/n): ").strip().lower()
        if agregar != 's':
            break
        nombre = input("Ingrese el nombre del artículo: ")
        try:
            cantidad = int(input("Ingrese la cantidad del artículo: "))
            precio = float(input("Ingrese el precio unitario del artículo: "))
        except ValueError:
            print("Error: cantidad o precio inválido, intente de nuevo.")
            continue
        articulos.append({"nombre": nombre, "cantidad": cantidad, "precio": precio})

    total = sum(item["cantidad"] * item["precio"] for item in articulos)

    print("\n--- Ticket de compra ---")
    print(f"Cliente: {cliente}")
    print(f"Número de artículos diferentes: {len(articulos)}")
    for idx, item in enumerate(articulos, 1):
        print(f"Artículo {idx}: {item['nombre']} - Cantidad: {item['cantidad']} - Precio unitario: {item['precio']} - Subtotal: {item['cantidad']*item['precio']}")
    print(f"Total de la compra: {total:.2f}")

# Programa principal
if __name__ == "__main__":
    ticket_compra()

