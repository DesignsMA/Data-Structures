## Importación de clases y estructuras necesarias desde otros archivos
from Clases import * # Necesita __init__.py para funcionar
from Estructuras import *
from Scripts.PolinomioDireccionamiento import polinomio_direccionamiento

#Definicion de la clase principal para gestionar la sistencia 
class GestionAyuda(): #Gestionar la asistencia a personas indocumentadas desplazadas
    #Variables de clase, compartidas entre clases
    
    """
    Sistema de Gestión de Ayuda para Indocumentados Desplazados
    
    Atributos de clase:
        atendidos (int): Número de indocumentados atendidos
    
    Atributos de instancia:
        registros (Cola): descripcion y uso
        urgentes (Pila):
        recursos (Lista):
        asignaciones (ListaDoble):
        seguimientos (ListaCircular):
    """
    atendidos = 0 # variable de clase, representa el total de personas atendidas 
    tipos = {0: "Alimentos", 1: "Refugios", 2: "Asesoría Legal"} #tipos de ayuda disponibles

    def __init__(self):
        """Sistema de Gestión de Ayuda para Indocumentados Desplazados"""
        #Variables de instancia, unicas de instancia
        self.registros = Cola() # Instancia de cola lineal
        self.urgentes = Pila() # Instancia de pila
        self.recursos = Lista() # Instancia de lista
        self.asignaciones = ListaDoble() # Instancia de lista doble
        self.seguimientos = ListaCircular() # Instancia de lista circular
        
        #Inicializando recursos, se tiene 0 disponibles de cada tipo
        #Cada recurso tiene una variable para, cantidad disponible, usados
        
        self.recursos.insertEnd( Recurso(0,0) ) #Alimentos
        self.recursos.insertEnd( Recurso(1,0) ) #Refugios 
        self.recursos.insertEnd( Recurso(2,0) ) #Asesoria legal

    def registrar(self): # Se le tiene que preguntar al usuario la persona
        """
        Registra una persona indocumentada y la coloca en una cola o pila dependiendo
        de su urgencia.
        """
        nombre=input("ingrese el nombre: ")
        motivo=input("ingrese el motivo de la repatriación: ")
        nacionalidad=input("ingrese la nacionalidad: ")
        prioridad =  int( input("Ingrese la urgencia:\nRegular 0 | Urgente 1: ") )
        persona = None #Se inicializa la variable persona
        print(prioridad)
        
        try:
            #Se crea una nueva instancia de Persona
            persona = Persona(nombre, nacionalidad, motivo, prioridad) # Generar una instancia de la clase persona
        except ValueError as e:
            print(e) #Manejo de error si los datos no son validos 
            return False
        # Solo ejecuta si no hay error
        if prioridad == 0: # caso regular se manda a cola
            self.registros.encolar(persona)
            print(self.registros)
        elif prioridad == 1: # caso urgente, va a la pila
            self.urgentes.push(persona)
            self.urgentes.show()

    
        # Administrador añade recursos a las variables de instancia
    def gestionarRecursos(self):
        """Añade recursos del tipo seleccionado por el usuario"""
        print("0 - Alimentos | 1 - Refugios | 2 - Asesoría Legal")
        tipo = int( input("Ingresa que tipo de recurso se va agregar: ") )
        
        if tipo in [0,1,2]:
            
            try:
                cantidad = int( input(f"¿Cuantos nuevos recursos de tipo {self.tipos[tipo]} quieres agregar?: ") )
                res = self.recursos.get_element_at( tipo )

                if isinstance(res, Recurso): # si es un recurso
                    res.agregar(cantidad)
                    
            except ValueError:
                print("La cantidad era erronea, no fue añadido nada.")
        
            print(self.recursos.get_element_at( tipo ))
            
        else:
            print("Ese tipo no es valido.")
    
    def atender(self):
        """
        Atiende a una persona registrada, primero a las que tengan una prioridad urgente
        (Pila), si la pila esta vacia, atiende a las que tengan una prioridad regular (Cola)
        
        Ademas, asigna recursos a esa persona ( Alimentos, refugios, asesoría legal)
        
        En el caso de que la persona necesite asesoría legal, e abre un proceso legal
        pendiente de resolver.
        """
        
        persona = Persona
        try:
            if self.urgentes.empty() == False: # si hay personas urgentes
                persona = self.urgentes.pop() #remueve y retorna
            else:
                persona = self.registros.desencolar() #remueve y retorna
        except IndexError as e:
            print(e)
        
        print(persona.datosBasicos())
        x = int( input("¿Que atención necesita?\n\
        0 - Alimentos | 1 - Refugios | 2 - Asesoría Legal") )
        
        if x in  [0,1,2]:
            res = self.recursos.get_element_at( x )
            try:
                if isinstance(res, Recurso): # si es un recurso
                    res.usar(1)
            except ValueError:
                print("No hay recursos disponibles.")
                
            asignacion = Asignacion(res.tipo, persona, 1) # se crea  un historial de recursos  asignados
            print(asignacion)
            self.asignaciones.insertStart( asignacion )
            
            if x == 2: # caso de proceso legal                
                caso = ProcesoLegal(persona)
                print(caso)
                self.seguimientos.insertStart(caso)
                
        else:
            print("Ese tipo no es valido.")
        


sistema = GestionAyuda()
sistema.gestionarRecursos()
sistema.gestionarRecursos()
sistema.registrar()
sistema.atender()
            
        
        
   
        
            
            
        