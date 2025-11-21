#Registro de alumnos

class Estudiante:
    def __init__ (self, matricula="", nombre="", carrera="", promedio=0.0, direccion=""):
        self.matricula = matricula
        self.nombre = nombre
        self.carrera = carrera
        self.promedio = promedio
        self.direccion = direccion

def capturar_datos():
    print("----- Captura de datos del estudiante -----")
    matricula = input("Ingrese la matrícula: ")
    nombre = input("Ingrese el nombre: ")
    carrera = input("Ingrese la carrera: ")
    promedio = float(input("Ingrese el promedio: "))
    direccion = input("Ingrese la dirección: ")

    # Crear y devolver el objeto tipo Estudiante
    return Estudiante(matricula, nombre, carrera, promedio, direccion)


def mostrar_datos(est):
    print("\n----- Datos del estudiante -----")
    print(f"Matrícula: {est.matricula}")
    print(f"Nombre: {est.nombre}")
    print(f"Carrera: {est.carrera}")
    print(f"Promedio: {est.promedio}")
    print(f"Dirección: {est.direccion}")


def main():
    estudiante = capturar_datos()
    mostrar_datos(estudiante)


if __name__ == "__main__":
    main()

