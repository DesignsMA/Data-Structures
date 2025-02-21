class Nodo:
    def __init__(self, data):
        self.data = data  # Dato del nodo
        self.sig = None   # Referencia al siguiente nodo
        
class Lista:
    def __init__(self):
        self.root = None  # La lista empieza vacía

    def insertEnd(self, data):
        """Inserta un nodo al final de la lista."""
        new = Nodo(data)

        if self.root is None:
            self.root = new  # Si la lista está vacía, el new nodo es la raíz
        else:
            aux = self.root
            while aux.sig is not None:  # Recorrer hasta el final
                aux = aux.sig
            aux.sig = new  # Insertar al final

    def insertStart(self, data):
        """Inserta un nodo al inicio de la lista."""
        new = Nodo(data)
        new.sig = self.root
        self.root = new
    
    def insertBetween(self, prev_data, data):
        """Inserta un nodo después de un nodo con el valor prev_data."""
        aux = self.root
        while aux is not None and aux.data != prev_data:
            aux = aux.sig
        
        if aux is None:
            print("Elemento previo no encontrado.")
        else:
            new = Nodo(data)
            new.sig = aux.sig
            aux.sig = new
    
    def remove(self, data: str): #elimina un elemento en cualquier posicion
        """Elimina un nodo con el valor dado."""
        if self.root is None:
            print("Lista vacía.")
            return
      
        if self.root.data == data or data == "inicio":
            self.root = self.root.sig
            return
            
        aux = self.root
        if data != "final":
            while aux.sig is not None and aux.sig.data != data:
                aux = aux.sig
        elif data == "final":
            while aux.sig.sig is not None:  # Recorrer hasta el penultimo
                aux = aux.sig
        
        if aux.sig is None:
            print("Elemento no encontrado.")
        else:
            aux.sig = aux.sig.sig
                
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
            print(current.data, end=" -> ")
            current = current.sig
        print("None")
    
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
    
    def __str__(self):
        """Retorna una cadena que representa la lista enlazada."""
        current = self.root
        result = ""
        while current is not None:
            result += str(current.data) + " -> "
            current = current.sig
        result += "None"
        return result
    
def interact():
    # Interacción con el usuario
    lista = Lista()
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
            