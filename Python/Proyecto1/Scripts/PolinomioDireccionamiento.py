def print_matrix(dim, pos):
    """
    Imprime la matriz en formato E[k1][k2]...[kn].

    Args:
        dim (int): Número de dimensiones de la matriz.
        pos (list): Lista de posiciones o tamaños de las dimensiones.
    """
    print("\nE", end="")
    if dim > 0:
        for j in range(dim):
            print(f"[{pos[j]}]", end="")  # Se imprimen las posiciones
    print()


def polinomio_direccionamiento(dim, pos, sizes, bytes):
    """
    Calcula la dirección de memoria aproximada usando el polinomio de direccionamiento.

    Args:
        dim (int): Número de dimensiones de la matriz.
        pos (list): Lista de posiciones en cada dimensión | empezando desde 1.
        sizes (list): Lista de tamaños de cada dimensión | empezando desde 1.
        bytes (int): Número de bytes del tipo de dato.

    Returns:
        long: Dirección de memoria aproximada.
    """
    dir = 0
    for n in range(dim):
        r = 1

        # Calcula r1 * r2 * ... * rn-1
        for i in range(n):
            r *= sizes[i]

        # Suma al resultado: r1 * r2 * ... * rn-1 * (kn - infn)
        dir += r * (pos[n] -1)  # pos[n] ya está en base 0
    return dir * bytes  # Multiplica por el tamaño del tipo de dato

def main():
    """
    Función principal del programa.
    Solicita al usuario los datos necesarios para calcular la dirección de memoria
    de un elemento en una matriz multidimensional.
    """
    while True:
        try:
            bytes = int(input("Introduzca el numero de bytes del tipo de la matriz: "))
            if bytes < 1:
                print("\nEl numero de bytes no puede ser negativo o cero\n")
            else:
                break
        except ValueError:
            print("\nEntrada inválida. Introduzca un número entero.\n")

    while True:
        try:
            dim = int(input("\nIntroduzca las dimensiones de la matriz: "))
            if dim < 1:
                print("\nLa matriz debe tener al menos una dimension\n")
            else:
                break
        except ValueError:
            print("\nEntrada inválida. Introduzca un número entero.\n")

    pos = [0] * dim
    sizes = [0] * dim

    for i in range(dim):
        while True:
            try:
                print_matrix(i, sizes)
                sizes[i] = int(input(f"[x]\nIntroduzca el numero de elementos de la dimension {i+1}: "))
                if sizes[i] < 1:
                    print("\nEl numero de elementos no puede ser negativo\n")
                else:
                    break
            except ValueError:
                print("\nEntrada inválida. Introduzca un número entero.\n")

        print_matrix(i + 1, sizes)
        print()

        while True:
            try:
                print_matrix(i, pos)
                pos[i] = int(input(f"[x]\nIntroduzca la posicion {i+1}: "))
                if pos[i] < 0 or pos[i] > sizes[i]:
                    print("\nLa posicion no puede ser negativa o mayor al rango de su dimension\n")
                else:
                    break
            except ValueError:
                print("\nEntrada inválida. Introduzca un número entero.\n")

    print_matrix(dim, sizes)
    print("\nEl elemento en posicion: ", end="")
    print_matrix(dim, pos)  # Se imprimen las posiciones
    print(f"\nTiene una direccion de memoria aproximada de: DirE + {polinomio_direccionamiento(dim, pos, sizes, bytes)}")  # Se imprime la direccion de memoria
