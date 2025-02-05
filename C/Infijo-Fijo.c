#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>  // Para usar isdigit

typedef struct {
    char *datos;
    int tope;
    int capacidad;
} Pila;

void inicializar(Pila *stack) {
    stack->datos = (char*)malloc(sizeof(char));
    if (stack->datos == NULL) {
        printf("\nError al reservar espacio.\n");
        exit(EXIT_FAILURE);
    }
    stack->tope = -1; // La pila está vacía
    stack->capacidad = 1;
}

int estaVacia(Pila *stack) {
    return stack->tope == -1;
}

void push(Pila *stack, char var) {
    if (stack->tope == (stack->capacidad - 1)) {
        stack->capacidad *= 2;
        stack->datos = (char*)realloc(stack->datos, stack->capacidad * sizeof(char));
        if (stack->datos == NULL) {
            printf("\nError al reservar espacio.\n");
            exit(EXIT_FAILURE);
        }
    }
    stack->datos[++stack->tope] = var;
}

char pop(Pila *stack) {
    if (estaVacia(stack)) {
        printf("La pila se encuentra vacía\n");
        exit(EXIT_FAILURE);
    }
    return stack->datos[stack->tope--];
}

char verTope(Pila *stack) {
    if (estaVacia(stack)) {
        printf("La pila se encuentra vacía\n");
        exit(EXIT_FAILURE);
    }
    return stack->datos[stack->tope];
}

int precedencia(char op) {
    switch (op) {
        case '+':
        case '-':
            return 1;
        case '*':
        case '/':
            return 2;
        default:
            return 0;
    }
}

void infijaAPostfija(char cad[]) {
    int i = 0, u = 0;
    char resultado[100];
    Pila stack;
    inicializar(&stack);

    while (cad[i] != '\0') {
        if (isdigit(cad[i])) {  // Si es un dígito, se agrega al resultado
            resultado[u++] = cad[i];
        } else if (cad[i] == '(') {  // Si es un paréntesis de apertura, se apila
            push(&stack, cad[i]);
        } else if (cad[i] == ')') {  // Si es un paréntesis de cierre, se desapila hasta encontrar '('
            while (!estaVacia(&stack) && verTope(&stack) != '(') {
                resultado[u++] = pop(&stack);
            }
            if (!estaVacia(&stack) && verTope(&stack) == '(') {
                pop(&stack);  // Sacar el '(' de la pila
            }
        } else if (cad[i] == '+' || cad[i] == '-' || cad[i] == '*' || cad[i] == '/') {
            // Si es un operador, se desapila mientras haya operadores con mayor o igual precedencia
            while (!estaVacia(&stack) && precedencia(verTope(&stack)) >= precedencia(cad[i])) {
                resultado[u++] = pop(&stack);
            }
            push(&stack, cad[i]);  // Se apila el operador actual
        }
        i++;
    }

    // Vaciar la pila y agregar los operadores restantes al resultado
    while (!estaVacia(&stack)) {
        resultado[u++] = pop(&stack);
    }

    resultado[u] = '\0';  // Terminar la cadena resultado
    printf("\nExpresion postfija: %s\n", resultado);

    free(stack.datos);  // Liberar memoria ocupada por la pila
}
/*
Pila:

Se utiliza una pila para almacenar operadores y paréntesis durante la conversión.

Recorrido de la cadena:

Se recorre la cadena de entrada carácter por carácter.

Si es un dígito, se agrega directamente al resultado.

Si es un paréntesis de apertura (, se apila.

Si es un paréntesis de cierre ), se desapila y se agrega al resultado hasta encontrar el paréntesis de apertura correspondiente.

Si es un operador (+, -, *, /), se desapilan los operadores con mayor o igual precedencia y se apila el operador actual.

Finalización:

Al final, se vacía la pila y se agregan los operadores restantes al resultado.
*/

int main() {
    char cadena[100];

    printf("Introduce una expresion infija: ");
    scanf("%s", cadena);  // Leer una cadena
    infijaAPostfija(cadena);

    return 0;
}