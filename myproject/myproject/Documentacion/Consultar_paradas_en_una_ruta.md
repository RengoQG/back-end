# Documentación del Servicio: Consultar Paradas en una Ruta

## Descripción

El servicio "Consultar Paradas en una Ruta" permite tanto a los "Pasajeros" como al "Operador Logístico" consultar las paradas asociadas a una ruta específica en la base de datos. Esto es esencial para que los usuarios puedan obtener información sobre las paradas de una ruta de transporte público.

## Detalles del Servicio

- **Endpoint:** `/api/routes/<route_id>/stops/`
- **Método HTTP:** GET

## Permisos

- **Operador Logístico:** Los Operadores Logísticos tienen permiso para acceder a este servicio y consultar las paradas asociadas a una ruta.
- **Pasajeros:** Los Pasajeros también tienen acceso a esta función.

## Parámetros

- `route_id`: El ID de la ruta para la cual se desean consultar las paradas (parte de la URL).

## Ejemplo de Solicitud

```json
GET /api/routes/1/stops/

Nota: Este servicio se utiliza principalmente a través de formularios HTML y no se recomienda probarlo directamente utilizando herramientas como Postman o cURL.
