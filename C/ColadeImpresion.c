#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TAMANIO_MAX_CADENA 100  // Definir un tamaño máximo para las cadenas

// Definición de la estructura de un trabajo de impresión
typedef struct Trabajo {
    int id;             // Identificador único del trabajo
    int paginas;        // Número de páginas a imprimir
    int prioridad;      // Prioridad del trabajo
    char nombre[TAMANIO_MAX_CADENA]; // Nombre del documento o del usuario
} Trabajo;

// Estructura de la cola de impresión
typedef struct Cola {
    Trabajo **datos;   // Punteros a trabajos
    int frente;
    int final;
    int capacidad;
} Cola;

void comprobar(void* ptr) {
    if (ptr == NULL) {
        printf("\nError al reservar espacio.\n");
        exit(EXIT_FAILURE);
    }
}

char estaVacia(Cola *queue) {
    return queue->frente == queue->final || queue->frente > (queue->capacidad - 1);
}

void realocar(void** ptr, int nsize) { 
    Trabajo **temp = (Trabajo **)realloc(*ptr, nsize * sizeof(Trabajo*)); // Realocación de memoria para trabajos
    if (temp == NULL) {
        printf("\nError al reservar espacio.\n");
        free(*ptr);
        exit(EXIT_FAILURE);
    } else *ptr = temp;
}

void inicializar(Cola *queue) {
    queue->datos = (Trabajo **)malloc(sizeof(Trabajo*));  // Alocar espacio para punteros a trabajos
    comprobar((void*)queue->datos);
    queue->capacidad = 1;
    queue->final = queue->frente = -1;
}

void insertar(Cola *queue, int id, const char* nombre, int paginas, int prioridad) {
    if (estaVacia(queue)) {
        queue->frente = queue->final = 0;
    }

    if (queue->final == queue->capacidad) {
        queue->capacidad *= 2;
        realocar((void*)&queue->datos, queue->capacidad);
    }

    // Crear un nuevo trabajo
    Trabajo *nuevoTrabajo = (Trabajo *)malloc(sizeof(Trabajo));
    nuevoTrabajo->id = id;
    nuevoTrabajo->paginas = paginas;
    nuevoTrabajo->prioridad = prioridad;
    strncpy(nuevoTrabajo->nombre, nombre, TAMANIO_MAX_CADENA);

    queue->datos[queue->final] = nuevoTrabajo; // Insertar el trabajo en la cola
    queue->final++;
}

void eliminar(Cola *queue) {
    if (estaVacia(queue)) {
        printf("\nLa cola esta vacía.\n");
    } else {
        Trabajo *trabajoEliminado = queue->datos[queue->frente];
        printf("\nTrabajo eliminado: ID: %d, Nombre: %s, Paginas: %d\n",
               trabajoEliminado->id, trabajoEliminado->nombre, trabajoEliminado->paginas);
        free(trabajoEliminado);  // Liberar la memoria del trabajo eliminado
        queue->frente++;
    }
}

void imprimir(Cola *queue) {
    if (!estaVacia(queue)) {
        printf("\nCola de impresion:\n");
        for (int i = queue->frente; i < queue->final; i++) {
            printf("ID: %d, Nombre: %s, Paginas: %d, Prioridad: %d\n", 
                   queue->datos[i]->id, queue->datos[i]->nombre, queue->datos[i]->paginas, queue->datos[i]->prioridad);
        }
    }
}

int main() {
    Cola *queue = (Cola*)malloc(sizeof(Cola));
    int opc, id, paginas, prioridad;
    char nombre[TAMANIO_MAX_CADENA];
    comprobar(queue);
    inicializar(queue);

    do {
        printf("\n1. Insertar trabajo de impresion\n2. Procesar trabajo\n3. Ver cola\n-1. Salir\n: ");
        scanf("%d", &opc);
        fflush(stdin);

        switch (opc) {
            case 1:
                printf("\nIntroduce el ID del trabajo: ");
                scanf("%d", &id);
                fflush(stdin);
                printf("Introduce el nombre del documento: ");
                fgets(nombre, TAMANIO_MAX_CADENA, stdin);
                nombre[strcspn(nombre, "\n")] = 0;  // Eliminar salto de línea al final
                printf("Introduce el numero de paginas: ");
                scanf("%d", &paginas);
                printf("Introduce la prioridad (1 es alta, 5 es baja): ");
                scanf("%d", &prioridad);
                insertar(queue, id, nombre, paginas, prioridad);
                break;

            case 2:
                eliminar(queue);
                break;

            case 3:
                imprimir(queue);
                break;

            default:
                break;
        }

    } while (opc != -1);

    // Liberar memoria
    for (int i = queue->frente; i < queue->final; i++) {
        free(queue->datos[i]);
    }
    free(queue->datos);
    free(queue);

    return 0;
}
