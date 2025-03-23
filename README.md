# Simulacion_de_inventario_reactivo

## 1. Vue no detecta cambios dentro de objetos reactivos de la forma que esperarías. ¿Cómo podrías observar un cambio en una propiedad anidada?

En Vue, la reactividad tiene ciertas limitaciones cuando se trata de propiedades anidadas en objetos reactivos. Para observar cambios en propiedades anidadas, tenemos varias opciones:

1. **Usar una función de getter en el callback de watch**: Esta es la técnica utilizada en nuestra solución. Al usar una función que retorna la propiedad específica que queremos observar dentro del objeto reactivo:

```javascript
watch(
  () => product.stock,
  (newStock) => {
    // Aquí detectamos el cambio específico
  }
);
```

2. **Usar la opción 'deep' en watch**: Para observar todas las propiedades anidadas en un objeto, podemos usar la opción deep:

```javascript
watch(
  product,
  (newValue) => {
    // Reacciona a cualquier cambio en cualquier propiedad del objeto
  },
  { deep: true }
);
```

3. **Usar watch en rutas específicas**: También podemos especificar directamente la ruta a la propiedad anidada que queremos observar:

```javascript
watch(
  () => productos.value[0].stock,
  (newValue) => {
    // Reacciona a cambios específicos en el stock del primer producto
  }
);
```

## 2. watch() permite escuchar cambios en propiedades específicas dentro de reactive(), explica cómo funciona.

La función `watch()` en Vue 3 permite observar y reaccionar a cambios en fuentes de datos reactivas. Cuando se usa con objetos creados mediante `reactive()`, funciona de la siguiente manera:

1. **Primer argumento (fuente)**: Puede ser una función getter que retorna el valor a observar, un objeto reactivo, una referencia (ref), o un array de estas opciones.

2. **Segundo argumento (callback)**: Es una función que se ejecuta cuando la fuente observada cambia. Recibe dos parámetros: el nuevo valor y el valor anterior.

3. **Tercer argumento (opciones)**: Es un objeto opcional que puede incluir:
   - `deep`: Para observar propiedades anidadas (default: false)
   - `immediate`: Para ejecutar el callback inmediatamente al iniciar el watch (default: false)
   - `flush`: Para controlar cuando se ejecuta el callback ('pre', 'post', o 'sync')

Ejemplos de cómo funciona:

```javascript
// Observando una propiedad específica
watch(
  () => product.stock,
  (newStock, oldStock) => {
    console.log(`Stock cambió de ${oldStock} a ${newStock}`);
  }
);

// Observando el objeto completo (cambios superficiales)
watch(product, (newValue, oldValue) => {
  console.log("El producto cambió", newValue, oldValue);
});

// Observando el objeto completo (cambios profundos)
watch(
  product,
  (newValue, oldValue) => {
    console.log("El producto o alguna propiedad anidada cambió");
  },
  { deep: true }
);
```

## 3. ¿Cómo harías que un watch() detecte cambios en stock dentro de un array de productos?

Para detectar cambios en la propiedad "stock" de cada producto dentro de un array de productos, hay varias técnicas:

1. **Observar cada elemento individualmente** (método implementado en mi solución):

```javascript
products.forEach((product) => {
  watch(
    () => product.stock,
    (newStock) => {
      product.disponible = newStock > 0;
    }
  );
});
```

2. **Usar un watch con deep para todo el array**:

```javascript
watch(
  products,
  () => {
    // Actualizar disponibilidad para todos los productos
    products.forEach((product) => {
      product.disponible = product.stock > 0;
    });
  },
  { deep: true }
);
```

3. **Crear una función personalizada para observar una propiedad específica dentro de cada elemento del array**:

```javascript
function watchArrayProperty(array, propName, callback) {
  array.forEach((item, index) => {
    watch(
      () => item[propName],
      (newValue, oldValue) => {
        callback(item, index, newValue, oldValue);
      }
    );
  });
}

// Uso
watchArrayProperty(products, "stock", (product) => {
  product.disponible = product.stock > 0;
});
```

La primera opción es generalmente la más eficiente para este caso específico, ya que solo reacciona cuando cambia la propiedad específica que nos interesa, mientras que la opción con `deep: true` reaccionaría a cualquier cambio en cualquier propiedad de cualquier producto.
