<template>
  <div class="inventory-app">
    <h1>Inventario de Productos</h1>

    <div class="product-form">
      <h2>Añadir Nuevo Producto</h2>
      <div class="form-group">
        <label for="name">Nombre:</label>
        <input id="name" v-model="newProduct.name" type="text" />
      </div>

      <div class="form-group">
        <label for="price">Precio:</label>
        <input id="price" v-model.number="newProduct.price" type="number" min="0" />
      </div>

      <div class="form-group">
        <label for="stock">Stock:</label>
        <input id="stock" v-model.number="newProduct.stock" type="number" min="0" />
      </div>

      <button @click="addProduct">Añadir Producto</button>
    </div>

    <div class="product-list">
      <h2>Lista de Productos</h2>
      <table>
        <thead>
        <tr>
          <th>Nombre</th>
          <th>Precio</th>
          <th>Stock</th>
          <th>Disponible</th>
          <th>Acciones</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(product, index) in products" :key="index" :class="{ 'unavailable': !product.disponible }">
          <td>{{ product.nombre }}</td>
          <td>€{{ product.precio.toFixed(2) }}</td>
          <td>{{ product.stock }}</td>
          <td>{{ product.disponible ? 'Sí' : 'No' }}</td>
          <td>
            <button @click="incrementStock(index)" :disabled="product.stock >= 100">+</button>
            <button @click="decrementStock(index)" :disabled="product.stock <= 0">-</button>
            <button @click="removeProduct(index)" class="remove-btn">Eliminar</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue';

// Crear un objeto reactivo para el estado de productos
const products = reactive([
  { nombre: 'Asus ROGX', precio: 999.99, stock: 10, disponible: true },
  { nombre: 'Samsung Galaxy S24', precio: 499.99, stock: 5, disponible: true },
  { nombre: 'Xiaomi 5G', precio: 79.99, stock: 0, disponible: false }
]);

// Objeto para el nuevo producto
const newProduct = reactive({
  name: '',
  price: 0,
  stock: 0
});

// Añadir un nuevo producto
const addProduct = () => {
  if (newProduct.name.trim() === '' || newProduct.price <= 0) {
    alert('Por favor, ingresa un nombre y un precio válido');
    return;
  }

  products.push({
    nombre: newProduct.name,
    precio: newProduct.price,
    stock: newProduct.stock,
    disponible: newProduct.stock > 0
  });

  // Resetear el formulario
  newProduct.name = '';
  newProduct.price = 0;
  newProduct.stock = 0;
};

// Eliminar un producto
const removeProduct = (index) => {
  if (confirm(`¿Estás seguro de que deseas eliminar ${products[index].nombre}?`)) {
    products.splice(index, 1);
  }
};

// Incrementar stock
const incrementStock = (index) => {
  products[index].stock += 1;

  // Actualizar disponibilidad si era falso
  if (!products[index].disponible) {
    products[index].disponible = true;
  }
};

// Decrementar stock
const decrementStock = (index) => {
  if (products[index].stock > 0) {
    products[index].stock -= 1;

    // Actualizar disponibilidad si llega a cero
    if (products[index].stock === 0) {
      products[index].disponible = false;
    }
  }
};

// Observar cambios en el stock de cada producto
products.forEach((product, index) => {
  watch(
      () => product.stock,
      (newStock) => {
        product.disponible = newStock > 0;
        console.log(`Producto ${product.nombre}: Stock cambiado a ${newStock}, disponible: ${product.disponible}`);
      }
  );
});
</script>

<style scoped>
.inventory-app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.product-form, .product-list {
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 10px;
}

label {
  display: inline-block;
  width: 80px;
}

input {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

button {
  padding: 5px 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  margin-right: 5px;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.remove-btn {
  background-color: #f44336;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
}

.unavailable {
  background-color: #ffebee;
}
</style>