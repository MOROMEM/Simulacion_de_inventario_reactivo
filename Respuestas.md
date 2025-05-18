📦 GraphQL vs REST en APIs de Productos
🧾 Introducción
Este documento explica las ventajas de usar GraphQL sobre REST en el desarrollo de una API para manejar productos, junto con prácticas recomendadas para garantizar la coherencia de datos como stock y disponibilidad. También se describe cómo se definen los tipos y resolvers en una API GraphQL.

📚 Tabla de Contenidos
✅ Ventajas de GraphQL sobre REST

🔧 Definición de Tipos y Resolvers

🔒 Por qué actualizar disponible en el backend

🛠️ Garantizar coherencia en la lógica de stock

✅ Ventajas de GraphQL sobre REST
Consultas a medida

El cliente solicita solo los campos que necesita (id, nombre, precio, stock, disponible).

Se evitan sobrecargas o peticiones incompletas típicas de REST.

Un solo endpoint

Todas las operaciones usan un único punto de entrada: /graphql.

Ya no es necesario definir múltiples rutas REST (GET /products, POST /products, etc.).

Tipado fuerte y documentación automática

El esquema centralizado define los tipos y operaciones disponibles.

Herramientas como GraphiQL o Playground generan documentación interactiva al instante.

Mejor manejo de relaciones

GraphQL permite resolver campos anidados (como categorías o historial de ventas) sin nuevos endpoints.

Se evita el uso de joins manuales en el frontend.

🔧 Definición de Tipos y Resolvers
📝 Esquema como contrato
El esquema es la fuente de verdad entre cliente y servidor.

Define qué tipos de datos existen y qué operaciones se pueden realizar.

🏗️ TypeDefs (Tipos)
Representan entidades como Product.

Especifican los campos (id, nombre, etc.), entradas (input) y salidas (output).

⚙️ Resolvers
Son funciones que implementan la lógica para cada operación o campo.

Se encargan de acceder a la base de datos, hacer validaciones y retornar resultados.

💡 Ventaja de la separación
El esquema documenta la API.

Los resolvers mantienen la lógica de negocio organizada y desacoplada.

🔒 Por qué actualizar disponible en el backend
Autoridad única de la verdad

El backend mantiene los datos auténticos que consumen todos los clientes.

Seguridad

Se evita que clientes maliciosos establezcan disponible = true sin justificación.

Evitar estados inconsistentes

Si el frontend falla o se desconecta, el backend sigue garantizando consistencia.

🛠️ Garantizar coherencia en la lógica de stock
Centralizar la lógica

Todas las actualizaciones se manejan en los resolvers.

Se aplica la regla: disponible = stock > 0.

Pruebas automatizadas

Tests unitarios y de integración cubren casos como:

Intento de restar más stock del disponible.

Añadir stock.

Agregar o eliminar productos.

Validar cambios en el campo disponible.

Control de concurrencia

En sistemas con múltiples usuarios, usar transacciones para evitar condiciones de carrera.

Validaciones previas

Validar entradas con herramientas como Pydantic o Marshmallow.

Lanzar errores claros si los datos no cumplen las reglas del esquema.
