#include <stdio.h>
#define MAX 100

// Estructura para representar un nodo
typedef struct Nodo {
    int dato;
    int sig; // Índice del siguiente nodo en el arreglo
} Nodo;

// Arreglo estático para la lista
Nodo lista[MAX];
int cabeza = -1; // Índice del primer nodo (-1 indica lista vacía)
int libre = 0;   // Índice del primer nodo disponible

// Función para inicializar la lista estática
void inicializarLista() {
    for (int i = 0; i < MAX - 1; i++) {
        lista[i].sig = i + 1; // Apunta al siguiente índice disponible
    }
    lista[MAX - 1].sig = -1; // Último nodo no tiene siguiente
}

// Función para insertar un nodo al inicio
void insertaInicio(int valor) {
    if (libre == -1) {
        printf("Error: No hay espacio disponible en la lista.\n");
        return;
    }

    int nuevo = libre;       // Toma el índice del nodo libre
    libre = lista[libre].sig; // Actualiza el índice libre al siguiente

    // Asigna el valor al nuevo nodo
    lista[nuevo].dato = valor;

    if (cabeza == -1) {
        // Si la lista está vacía, el nuevo nodo será la cabeza y apunta a sí mismo
        cabeza = nuevo;
        lista[nuevo].sig = nuevo;
    } else {
        // Enlaza el nuevo nodo al inicio
        lista[nuevo].sig = cabeza;

        // Actualiza el último nodo para que apunte al nuevo nodo
        int actual = cabeza;
        while (lista[actual].sig != cabeza) {
            actual = lista[actual].sig;
        }
        lista[actual].sig = nuevo;

        // Actualiza la cabeza
        cabeza = nuevo;
    }
}
// Función para insertar un nodo en una posición específica
void insertaMedio(int valor, int pos) {
    if (libre == -1) {
        printf("Error: No hay espacio disponible en la lista.\n");
        return;
    }

    // Verificar si la posición es válida
    if (pos < 0 || pos >= MAX) {
        printf("Error: La posición no es válida.\n");
        return;
    }

    // Tomar un nodo libre
    int nuevo = libre;
    libre = lista[libre].sig;

    // Asignar el valor al nuevo nodo
    lista[nuevo].dato = valor;

    // Insertar el nuevo nodo después del nodo en la posición `pos`
    lista[nuevo].sig = lista[pos].sig;
    lista[pos].sig = nuevo;
}

// Función para insertar un nodo al final
void insertaFinal(int valor) {
    if (libre == -1) {
        printf("Error: No hay espacio disponible en la lista.\n");
        return;
    }

    int nuevo = libre;       // Toma el índice del nodo libre
    libre = lista[libre].sig; // Actualiza el índice libre al siguiente

    // Asignar el valor al nuevo nodo
    lista[nuevo].dato = valor;
    lista[nuevo].sig = cabeza; // Este nodo será el último, regresa al principio

    if (cabeza == -1) {
        // Si la lista está vacía, el nuevo nodo será la cabeza
        cabeza = nuevo;
        lista[nuevo].sig = nuevo; //apunta a si mismo
    } else {
        // Recorrer la lista para encontrar el último nodo
        int actual = cabeza;
        while (lista[actual].sig != cabeza) {
            actual = lista[actual].sig;
        }
        lista[actual].sig = nuevo; // Enlaza el nuevo nodo al final
    }
}

// Función para borrar el nodo final
int borrarFinal() {
    if (cabeza == -1) {
        printf("Error: La lista está vacía.\n");
        return -1;
    }

    int actual = cabeza;
    int anterior = -1;

    // Recorrer hasta el último nodo
    while (lista[actual].sig != cabeza) {
        anterior = actual;
        actual = lista[actual].sig;
    }

    int datoEliminado = lista[actual].dato;

    if (anterior == -1) {
        // Si solo hay un nodo
        cabeza = -1;
    } else {
        // Eliminar el último nodo
        lista[anterior].sig = cabeza;
    }

    // Liberar el nodo eliminado
    lista[actual].sig = libre;
    libre = actual;

    return datoEliminado;
}

// Función para buscar un elemento en la lista
int buscarElemento(int valorBuscado) {
    if (cabeza == -1) {
        return -1; // Lista vacía
    }

    int actual = cabeza;
    do {
        if (lista[actual].dato == valorBuscado) {
            return actual; // Retorna el índice del nodo encontrado
        }
        actual = lista[actual].sig;
    } while (actual != cabeza);

    return -1; // Retorna -1 si no encuentra el valor
}

// Función para borrar el nodo al inicio
void borraInicio() {
    if (cabeza == -1) {
        printf("Error: La lista ya está vacía.\n");
        return;
    }

    int nodoEliminado = cabeza;

    if (lista[cabeza].sig == cabeza) {
        // Si solo hay un nodo
        cabeza = -1;
    } else {
        // Actualizar la cabeza y el último nodo
        int actual = cabeza;
        while (lista[actual].sig != cabeza) {
            actual = lista[actual].sig;
        }
        cabeza = lista[cabeza].sig;
        lista[actual].sig = cabeza;
    }

    // Liberar el nodo eliminado
    lista[nodoEliminado].sig = libre;
    libre = nodoEliminado;
}

// Función para borrar un nodo en una posición específica
void borraMedio(int pos) {
    if (cabeza == -1) {
        printf("Error: La lista está vacía.\n");
        return;
    }

    // Verificar si la posición es válida
    if (pos < 0 || pos >= MAX) {
        printf("Error: La posición no es válida.\n");
        return;
    }

    // Caso especial: borrar el primer nodo
    if (pos == cabeza) {
        borraInicio();
        return;
    }

    // Buscar el nodo anterior al que se va a eliminar
    int anterior = cabeza;
    while (lista[anterior].sig != pos) {
        anterior = lista[anterior].sig;
        if (anterior == cabeza) {
            printf("Error: La posición no existe en la lista.\n");
            return;
        }
    }

    // Eliminar el nodo en la posición `pos`
    int nodoEliminado = lista[anterior].sig;
    lista[anterior].sig = lista[nodoEliminado].sig;

    // Liberar el nodo eliminado
    lista[nodoEliminado].sig = libre;
    libre = nodoEliminado;
}

// Función para imprimir la lista
void imprimirLista() {
    if (cabeza == -1) {
        printf("Lista vacía.\n");
        return;
    }

    int actual = cabeza;
    do {
        printf("%d -> ", lista[actual].dato);
        actual = lista[actual].sig;
    } while (actual != cabeza);
    printf("\n");
}

// Función principal
int main() {
inicializarLista(); // Inicializa la lista estática

    // Caso 1: Insertar al inicio
    insertaInicio(10);
    printf("Lista después de insertar 10 al inicio: ");
    imprimirLista();

    // Caso 2: Insertar al final
    insertaFinal(20);
    printf("Lista después de insertar 20 al final: ");
    imprimirLista();

    // Caso 3: Insertar en medio
    insertaMedio(15, buscarElemento(10));
    printf("Lista después de insertar 15 en medio: ");
    imprimirLista();

    // Caso 4: Eliminar al inicio
    borraInicio();
    printf("Lista después de borrar al inicio: ");
    imprimirLista();

    // Caso 5: Eliminar al final
    borrarFinal();
    printf("Lista después de borrar al final: ");
    imprimirLista();

    // Caso 6: Eliminar en medio
    insertaFinal(30); // Insertamos un nuevo elemento para tener una lista con más de un nodo
    insertaFinal(40);
    imprimirLista();
    borraMedio(buscarElemento(30));
    printf("Lista después de borrar en medio: ");
    imprimirLista();

    insertaInicio(77);
    printf("Lista después de insertar 77 al inicio: ");
    imprimirLista();

    insertaMedio(78, buscarElemento(77));
    printf("Lista después de insertar 78 en medio: ");
    imprimirLista();

    borraInicio();
    printf("Lista después de borrar al inicio: ");
    imprimirLista();

    insertaMedio(81, buscarElemento(40));
    printf("Lista después de insertar 81 en medio: ");
    imprimirLista();

    borraMedio(buscarElemento(15));
    printf("Lista después de borrar en medio: ");
    imprimirLista();

    borraMedio(buscarElemento(78));
    printf("Lista después de borrar en medio: ");
    imprimirLista();

    borraMedio(buscarElemento(81));
    printf("Lista después de borrar en medio: ");
    imprimirLista();

    return 0;
}