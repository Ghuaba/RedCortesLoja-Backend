**Servicio de Supervisores y Notificaciones de Validación**
### **Descripción**
Este microservicio gestiona las notificaciones relacionadas con cortes de servicio reportados por usuarios. La validación de dichas notificaciones se realiza mediante un sistema de consenso en el que un 65% de aceptación por parte de otros usuarios registrados en el área afectada es suficiente para su aprobación. Posteriormente, las notificaciones validadas son difundidas de manera escalonada y progresiva a los usuarios de la red.
### **Responsable**
**Nombre:** Kevin Jaramillo  
**Rol:** Desarrollador principal del microservicio de Supervisores y Notificaciones de Validación.
### **Objetivo**
El objetivo de este microservicio es proveer un mecanismo eficiente y confiable para:
•	Generar alertas de cortes de servicio.
•	Validar las alertas a través de consenso entre usuarios.
•	Difundir notificaciones validadas a los usuarios en capas progresivas.


### **Funcionalidad**
1.	**Reporte de cortes**: Los usuarios pueden informar sobre interrupciones especificando el tipo de servicio y el sector afectado.
2.	**Validación de alertas**: Los nodos cercanos (usuarios registrados en el radio inicial) reciben la alerta y votan para aceptarla o rechazarla.
3.	**Difusión escalonada**: Si la alerta es validada, la notificación se envía inicialmente a los usuarios cercanos y luego se expande progresivamente en radios mayores.

### **Clases y Métodos**
#### **Usuario**
### `reportarCorte(tipo: String, sector: Sector): void`
Genera una alerta de corte especificando el tipo de servicio y el sector afectado.

### `validarCorte(corte: Corte): boolean`
Permite al usuario aceptar o rechazar un corte reportado.

### `recibirNotificacion(mensaje: String): void`
Recibe una notificación validada.


### Clase: `Corte`

- **`validarCorte(usuario: Usuario): void`**  
  Registra la validación del usuario para el corte.

- **`rechazarCorte(): void`**  
  Marca el corte como rechazado si no se alcanza el consenso necesario.

### Clase: `Notificación`

- **`enviar(usuario: Usuario): void`**  
  Envía la notificación a un usuario específico.

### Clase: `Sector`

Representa la región afectada por el corte y gestiona la información del área.

### **Flujo del Servicio**
1.	**Reporte de corte:**
      Un usuario genera una alerta indicando el tipo de servicio afectado y el sector.
2.	**Validación inicial:**
      Los nodos cercanos reciben la alerta y emiten su voto para aceptar o rechazarla.
      Si el 65% de los nodos acepta la alerta, esta es validada.
3.	**Notificación inicial:**
      La alerta validada se envía como notificación a los usuarios en el primer radio de difusión (por ejemplo, 60 metros).
4.	**Difusión progresiva:**
      La notificación se expande a radios más amplios (125 metros, 250 metros, etc.) hasta alcanzar el límite predefinido.
5.	**Finalización:**
      Todos los usuarios en el área afectada reciben la notificación validada, asegurando una cobertura eficiente y gradual.
