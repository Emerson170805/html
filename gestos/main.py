def factorial(n):
    if n < 0:
        return "No existe el factorial de un número negativo"
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado

# Prueba
numero = int(input("Ingresa un número entero: "))
print(f"El factorial de {numero} es {factorial(numero)}")
