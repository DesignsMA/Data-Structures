class Nodo:
    def __init__(self, data):
        self.data = data  # Dato del nodo
        self.sig = None   # Referencia al siguiente nodo
        self.ant = None   # Referencia al nodo anterior

class ListaDoble:
    def __init__(self):
        self.root = None  # La lista empieza vacía
        self.tail = None  # La cola también empieza vacía

    def insertEnd(self, data):
        """Inserta un nodo al final de la lista."""
        new = Nodo(data)

        if self.root is None:
            self.root = self.tail = new  # Si la lista está vacía, el nuevo nodo es la raíz y la cola
        else:
            self.tail.sig = new  # El último nodo apunta al nuevo nodo
            new.ant = self.tail  # El nuevo nodo apunta al nodo anterior (cola)
            self.tail = new  # La cola se actualiza al nuevo nodo

    def insertStart(self, data):
        """Inserta un nodo al inicio de la lista."""
        new = Nodo(data)
        if self.root is None:
            self.root = self.tail = new  # Si la lista está vacía, el nuevo nodo es la raíz y la cola
        else:
            new.sig = self.root  # El nuevo nodo apunta al nodo raíz
            self.root.ant = new  # El nodo raíz apunta al nuevo nodo
            self.root = new  # La raíz se actualiza al nuevo nodo
    
    def insertBetween(self, prev_data, data):
        """Inserta un nodo después de un nodo con el valor prev_data."""
        aux = self.root
        while aux is not None and aux.data != prev_data:
            aux = aux.sig
        
        if aux is None:
            print("Elemento previo no encontrado.")
        else:
            new = Nodo(data)
            new.sig = aux.sig  # El nuevo nodo apunta al siguiente nodo
            if aux.sig is not None:  # Si no estamos insertando al final
                aux.sig.ant = new  # El siguiente nodo apunta al nuevo nodo
            aux.sig = new  # El nodo previo apunta al nuevo nodo
            new.ant = aux  # El nuevo nodo apunta al nodo previo
    
    def remove(self, data: str): 
        """Elimina un nodo con el valor dado."""
        if self.root is None:
            print("Lista vacía.")
            return
      
        if self.root.data == data or data == "inicio":
            self.root = self.root.sig
            if self.root:  # Si no es el último nodo
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
                aux.sig.sig.ant = aux  # El siguiente nodo apunta al nodo anterior
            aux.sig = aux.sig.sig  # El nodo anterior apunta al siguiente de su siguiente
    
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

# Interacción con el usuario
lista = ListaDoble()
while True:
    print("\n1. Insertar al inicio\n2. Insertar al final\n3. Insertar entre elementos\n4. Eliminar\n5. Buscar\n6. Mostrar lista\n7. Salir")
    opcion = input("Elige una opción: ")
    
    if opcion == "1":
        valor = input("Ingresa el valor a insertar al inicio: ")
        lista.insertStart(valor)
    elif opcion == "2":
        valor = input("Ingresa el valor a insertar al final: ")
        lista.insertEnd(valor)
    elif opcion == "3":
        prev_valor = input("Ingresa el valor del nodo previo: ")
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
