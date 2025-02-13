# Sistema de Gestión de Personas y Recursos

Este proyecto implementa un sistema de gestión para registrar personas, asignar recursos y realizar seguimiento de casos utilizando diversas estructuras de datos como colas, pilas, listas enlazadas y listas circulares.

## Funcionalidades Principales

### 1. Registro de Personas (Colas y Listas Circulares)
- Se utiliza una **cola** para registrar a las personas en orden de llegada.
- Si la cola debe ser circular (para atender de manera cíclica), se implementa una **lista enlazada circular**.

### 2. Atención Prioritaria (Pilas)
- Cuando una persona se clasifica como "urgente", se mueve de la cola a una **pila**, donde será atendida antes que los demás.

### 3. Gestión de Recursos (Listas Simples y Dobles)
- Se usa una **lista enlazada simple** para almacenar los recursos disponibles.
- Al asignar un recurso, se elimina de la lista y se registra en una **lista doblemente enlazada** para mantener un historial.

### 4. Seguimiento de Casos (Lista Circular)
- Para los casos que requieren seguimiento (como asesoría legal en varias etapas), se usa una **lista circular** para recorrer los registros sin llegar a un final.

### 5. Reportes Semanales
- Se implementan funciones para generar reportes sobre:
  - Número de personas atendidas.
  - Recursos asignados y utilizados.
  - Casos resueltos y pendientes.

---

## ¿Cómo empezar?

### 1. Define las clases base
- **Persona**: `nombre`, `ID`, `nacionalidad`, `prioridad`, etc.
- **Recurso**: `tipo`, `cantidad disponible`.
- **Nodo**: para listas, pilas y colas.

### 2. Implementa las estructuras de datos
- Colas.
- Pilas.
- Listas enlazadas (simples, dobles y circulares).

### 3. Desarrolla las funciones de asignación y seguimiento
- Funciones para mover personas entre colas y pilas.
- Funciones para asignar recursos y registrar en el historial.
- Funciones para recorrer listas circulares.

### 4. Prueba con datos simulados y ajusta el comportamiento
- Simula el registro de personas, la asignación de recursos y el seguimiento de casos.
- Ajusta el comportamiento según los resultados.

---

## Ejemplo de Estructura del Proyecto

```plaintext
/proyecto
│
├── README.md
├── main.py
├── clases/
│   ├── Persona.py
│   ├── Recurso.py
│   └── Nodo.py
├── estructuras/
│   ├── Cola.py
│   ├── Pila.py
│   ├── ListaSimple.py
│   ├── ListaDoble.py
│   └── ListaCircular.py
└── reportes/
    ├── ReportePersonas.py
    ├── ReporteRecursos.py
    └── ReporteCasos.py