from ..Clases.Nodo import *
class ListaCircular:
    def __init__(self):
        self.root = None  # La lista empieza vacía
        self.current = None  # Nodo actual para recorrer
    
    def insertEnd(self, data):
        """Inserta un nodo al final de la lista."""
        new = Nodo(data)
        if self.root is None:
            self.root = new
            self.root.sig = self.root  # Apunta a sí mismo
        else:
            aux = self.root
            while aux.sig != self.root:  # Recorrer hasta el final
                aux = aux.sig
            aux.sig = new
            new.sig = self.root  # Apuntar al inicio
    
    def insertStart(self, data):
        """Inserta un nodo al inicio de la lista."""
        new = Nodo(data)
        if self.root is None:
            self.root = new
            self.root.sig = self.root
        else:
            aux = self.root
            while aux.sig != self.root:  # Buscar el último nodo
                aux = aux.sig
            new.sig = self.root
            self.root = new
            aux.sig = self.root  # Ajustar el último nodo
    
    def insertBetween(self, data, position):
        """Inserta un nodo en una posición específica de la lista."""
        if position < 0:
            print("Posición inválida.")
            return
        new = Nodo(data)
        if position == 0:
            self.insertStart(data)
            return
        aux = self.root
        count = 0
        while count < position - 1:
            aux = aux.sig
            count += 1
            if aux == self.root:
                print("Posición fuera de rango.")
                return
        new.sig = aux.sig
        aux.sig = new
    
    def deleteStart(self):
        """Elimina el nodo al inicio de la lista."""
        if self.root is None:
            print("Lista vacía.")
            return
        if self.root.sig == self.root:  # Solo hay un nodo
            self.root = None
        else:
            aux = self.root
            while aux.sig != self.root:  # Buscar el último nodo
                aux = aux.sig
            self.root = self.root.sig
            aux.sig = self.root
    
    def deleteEnd(self):
        """Elimina el nodo al final de la lista."""
        if self.root is None:
            print("Lista vacía.")
            return
        if self.root.sig == self.root:  # Solo hay un nodo
            self.root = None
        else:
            aux = self.root
            prev = None
            while aux.sig != self.root:  # Buscar el último nodo
                prev = aux
                aux = aux.sig
            prev.sig = self.root
    
    def deleteBetween(self, position):
        """Elimina un nodo en una posición específica de la lista."""
        if self.root is None:
            print("Lista vacía.")
            return
        if position < 0:
            print("Posición inválida.")
            return
        if position == 0:
            self.deleteStart()
            return
        aux = self.root
        count = 0
        while count < position - 1:
            aux = aux.sig
            count += 1
            if aux.sig == self.root:
                print("Posición fuera de rango.")
                return
        if aux.sig == self.root:
            print("Posición fuera de rango.")
            return
        aux.sig = aux.sig.sig
    
    def print(self):
        """Imprime la lista circular."""
        if self.root is None:
            print("Lista vacía.")
            return
        aux = self.root
        while True:
            print(aux.data, end=" -> ")
            aux = aux.sig
            if aux == self.root:
                break
        print("(circular)")
    
    def get_element_at(self, n):
        """
        Retorna el elemento en la posición n (empezando desde 0).
        Si la posición no existe, retorna None.
        """
        if self.root is None:
            print("Lista vacía.")
            return None

        aux = self.root
        pos = 0
        while aux is not None:
            if pos == n:  # Si se encuentra la posición
                return aux.data
            aux = aux.sig  # Avanzar al siguiente nodo
            pos += 1

        print(f"La posición {n} no existe en la lista.")
        return None
    
    def printOne(self):
        """Imprime un nodo por vez, recorriendo en cada llamada."""
        if self.root is None:
            print("Lista vacía.")
            return
        if self.current is None:
            self.current = self.root
        print(self.current.data)
        self.current = self.current.sig

def interact():
    # Interacción con el usuario
    lista = ListaCircular()
    while True:
        lista.print()
        print("\n1. Insertar al inicio\n2. Insertar al final\n3. Insertar en posición\n4. Eliminar al inicio\n5. Eliminar al final\n6. Eliminar en posición\n7. Mostrar lista completa\n8. Mostrar un nodo\n9. Salir")
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            valor = input("Ingresa el valor a insertar al inicio: ")
            lista.insertStart(valor)
        elif opcion == "2":
            valor = input("Ingresa el valor a insertar al final: ")
            lista.insertEnd(valor)
        elif opcion == "3":
            valor = input("Ingresa el valor a insertar: ")
            posicion = int(input("Ingresa la posición: "))
            lista.insertBetween(valor, posicion)
        elif opcion == "4":
            lista.deleteStart()
        elif opcion == "5":
            lista.deleteEnd()
        elif opcion == "6":
            posicion = int(input("Ingresa la posición a eliminar: "))
            lista.deleteBetween(posicion)
        elif opcion == "7":
            lista.print()
        elif opcion == "8":
            lista.printOne()
        elif opcion == "9":
            break
        else:
            print("Opción inválida, intenta de nuevo.")