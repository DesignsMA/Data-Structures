# Importación de clases y estructuras necesarias desde otros archivos
from Clases import * # Necesita __init__.py para funcionar
from Estructuras import *
from Scripts.PolinomioDireccionamiento import polinomio_direccionamiento
from datetime import datetime # Libreria  de fechas
import os

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
        nombre=input("\bIngrese el nombre: ")
        motivo=input("Ingrese el motivo de la repatriación: ")
        nacionalidad=input("Ingrese la nacionalidad: ")
        prioridad =  int( input("Ingrese la urgencia:\nRegular 0 | Urgente 1: ") )
        persona = None #Se inicializa la variable persona
        
        try:
            #Se crea una nueva instancia de Persona
            persona = Persona(nombre, nacionalidad, motivo, prioridad) # Generar una instancia de la clase persona
        except ValueError as e:
            print(e) #Manejo de error si los datos no son validos 
            return False
        # Solo ejecuta si no hay error
        if prioridad == 0: # caso regular se manda a cola
            self.registros.encolar(persona)
            print("\n", self.registros.show())
        elif prioridad == 1: # caso urgente, va a la pila
            self.urgentes.push(persona)
            print("\n", self.urgentes.show())

    
        # Administrador añade recursos a las variables de instancia
    def gestionarRecursos(self):
        """Añade recursos del tipo seleccionado por el usuario"""
        print("\n0 - Alimentos | 1 - Refugios | 2 - Asesoría Legal\n")
        tipo = int( input("Ingresa que tipo de recurso se va agregar: ") )
        
        if tipo in [0,1,2]: #Verifica que el tipo de recurso se valido
            
            try:
                cantidad = int( input(f"\n¿Cuantos nuevos recursos de tipo {self.tipos[tipo]} quieres agregar?: ") )
                res = self.recursos.get_element_at( tipo ) #Obtiene el recurso correspondiente

                if isinstance(res, Recurso): # si es un recurso
                    res.agregar(cantidad) #Agrega la cantidad especificada 
                    
            except ValueError:
                print("La cantidad era erronea, no fue añadido nada.")
        
            print(f"Recurso modificado:\n{self.recursos.get_element_at( tipo )}\n") # imprimiendo el recurso modificado
            
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


            print(f"Atendiendo a:\n{persona.datosBasicos()}", end="\n\n")
            
            print(f"{self.recursos.get_element_at(0)}\n{self.recursos.get_element_at(1)}\n{self.recursos.get_element_at(2)}\n")

            x = int( input("¿Que atención necesita?\n0 - Alimentos | 1 - Refugios | 2 - Asesoría Legal\n: ") )

            if x in  [0,1,2]: # si es un recurso valido
                res = self.recursos.get_element_at( x )
                try:
                    if isinstance(res, Recurso): # si es un recurso
                        res.usar(1)
                except ValueError:
                    print(f"No hay recursos disponibles\n\n{persona.datosBasicos()}\nFue formado de nuevo como prioritario.")
                    persona.prioridad = "Urgente"
                    self.urgentes.push(persona)
                    return

                asignacion = Asignacion(res.tipo, persona, 1) # se crea  un historial de recursos  asignados
                print(asignacion) #Muestra la asignacion realizada
                self.asignaciones.insertStart( asignacion ) # Guarda la asignacion en la lista doble

                if x == 2: # caso de proceso legal                
                    caso = ProcesoLegal(persona) # iniciar proceso legal
                    print(caso)
                    self.seguimientos.insertStart(caso) # insertar en lista de seguimientos

                self.atendidos += 1
            else:
                print("Ese tipo no es valido.")
        except IndexError as e:
            print(e) # Si esta vacia
             
    def seguimiento(self):
        if not self.seguimientos.empty():
            self.seguimientos.current = self.seguimientos.root # inicializar caso actual
            CasoLegal = self.seguimientos.current.data	#guardamos en una variable el dato del nodo
            while True:
                if isinstance(CasoLegal, ProcesoLegal): # si es un proceso legal
                    print(CasoLegal)
                    print("1. Completar caso\n2. Siguiente caso\n-1. Salir")
                    opt = input("seleccione una opción: ")
                    if opt == '1':
                        # En el caso actual, donde  el actual inicia en la raiz
                        CasoLegal.resolverCaso() # resolver el caso actual
                    elif opt=='2':
                        self.seguimientos.next() 
                        CasoLegal = self.seguimientos.current.data # se actualiza la variable
                        #Recorre al siguiente caso
                    elif opt=='-1': # salir del menu
                        break
        else:
            print("No hay casos registrados hoy.")
                    
                    
    def generarReporte(self):
        fecha = datetime.now().strftime("%Y-%m-%d")  # Formato: Año-Mes-Día #obtener la cadena de la fecha actual
        ruta_archivo = os.path.join("Reportes", f"Reporte-Semanal-{fecha}.txt")
        file = open(ruta_archivo, "w+", encoding="UTF-8") #modo de escritura, siempre es un reporte diferente
        file.write(f"----Reporte Semanal | {fecha}----\n") # cabezera del reporte
        file.write(f"\nPersonas atendidas = {self.atendidos}\n") # numero de personas atendidas
        
        file.write(f"""
----Recursos usados----
{self.recursos.get_element_at(0).__str__()} 
{self.recursos.get_element_at(1).__str__()}
{self.recursos.get_element_at(2).__str__()}
""")

        file.write("\n----Casos Legales---\n")
        if not self.seguimientos.empty():
            self.seguimientos.current = self.seguimientos.root # mover actual al inicio
            CasoLegal = self.seguimientos.current.data # obtener el caso actual
            bol = True
            if isinstance(CasoLegal, ProcesoLegal) and CasoLegal is not None:
                while( CasoLegal !=  self.seguimientos.root.data or bol):
                    if bol:
                        bol = False #indicar que no es la primera vez que se recorre
                        
                    file.write(f"{CasoLegal}\n") # se escribe el caso
                    self.seguimientos.next() # siguiente caso
                    CasoLegal = self.seguimientos.current.data
        
        print(file.read()) #imprimir reporte
        file.close()
        
        
                        
#Menú principal
def menu():
    sistema = GestionAyuda()
    while True:
        print("\n---MENU PRINCIPAL---")    
        print("1. Registrar persona")
        print("2. Gestionar recursos")
        print("3. Atender y asignar recurso")
        print("4. Revisar seguimiento de casos")
        print("5. Obtener reporte semanal")
        print("6. Historial de asignaciones")
        print("7. Salir")
        
        opt= input("\nSeleccione una opcion: ")
        
        if opt == '1':
            sistema.registrar()
        elif opt == '2':
            sistema.gestionarRecursos()
        elif opt == '3':
            sistema.atender()
        elif opt == '4':
            sistema.seguimiento()
        elif opt == '5':
            sistema.generarReporte()
        elif opt == '6':
            sistema.asignaciones.print()
        elif opt == '7':
            print("Saliendo ...\n")
            break            
        else: 
            print("Opcion no valida")
    
#Instancia de la clase 

menu()
            
        
        
   
        
            
            
        