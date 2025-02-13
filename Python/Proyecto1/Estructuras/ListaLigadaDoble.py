from ..Clases.NodoDoble import *
class ListaDoble:
    def __init__(self):
        self.root = None  # La lista empieza vacía
        self.tail = None  # La cola también empieza vacía

    def insertEnd(self, data):
        """Inserta un NodoDoble al final de la lista."""
        new = NodoDoble(data)

        if self.root is None:
            self.root = self.tail = new  # Si la lista está vacía, el nuevo NodoDoble es la raíz y la cola
        else:
            self.tail.sig = new  # El último NodoDoble apunta al nuevo NodoDoble
            new.ant = self.tail  # El nuevo NodoDoble apunta al NodoDoble anterior (cola)
            self.tail = new  # La cola se actualiza al nuevo NodoDoble

    def insertStart(self, data):
        """Inserta un NodoDoble al inicio de la lista."""
        new = NodoDoble(data)
        if self.root is None:
            self.root = self.tail = new  # Si la lista está vacía, el nuevo NodoDoble es la raíz y la cola
        else:
            new.sig = self.root  # El nuevo NodoDoble apunta al NodoDoble raíz
            self.root.ant = new  # El NodoDoble raíz apunta al nuevo NodoDoble
            self.root = new  # La raíz se actualiza al nuevo NodoDoble
    
    def insertBetween(self, prev_data, data):
        """Inserta un NodoDoble después de un NodoDoble con el valor prev_data."""
        aux = self.root
        while aux is not None and aux.data != prev_data:
            aux = aux.sig
        
        if aux is None:
            print("Elemento previo no encontrado.")
        else:
            new = NodoDoble(data)
            new.sig = aux.sig  # El nuevo NodoDoble apunta al siguiente NodoDoble
            if aux.sig is not None:  # Si no estamos insertando al final
                aux.sig.ant = new  # El siguiente NodoDoble apunta al nuevo NodoDoble
            aux.sig = new  # El NodoDoble previo apunta al nuevo NodoDoble
            new.ant = aux  # El nuevo NodoDoble apunta al NodoDoble previo
    
    def remove(self, data: str): 
        """Elimina un NodoDoble con el valor dado."""
        if self.root is None:
            print("Lista vacía.")
            return
      
        if self.root.data == data or data == "inicio":
            self.root = self.root.sig
            if self.root:  # Si no es el último NodoDoble
                self.root.ant = None
            return
            
        aux = self.root
        if data != "final":
            while aux.sig is not None and aux.sig.data != data:
                aux = aux.sig
        elif data == "final":
            while aux.sig.sig is not None:  # Recorrer hasta el penúltimo
                aux = aux.sig
        
        if aux.sig is None:
            print("Elemento no encontrado.")
        else:
            if aux.sig.sig is not None:
                aux.sig.sig.ant = aux  # El siguiente NodoDoble apunta al NodoDoble anterior
            aux.sig = aux.sig.sig  # El NodoDoble anterior apunta al siguiente de su siguiente
    
    def exists(self, data):
        """Verifica si un elemento está en la lista."""
        aux = self.root
        while aux is not None:
            if aux.data == data:
                return True
            aux = aux.sig
        return False
    
    def print(self):
        """Imprime la lista completa."""
        current = self.root
        while current is not None:
            print(current.data, end=" <-> ")
            current = current.sig
        print("None")

def interact():
    # Interacción con el usuario
    lista = ListaDoble()
    while True:
        lista.print()
        print("\n1. Insertar al inicio\n2. Insertar al final\n3. Insertar entre elementos\n4. Eliminar\n5. Buscar\n6. Mostrar lista\n7. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            valor = input("Ingresa el valor a insertar al inicio: ")
            lista.insertStart(valor)
        elif opcion == "2":
            valor = input("Ingresa el valor a insertar al final: ")
            lista.insertEnd(valor)
        elif opcion == "3":
            prev_valor = input("Ingresa el valor del NodoDoble previo: ")
            valor = input("Ingresa el valor a insertar: ")
            lista.insertBetween(prev_valor, valor)
        elif opcion == "4":
            valor = input("Ingresa el valor a eliminar | escribe inicio o final para borrar en esa posicion: ")
            lista.remove(valor)
        elif opcion == "5":
            valor = input("Ingresa el valor a buscar: ")
            print("Encontrado" if lista.exists(valor) else "No encontrado")
        elif opcion == "6":
            lista.print()
        elif opcion == "7":
            break
        else:
            print("Opción inválida, intenta de nuevo.")