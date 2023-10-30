# Documentación del Servicio: Consultar Detalles de una Ruta de Autobús

## Descripción

El servicio "Consultar Detalles de una Ruta de Autobús" permite tanto a los "Pasajeros" como al "Operador Logístico" obtener detalles de una ruta de autobús específica, incluyendo la lista de paradas asociadas. Esto es útil para obtener información detallada sobre una ruta de autobús y sus paradas correspondientes.

## Detalles del Servicio

- **Endpoint:** `/api/routes/<route_id>/`
- **Método HTTP:** GET

## Permisos

- **Operador Logístico:** Los Operadores Logísticos tienen permiso para acceder a este servicio y obtener detalles de una ruta de autobús específica.
- **Pasajeros:** Los Pasajeros también tienen acceso para consultar detalles de rutas de autobús.

## Datos de Salida

El servicio devuelve una respuesta que incluye los detalles de la ruta de autobús, que pueden incluir información como el nombre de la ruta, su origen, destino y una lista de paradas asociadas.

## Ejemplo de Solicitud

Para obtener detalles de una ruta de autobús, realiza una solicitud GET a la siguiente URL, donde `<route_id>` es el ID de la ruta deseada:

Nota: Se creo dos end point uno para probarlo en postman y otro desde la interfaz de usuario(/detalle_ruta).
