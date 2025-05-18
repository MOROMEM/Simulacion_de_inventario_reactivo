🛒 Gestión de Stock con Frontend y Backend Separados
Una aplicación web para la gestión de inventario, construida con un backend en Python y un frontend en JavaScript. La arquitectura separa claramente el frontend del backend, facilitando el desarrollo y mantenimiento. Se utiliza GraphQL para las operaciones con los productos.

📑 Tabla de Contenidos
🚀 Instalación y Ejecución

🔧 Requisitos

🧪 Probar GraphQL

📦 Funcionalidades

❓ Troubleshooting

👥 Contribuidores

📄 Licencia

🚀 Instalación y Ejecución
Por comodidad, se recomienda abrir dos consolas: una para el backend y otra para el frontend.

Consola 1 – Backend

Ejecuta el servidor backend:

python app.py

Una vez iniciado, accede a GraphQL en:

http://localhost:5000/graphql

Consola 2 – Frontend
Asegúrate de tener Node.js y npm instalados.

Ejecuta el servidor frontend:

npm run serve
Accede a la aplicación en:

http://localhost:8080/
Desde ahí podrás gestionar el stock de productos de forma visual.

🔧 Requisitos
Python 3.x

Node.js >= 14.x

npm >= 6.x

Flask y dependencias necesarias (para el backend)

Framework JS como Vue.js (para el frontend)

🧪 Probar GraphQL
Accede a http://localhost:5000/graphql para ejecutar las siguientes queries/mutations directamente en el explorador:

Obtener todos los productos
graphql
Copiar
Editar
query {
products {
id
nombre
precio
stock
disponible
}
}
Actualizar el stock de un producto
graphql
Copiar
Editar
mutation {
updateStock(id: 1, amount: 5) {
id
nombre
stock
disponible
}
}
Añadir un nuevo producto
graphql
Copiar
Editar
mutation {
addProduct(
nombre: "Nuevo Producto",
precio: 299.99,
stock: 15
) {
id
nombre
precio
stock
disponible
}
}
Eliminar un producto
graphql
Copiar
Editar
mutation {
removeProduct(id: 4)
}
📦 Funcionalidades
Listado de productos con disponibilidad

Añadir, actualizar y eliminar productos

Control de stock en tiempo real vía GraphQL
