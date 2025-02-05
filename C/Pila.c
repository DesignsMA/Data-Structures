#include <stdlib.h>
#include <stdio.h>
typedef struct Pila{
    int *datos;
    int tope;
    int capacidad;
}Pila;

void inicializar(Pila *stack){
    stack->datos = (int*)malloc(sizeof(int)); //inicializar
    if (stack->datos == NULL) {
        printf("\nError al reservar espacio.\n");
        exit(EXIT_FAILURE);
    }
    stack->tope = -1; //La pila esta vacia
    stack->capacidad =1;
}

char estaVacia(Pila *stack){
    return stack->tope==-1;
}

void realocar(void** ptr, int nsize){ //contiene una direccion a un apuntador que apunta a un arreglo
    int *temp = (int *)realloc(*ptr, nsize * sizeof(int)); //devuelve NULL si no se aloja
    if (temp == NULL) {
        printf("\nError al reservar espacio.\n");
        free(*ptr); // Liberar la memoria original antes de salir
        exit(EXIT_FAILURE);
    } else *ptr = temp; // Asignar el nuevo bloque de memoria al apuntador original
}


/*Realloc solo mueve de lugar el bloque original (si no puede ser extendido) o lo extiende, se conservan los  datos
  en caso de no poder ser extendido, el bloque de memoria original se libera tras copiarlo*/

void push(Pila *stack, int var){
    /*Si el proximo elemento es igual a la capacidad actual*/
    if ( stack->tope == (stack->capacidad-1)) { //Realizar el realojamiento de memoria menos veces es menos costoso
        stack->capacidad *=2;
        realocar((void*)&stack->datos, stack->capacidad);
    }

    stack->datos[++stack->tope] = var; //inicia en -1s
}

void pop(Pila *stack){
    if ( estaVacia(stack) ) {
        printf("La pila se encuentra vacia");
    } else {
        stack->tope -= 1;

        // Reducir la capacidad de la pila si está muy vacía
        if (stack->tope < stack->capacidad / 4) {
            stack->capacidad /= 2;
            realocar((void*)&stack->datos, stack->capacidad);
        }
    }
}

void imprimir(Pila *stack) {
    if ( estaVacia(stack) ) {
        printf("\n\nLa pila esta vacia");
    } else {
        printf("\n\n\t   Pila\n");
        for(int i = stack->tope ; i>=0; i--) {
            printf("\t%d. %d\n", stack->tope-(i-1), stack->datos[i]);
        }
    }
}

char verTope(Pila *stack) {
    if (estaVacia(stack)) {
        printf("La pila se encuentra vacía\n");
        exit(EXIT_FAILURE);
    }
    return stack->datos[stack->tope];
}

int main( int argc, char **argv){
    Pila *stack = (Pila*)malloc(sizeof(Pila));
    int opc, temp;

    if (stack == NULL) {
        printf("\nError al reservar espacio.\n");
        exit(EXIT_FAILURE);
    }

    inicializar(stack);
    do
    {
        printf("\n1. Insertar\n2. Eliminar\n-1. Salir\n: ");
        fflush(stdin);
        scanf("%d", &opc);
        fflush(stdin);
        switch (opc)
        {
            case 1:
                printf("\n: ");
                scanf("%d", &temp);
                push(stack, temp);
                break;

            case 2:
                pop(stack);
                break;

            default:
                break;
        }

        imprimir(stack);
    } while (opc != -1);
    

    free(stack->datos); //Liberar memoria ocupada
    free(stack);

}