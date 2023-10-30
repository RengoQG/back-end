# Documentación del Servicio: Registro de Paradas

## Descripción

El servicio de "Registro de Paradas" permite a los "Operadores Logísticos" registrar nuevas paradas en la base de datos. Las paradas son esenciales para la gestión de rutas de transporte público en una ciudad.

## Detalles del Servicio

- **Endpoint:** `/api/stops/`
- **Método HTTP:** POST

## Permisos

- **Operador Logístico:** Los Operadores Logísticos tienen el permiso para acceder a este servicio y registrar nuevas paradas.
- **Pasajeros:** Los Pasajeros no tienen acceso a esta función.

## Parámetros

La solicitud POST debe incluir los siguientes parámetros en el cuerpo de la solicitud (en formato JSON):

- `nombre`: Nombre de la parada (cadena de texto).
- `latitud`: Coordenada de latitud de la parada (valor numérico).
- `longitud`: Coordenada de longitud de la parada (valor numérico).
- `ciudad_id`: ID de la ciudad a la que se asociará la parada (entero).

## Ejemplo de Solicitud

```json
POST /api/stops/
Content-Type: application/json

{
    "nombre": "Nueva Parada",
    "latitud": 45.123,
    "longitud": 23.456,
    "ciudad_id": 1
}


Nota: Este servicio se utiliza principalmente a través de formularios HTML y no se recomienda probarlo directamente utilizando herramientas como Postman o cURL.
