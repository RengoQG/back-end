# Documentación del Servicio: Asociar Paradas a Rutas

## Descripción

El servicio "Asociar Paradas a Rutas" permite a los "Operadores Logísticos" asociar paradas existentes a rutas específicas en la base de datos. Esta función es esencial para la configuración de rutas de transporte público.

## Detalles del Servicio

- **Endpoint:** `/api/routes/<route_id>/add-stop/`
- **Método HTTP:** POST

## Permisos

- **Operador Logístico:** Los Operadores Logísticos tienen el permiso para acceder a este servicio y asociar paradas a rutas existentes.
- **Pasajeros:** Los Pasajeros no tienen acceso a esta función.

## Parámetros

La solicitud POST debe incluir los siguientes parámetros:

- `route_id`: El ID de la ruta a la que se desea asociar una parada (parte de la URL).
- `parada_id`: El ID de la parada existente que se desea asociar a la ruta (en el cuerpo de la solicitud).

## Ejemplo de Solicitud

```json
POST /api/routes/1/add-stop/
Content-Type: application/json

{
    "parada_id": 42
}


Nota: Este servicio se utiliza principalmente a través de formularios HTML y no se recomienda probarlo directamente utilizando herramientas como Postman o cURL.