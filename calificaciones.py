# Ejercicio 2 Estructura Selectiva
# Calificaciones

def calificaciones(nota):
    if nota < 0 or nota > 10:  
        return "Error: La nota debe estar entre 0 y 10"
    elif nota >= 0 and nota < 6:
        return "No acreditado"
    elif nota >= 6  and nota <= 7:
        return "Regular"
    elif nota > 7 and nota <= 8:
        return "Bien"
    elif nota > 8 and nota <= 9:
        return "Muy Bien"
    elif nota > 9 and nota <= 10:
        return "Excelente"

#Solicitar la nota al usuario
try:
    nota = float(input("Ingrese la nota del alumno: "))
    print(calificaciones(nota))
except ValueError:
    print("Error: Ingrese una nota valida")