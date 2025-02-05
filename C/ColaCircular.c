#include <stdio.h>
#include <stdlib.h>

typedef struct Cola{
    int *datos;
    int frente;
    int final;
    char ultimo;
    int capacidad;
}Cola;

void comprobar( void* ptr) {
    if (ptr == NULL) {
        printf("\nError al reservar espacio.\n");
        exit(EXIT_FAILURE);
    }
}

char estaVacia(Cola *queue){
    return (queue->final)%(queue->capacidad) == queue->frente%(queue->capacidad) && queue->ultimo == 'E';
}

char estaLlena(Cola *queue){
    return (queue->final)%(queue->capacidad) == queue->frente%(queue->capacidad) && queue->ultimo == 'I';
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
    queue->final = queue->frente = 0;
    queue->ultimo = 'E';
}

void insertar( Cola *queue, int var) {
    
    if ( estaLlena(queue) ) {
        queue->capacidad *=2;
        realocar((void*)&queue->datos, queue->capacidad);
        for (int i = 0; i < queue->frente; i++)
        {
            queue->datos[i+queue->capacidad/2] =  queue->datos[i]; //reordenando cola
        }
        
    }
    
    queue->datos[(queue->final++)%(queue->capacidad)] = var;
    queue->ultimo = 'I';
}

void eliminar(Cola *queue) {
    if (estaVacia(queue)) {
        printf("\nLa cola esta vacia.\n");
        if ( queue->capacidad > 1) {
            queue->capacidad /= 2;
            realocar((void*)&queue->datos, queue->capacidad);
        }
        queue->frente = queue->final = 0;
    } else {
        queue->frente++;
        queue->ultimo = 'E';        
    }
}

void imprimir(Cola *queue) {
    if ( !estaVacia(queue) ){
        printf("\nCola\n");
        for (int i = queue->frente; i < queue->final ; i++){
            printf("%d  ", queue->datos[i%(queue->capacidad)]);
        }
        printf("\n\nReal:\n");
        for (int i = 0; i < queue->capacidad ; i++){
            printf("%d  ", queue->datos[i]);
        }
    }
}

int verCola(Cola *queue) {
    if ( estaVacia(queue) ) {
         printf("\nLa cola esta vacia.\n");
    } else return queue->datos[queue->frente%(queue->capacidad)];
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
