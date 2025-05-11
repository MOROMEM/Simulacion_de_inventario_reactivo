Backend Flask con GraphQL para Inventario
Este proyecto implementa un backend utilizando Flask y GraphQL para gestionar el inventario de productos de una tienda online, conectándose con un frontend desarrollado en Vue.
Estructura del Proyecto
/proyecto
├── backend/
│ ├── app.py # Aplicación Flask + GraphQL
│ └── requirements.txt
│
└── frontend/
├── src/
│ ├── App.vue # Componente principal de Vue (modificado)
│ └── main.js
└── ...
Características Implementadas
Backend (Flask + GraphQL)

Base de datos en memoria con productos iniciales
Esquema GraphQL con:

Consulta (Query) para obtener todos los productos
Mutaciones (Mutations) para:

Actualizar el stock de un producto
Añadir nuevos productos
Eliminar productos existentes

Lógica de negocio:

Actualización automática del campo disponible basado en el stock
Stock a 0 = producto no disponible
Stock > 0 = producto disponible

Frontend (Vue)

Conexión con el backend mediante solicitudes GraphQL
Actualización reactiva de la interfaz de usuario cuando cambian los datos
Funcionalidades de:

Visualización de productos
Adición de nuevos productos
Incremento/decremento del stock
Eliminación de productos

Instalación y Ejecución
Backend

Navega a la carpeta backend:
cd backend

Instala las dependencias:
pip install -r requirements.txt

Ejecuta la aplicación Flask:
python app.py
El servidor estará disponible en http://localhost:5000

Frontend

Navega a la carpeta del frontend:
cd frontend

Instala las dependencias:
npm install

Ejecuta el servidor de desarrollo:
npm run dev
El frontend estará disponible en http://localhost:5173 (o el puerto que Vue asigne)

Pruebas GraphQL
Puedes acceder al GraphQL Playground para probar las consultas en:
http://localhost:5000/graphql
Consultas de ejemplo:

Obtener todos los productos:
graphqlquery {
products {
id
nombre
precio
stock
disponible
}
}

Actualizar el stock de un producto:
graphqlmutation {
updateStock(id: 1, amount: 5) {
id
nombre
stock
disponible
}
}

Añadir un nuevo producto:
graphqlmutation {
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

Eliminar un producto:
graphqlmutation {
removeProduct(id: 4)
}

Implementación de la Lógica de Disponibilidad
La lógica que actualiza el campo disponible basado en el stock se implementa en el backend dentro del resolver updateStock. Siguiendo los requisitos, un producto:

Es no disponible cuando su stock es 0
Es disponible cuando su stock es mayor que 0

Esta lógica se aplica tanto al actualizar el stock como al crear nuevos productos
