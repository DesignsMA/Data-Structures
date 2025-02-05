#include <stdio.h>
#include <stdlib.h>


void printMatrix(int dim, int pos[]) {
    printf("\nE");
    if (dim >0)
    for( int j = 0; j < dim; j++) 
        printf("[%u]", pos[j]); //Se imprimen las posiciones
}
/*Pd(E[k1 ,k2 ,…,kn ]) = dirE + [r1 * r2 * r3 * … * rn-1 * (kn -infn ) + r1 * r2 * r3 * … * rn-2 * 
(kn-1 -infn-1 ) + … + r1 * (k2 -inf2 ) + (k1 - inf1 )] * T*/
long int polinomioDireccionamiento(int dim, int pos[], int sizes[], int bytes) {
    long int dir = 0;
    for (int n = 0; n < dim; n++) {
        long int r = 1;

        // Calcula r1 * r2 * ... * rn-1
        for (int i = 0; i < n; i++) {
            r *= sizes[i];
        }

        // Suma al resultado: r1 * r2 * ... * rn-1 * (kn - infn)
        dir += r * pos[n]; // pos[n] ya está en base 0
    }
    return dir * bytes; // Multiplica por el tamaño del tipo de dato
}

int main(int argc, char **argv) {
    int dim, bytes;

    do
    {
        printf("Introduzca el numero de bytes del tipo de la matriz: ");
        scanf("%d", &bytes);
        if (bytes < 1) {
            printf("\nEl numero de bytes no puede ser negativo o cero\n");
        }
    } while (bytes < 1);

    do {
        printf("\nIntroduzca las dimensiones de la matriz: ");
        scanf("%d", &dim);
        if (dim < 1) {
            printf("\nLa matriz debe tener al menos una dimension\n");
        }
    } while (dim < 1);
    
    int pos[dim], sizes[dim]; //, test[3][4]; //Arreglo de posiciones

    for( int i = 0; i < dim; i++) { 
        int est = 0; //Variable de estado
        do
        {
            printMatrix(i, sizes);
            printf("[x]\nIntroduzca el numero de elementos de la dimension x: ", i+1);
            printf("\n");
            fflush(stdin);
            est = scanf("%d", &sizes[i]);
            if (sizes[i] < 1) {
                printf("\nEl numero de elementos no puede ser negativo\n");
                est = 0;
            }
        } while ( est == 0 ); //Se pide la posicion

        printMatrix(i+1, sizes);
        printf("\n");

        do
        {
            printMatrix(i, pos);
            printf("[x]\nIntroduzca la posicion x: ", i+1);
            printf("\n");
            fflush(stdin);
            est = scanf("%d", &pos[i]); //Se pide la posicion
            if (pos[i] < 0 || pos[i] > sizes[i]) {
                printf("\nLa posicion no puede ser negativa o mayor al rango de su dimension\n");
                est = 0;
            }
        } while ( est == 0 ); //Se pide la posicion
    }
    printMatrix(dim, sizes);
    printf("\nEl elemento en posicion: ");
    printMatrix(dim, pos); //Se imprimen las posiciones
    printf("\nTiene una direccion de memoria aproximada de: DirE + %ld", polinomioDireccionamiento(dim, pos, sizes, bytes)); //Se imprime la direccion de memoria    

    
}