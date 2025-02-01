#include <stdio.h>
#include <stdlib.h>
#include <string.h>


struct ElementoPila {
    char simbolo;
    struct ElementoPila *sig;
};

struct ElementoPila *tope=NULL;

void push(char x)
{
    struct ElementoPila *nuevo;
    nuevo = malloc(sizeof(struct ElementoPila));
    nuevo->simbolo = x;
    if (tope == NULL)
    {
        tope = nuevo;
        nuevo->sig = NULL;
    }
    else
    {
        nuevo->sig = tope;
        tope = nuevo;
    }
}


char pop()
{
    if (tope != NULL)
    {
        char info= tope->simbolo;
        struct ElementoPila *ElementoAEliminar = tope;
        tope = tope->sig;
        free(ElementoAEliminar);
        return info;
    }
    else
    {
        return -1;
    }
}

void liberar()
{
    struct ElementoPila *recorrer = tope;
    struct ElementoPila *ElementoAEliminar;
    while (recorrer != NULL)
    {
        ElementoAEliminar = recorrer;
        recorrer = recorrer->sig;
        free(ElementoAEliminar);
    }
}

int PilaVacia()
{
    if (tope == NULL)
        return 1;
    else
        return 0;
}

void CargarExpresion(char *expresion)
{
    printf("Ingrese la Expresion:");
    //leer cadena con un limite de sizeof(expresion) en el stream stdin
    fgets(expresion, sizeof(expresion), stdin);
}

int verificar(char *expresion)
{
    int i;
    for (i=0;i<strlen(expresion);i++)
    {
        if (expresion[i]=='(' || expresion[i]=='[' || expresion[i]=='{')
        {
            push(expresion[i]);
        }
        else
        {
            if (expresion[i]==')')
            {
                if (pop()!='(')
                {
                    return 0;
                }
            }
            else
            {
                if (expresion[i]==']')
                {
                    if (pop()!='[')
                    {
                        return 0;
                    }
                }
                else
                {
                    if (expresion[i]=='}')
                    {
                        if (pop()!='{')
                        {
                            return 0;
                        }
                    }
                }
            }
        }
    }
    if (PilaVacia())
    {
        return 1;
    }
    else
    {
        return 0;
    }
}


int main()
{
    char expresion[100];
    CargarExpresion(expresion);
    if (verificar(expresion))
    {
        printf("si esta balanceada");
    }
    else
    {
        printf("no esta balanceada");
    }
    liberar();
    getchar();
    return 0;
}