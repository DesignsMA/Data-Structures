#include <stdio.h>
#include <stdlib.h>

typedef struct Cola{
    int *datos;
    int frente;
    int final;
    int capacidad;
}Cola;

void comprobar( void* ptr) {
    if (ptr == NULL) {
        printf("\nError al reservar espacio.\n");
        exit(EXIT_FAILURE);
    }
}

char estaVacia(Cola *queue){
    return queue->frente == queue->final || queue->frente > (queue->capacidad-1);
}

void realocar(void** ptr, int nsize){ //contiene una direccion a un apuntador que apunta a un arreglo
    int *temp = (int *)realloc(*ptr, nsize * sizeof(int)); //devuelve NULL si no se aloja
    if (temp == NULL) {
        printf("\nError al reservar espacio.\n");
        free(*ptr); // Liberar la memoria original antes de salir
        exit(EXIT_FAILURE);
    } else *ptr = temp; // Asignar el nuevo bloque de memoria al apuntador original
}

void inicializar(Cola *queue){
    queue->datos = (int*)malloc(sizeof(int));
    comprobar((void*)queue->datos);
    queue->capacidad = 1;
    queue->final = queue->frente = -1;
}

void insertar( Cola *queue, int var) {
    if ( estaVacia(queue) ){
        queue->frente = queue->final = 0;
    }
    
    if ( queue->final == (queue->capacidad)) {
        queue->capacidad *=2;
        realocar((void*)&queue->datos, queue->capacidad);

    }
    
    queue->datos[queue->final++] = var;
}

void eliminar(Cola *queue) {
    if (estaVacia(queue)) {
        printf("\nLa cola esta vacia.\n");
    } else {
        queue->frente++;
        if (queue->frente > queue->capacidad / 2) {
            queue->capacidad /= 2;
            realocar((void*)&queue->datos, queue->capacidad);
        }
    }
}

int verCola(Cola *queue) {
    if ( estaVacia(queue) ) {
         printf("\nLa cola esta vacia.\n");
    } else return queue->datos[queue->frente];
}

void imprimir(Cola *queue) {
    if ( !estaVacia(queue) ){
        printf("\nCola\n");
        for (int i = queue->frente; i < queue->final ; i++){
            printf("%d  ", queue->datos[i]);
        }
    }
}

int main( int argc, char **argv) {
    Cola *queue = (Cola*)malloc(sizeof(Cola));
    int opc, temp;
    comprobar(queue);
    inicializar(queue);

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
                insertar(queue, temp);
                break;

            case 2:
                eliminar(queue);
                break;

            default:
                break;
        }

        imprimir(queue);
    } while (opc != -1);
    

    free(queue->datos); //Liberar memoria ocupada
    free(queue);


    
}
