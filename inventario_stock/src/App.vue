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
      <p v-if="loading">Cargando productos...</p>
      <p v-if="error">{{ error }}</p>
      <table v-if="!loading && !error">
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
        <tr v-for="product in products" :key="product.id" :class="{ 'unavailable': !product.disponible }">
          <td>{{ product.nombre }}</td>
          <td>€{{ product.precio.toFixed(2) }}</td>
          <td>{{ product.stock }}</td>
          <td>{{ product.disponible ? 'Sí' : 'No' }}</td>
          <td>
            <button @click="incrementStock(product.id)" :disabled="product.stock >= 100">+</button>
            <button @click="decrementStock(product.id)" :disabled="product.stock <= 0">-</button>
            <button @click="removeProduct(product.id)" class="remove-btn">Eliminar</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';

// URL del backend GraphQL
const GRAPHQL_URL = 'http://localhost:5000/graphql';

// Estado para el manejo de productos
const products = ref([]);
const loading = ref(true);
const error = ref(null);

const newProduct = reactive({
  name: '',
  price: 0,
  stock: 0
});

async function fetchGraphQL(query, variables = {}) {
  try {
    const response = await fetch(GRAPHQL_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        variables
      }),
    });

    const data = await response.json();

    if (data.errors) {
      throw new Error(data.errors[0].message);
    }

    return data.data;
  } catch (err) {
    console.error('Error en la consulta GraphQL:', err);
    error.value = `Error al comunicarse con el servidor: ${err.message}`;
    throw err;
  }
}

async function loadProducts() {
  loading.value = true;
  error.value = null;

  try {
    const query = `
      query {
        products {
          id
          nombre
          precio
          stock
          disponible
        }
      }
    `;

    const data = await fetchGraphQL(query);
    products.value = data.products;
  } catch (err) {
    console.error('Error al cargar productos:', err);
    error.value = 'No se pudieron cargar los productos';
  } finally {
    loading.value = false;
  }
}

async function addProduct() {
  if (newProduct.name.trim() === '' || newProduct.price <= 0) {
    alert('Por favor, ingresa un nombre y un precio válido');
    return;
  }

  try {
    const mutation = `
      mutation ($nombre: String!, $precio: Float!, $stock: Int!) {
        addProduct(nombre: $nombre, precio: $precio, stock: $stock) {
          id
          nombre
          precio
          stock
          disponible
        }
      }
    `;

    const variables = {
      nombre: newProduct.name,
      precio: newProduct.price,
      stock: newProduct.stock
    };

    await fetchGraphQL(mutation, variables);


    await loadProducts();

    newProduct.name = '';
    newProduct.price = 0;
    newProduct.stock = 0;
  } catch (err) {
    console.error('Error al añadir producto:', err);
    alert('Error al añadir el producto');
  }
}

async function removeProduct(id) {
  const productToRemove = products.value.find(p => p.id == id);

  if (confirm(`¿Estás seguro de que deseas eliminar ${productToRemove.nombre}?`)) {
    try {
      const mutation = `
        mutation ($id: ID!) {
          removeProduct(id: $id)
        }
      `;

      const variables = { id };

      await fetchGraphQL(mutation, variables);

      await loadProducts();
    } catch (err) {
      console.error('Error al eliminar producto:', err);
      alert('Error al eliminar el producto');
    }
  }
}


async function incrementStock(id) {
  try {
    const mutation = `
      mutation ($id: ID!, $amount: Int!) {
        updateStock(id: $id, amount: $amount) {
          id
          nombre
          stock
          disponible
        }
      }
    `;

    const variables = { id, amount: 1 };

    await fetchGraphQL(mutation, variables);


    await loadProducts();
  } catch (err) {
    console.error('Error al incrementar stock:', err);
    alert('Error al actualizar el stock');
  }
}


async function decrementStock(id) {
  try {
    const mutation = `
      mutation ($id: ID!, $amount: Int!) {
        updateStock(id: $id, amount: $amount) {
          id
          nombre
          stock
          disponible
        }
      }
    `;

    const variables = { id, amount: -1 };

    await fetchGraphQL(mutation, variables);


    await loadProducts();
  } catch (err) {
    console.error('Error al decrementar stock:', err);
    alert('Error al actualizar el stock');
  }
}


onMounted(() => {
  loadProducts();
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