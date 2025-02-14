class Pila():
    
    def _init_(self,size):
        self.lista=[]
        self.tope=0
        self.size=size
        
    def empty(self):
        if self.tope==0:
            return True
        else:
            return False
        
    def push(self,dato):
        if self.tope<self.size:
            self.lista.append(dato)
            self.tope+=1
        else:
            self.size+=5
            self.lista.append(dato)
            self.tope+=1
           
            
    def pop(self):
        if self.empty():
            print("lista vacía")
        else:
            self.lista.pop()# Si no especificas el índice del elemento a eliminar de la lista, la función pop() eliminará por defecto el último elemento de la lista.
            self.tope-=1
            
    def show(self):
        i=self.tope-1
        while i>-1:
            print("[%d] -> %d" %(i,self.lista[i]))
            i-=1
            
            
    def Size(self):
        return self.tope
    
    def top(self):
       if self.empty():
        print("no hay elementos, esta vacía")
       else:
           return self.lista[-1]