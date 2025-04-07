def quick_sort(arr):
    # Caso base: si la lista tiene 0 o 1 elementos, ya está ordenada
    if len(arr) <= 1:
        return arr
    
    # Elegimos un pivote (usualmente el primero, último o uno aleatorio)
    pivote = arr[0]
    
    # Partimos la lista en tres:
    menores = [x for x in arr[1:] if x < pivote]      # Menores al pivote
    iguales = [x for x in arr if x == pivote]         # Iguales al pivote
    mayores = [x for x in arr[1:] if x > pivote]      # Mayores al pivote
    
    # Aplicamos recursivamente el quick_sort a menores y mayores
    return quick_sort(menores) + iguales + quick_sort(mayores)

# Ejemplo de uso:
lista = [8, 3, 1, 7, 0, 10, 2]
ordenada = quick_sort(lista)
print("Lista ordenada:", ordenada)
