# Documentación del Servicio: Consultar Rutas de Autobús

## Descripción

El servicio "Consultar Rutas de Autobús" permite tanto a los "Pasajeros" como al "Operador Logístico" consultar la lista de rutas de autobús disponibles en la base de datos. Esto es esencial para que los usuarios puedan obtener información sobre las rutas de transporte público.

## Detalles del Servicio

- **Endpoint:** `http://localhost:8000/api/routes/`
- **Método HTTP:** GET

## Permisos

- **Operador Logístico:** Los Operadores Logísticos tienen permiso para acceder a este servicio y consultar la lista de rutas de autobús disponibles.
- **Pasajeros:** Los Pasajeros también tienen acceso a esta función.

## Ejemplo de Solicitud

```json
GET http://localhost:8000/api/routes/

Nota: Se creo dos end point uno para probarlo en postman y otro desde la interfaz de usuario(rutas/).
