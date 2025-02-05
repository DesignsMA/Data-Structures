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
        if ( queue->capacidad > 5) {
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
// Función para reproducir la lista de canciones
void reproducir(Cola *queue,char **canciones) {
    if (estaVacia(queue)) {
        printf("\nNo hay canciones en la lista de reproduccion.\n");
        return;
    }

    printf("\nReproduciendo lista de canciones:\n");
    int i = queue->frente;
    while (i != queue->final) {
        int cancion = queue->datos[i % queue->capacidad];
        if (cancion == -1) {
            printf("Cancion dañada o inexistente - Saltando a la siguiente...\n");
        } else {
            printf("Reproduciendo cancion: %d | %s\n", cancion, canciones[cancion]);
        }
        i++;
    }
    printf("Fin de la lista de reproduccion.\n");
}

// Función principal
int main() {
    Cola *queue = (Cola *)malloc(sizeof(Cola));
    comprobar(queue);
    inicializar(queue);
    char *canciones[] = {
    "Bohemian Rhapsody",
    "Stairway to Heaven",
    "Hotel California",
    "Imagine",
    "Smells Like Teen Spirit",
    "Like a Rolling Stone",
    "Hey Jude",
    "Purple Haze",
    "Yesterday",
    "Let It Be"
};

    int opc, temp, num_elementos = sizeof(canciones) / sizeof(canciones[0]);;
    do {
        
        printf("\n1. Insertar cancion\n2. Eliminar cancion\n3. Reproducir lista\n4. Lista de canciones\n-1. Salir\n: ");
        scanf("%d", &opc);

        switch (opc) {
            case 1:
                printf("\nIngrese el ID de la cancion: ");
                scanf("%d", &temp);
                if (temp > num_elementos-1 || temp < 0) { 
                    temp = -1;
                }
                insertar(queue, temp);
                break;

            case 2:
                eliminar(queue);
                break;

            case 3:
                reproducir(queue, canciones);
                break;

            case 4:
                for ( int i = 0; i < num_elementos; i++)
                {
                    printf("\nId: %d | %s",i, canciones[i]);
                }
            break;

            case -1:
                printf("\nSaliendo...\n");
                break;

            default:
                printf("\nOpcion no valida.\n");
                break;
        }
    } while (opc != -1);

    free(queue->datos);  // Liberar memoria ocupada por las canciones
    free(queue);             // Liberar memoria ocupada por la cola

    return 0;
}