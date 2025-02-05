#include <stdio.h>
#include <malloc.h>

typedef struct nodo {
	int dato;
	struct nodo *sig;
}NODO;

	void imprimeLista(NODO *ap){
		while(ap!=NULL) {
			printf("\nDato: %d", ap->dato);
			ap=ap->sig;
		}
		printf("\nFin\n\n");
	} 

	NODO *creaNodo (int dato) {
		NODO *nuevo;
		nuevo=(NODO *)malloc(sizeof(NODO));
		if (nuevo != NULL) {
			nuevo->dato=dato;
			nuevo->sig=NULL;
		}
		return nuevo;
	}

	NODO *eliminaNodo (NODO *raiz, int dato) { 
    NODO *aux, *ant;
    if ( raiz != NULL ) {
        aux = raiz;
        if (raiz->dato == dato) {
            raiz=raiz->sig;
            free(aux);
        }
        else {
            aux = raiz;
            ant = raiz;
            while ( aux != NULL ) {
                if ( aux->dato == dato ) break;
                ant = aux;
                aux = aux->sig;
            }
            if ( aux == NULL ) return NULL;
            ant->sig=aux->sig;
            free(aux);
        }
    }
    return raiz;
}

	
	NODO *insertaFinal(NODO *ap, int d) {
		NODO *aux, *nuevo;
		
		nuevo=creaNodo(d);
		if (nuevo == NULL) return ap;
		if (ap==NULL) {
			ap=nuevo;
		}
		else {
			aux=ap;
			while(aux->sig != NULL) {
				aux=aux->sig;
			}	
			aux->sig=nuevo;
		}
		return ap;
	}
	
	NODO *insertaAlInicio(NODO *ap, int d) {
		NODO *aux, *nuevo;
		
		nuevo=creaNodo(d);
		if (nuevo == NULL) return ap;
		aux=ap;
		ap=nuevo;
		nuevo->sig=aux;
		return ap;
	}
	
	int cuentaNodos(NODO *ap){
		int c;
		
		c=0;
		while (ap!=NULL) {
			ap=ap->sig;
			c++;
		}
		return c;
	}
		
	int main() {
		NODO *raiz, *raiz1;
	
		printf("\n Primera lista");
		raiz=NULL;
		raiz=insertaFinal(raiz,3);			
		raiz=insertaFinal(raiz,87);
		raiz=insertaFinal(raiz,88);
		raiz=insertaFinal(raiz,-83);
		raiz=insertaFinal(raiz,54);
		raiz=insertaFinal(raiz,-21); 
		raiz=insertaAlInicio(raiz, 0);
		imprimeLista(raiz);
		printf("\n Numero de nodos: %d", cuentaNodos(raiz));	
		
		printf("\n Segunda lista");
		raiz1=NULL;
		raiz1=insertaAlInicio(raiz1, 5);
		raiz1=insertaAlInicio(raiz1, 6);
		raiz1=insertaAlInicio(raiz1, 7);
		raiz1=insertaFinal(raiz1,8);
		imprimeLista(raiz1);
		printf("\n Numero de nodos: %d", cuentaNodos(raiz1));	
		return 0;
	}
		
