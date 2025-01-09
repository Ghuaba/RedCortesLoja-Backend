Servicio de Supervisores y Notificaciones Directas
Descripción
Este microservicio se encarga de gestionar a los supervisores y las notificaciones que emiten de manera directa, sin necesidad de validación por parte de los usuarios. Los supervisores pueden declarar cortes de agua o luz de manera oficial, notificando a todos los usuarios registrados en los sectores afectados. Este servicio forma parte del sistema de alerta en tiempo real para cortes de agua y luz en la ciudad de Loja.

Responsable
Nombre: Pool Ochoa
Rol: Desarrollador principal del microservicio de supervisores y notificaciones directas.

Objetivo
El objetivo de este microservicio es proporcionar un mecanismo para que los supervisores puedan generar alertas oficiales de cortes sin tener que esperar la validación de los usuarios. Las notificaciones se envían a todos los usuarios registrados dentro de los sectores afectados por el corte.

Funcionalidad
Generación de Cortes: Los supervisores pueden declarar un corte (agua o luz) especificando el tipo de servicio y el sector afectado.
Notificaciones Directas: Una vez que el corte es declarado, se genera una notificación oficial que se envía a todos los usuarios registrados en el sector afectado.
Sin Validación de Usuarios: No se requiere que los usuarios validen los cortes, ya que son emitidos directamente por los supervisores.