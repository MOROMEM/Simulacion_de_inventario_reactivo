from flask import Flask, request, jsonify
from flask_cors import CORS
from ariadne import ObjectType, QueryType, MutationType, make_executable_schema, graphql_sync
# Importación actualizada para versiones recientes de Ariadne
from ariadne.explorer import ExplorerGraphiQL

app = Flask(__name__)
CORS(app)  # Habilitar CORS para conectar con el frontend Vue

# Base de datos en memoria
products = [
    {
        "id": 1,
        "nombre": "Asus ROGX",
        "precio": 999.99,
        "stock": 10,
        "disponible": True
    },
    {
        "id": 2,
        "nombre": "Samsung Galaxy S24",
        "precio": 499.99,
        "stock": 5,
        "disponible": True
    },
    {
        "id": 3,
        "nombre": "Xiaomi 5G",
        "precio": 79.99,
        "stock": 0,
        "disponible": False
    }
]

# Definición del esquema GraphQL
type_defs = """
    type Product {
        id: ID!
        nombre: String!
        precio: Float!
        stock: Int!
        disponible: Boolean!
    }
    
    type Query {
        products: [Product]!
        product(id: ID!): Product
    }
    
    type Mutation {
        updateStock(id: ID!, amount: Int!): Product
        addProduct(nombre: String!, precio: Float!, stock: Int!): Product
        removeProduct(id: ID!): Boolean
    }
"""

# Configurar los resolvers
query = QueryType()
mutation = MutationType()
product = ObjectType("Product")

@query.field("products")
def resolve_products(*_):
    return products

@query.field("product")
def resolve_product(_, info, id):
    for product in products:
        if product["id"] == int(id):
            return product
    return None

@mutation.field("updateStock")
def resolve_update_stock(_, info, id, amount):
    for product in products:
        if product["id"] == int(id):
            # Actualizar el stock
            product["stock"] += amount

            # Aplicar la lógica de disponibilidad
            if product["stock"] <= 0:
                product["stock"] = 0  # Asegurar que el stock no sea negativo
                product["disponible"] = False
            else:
                product["disponible"] = True

            return product
    return None

@mutation.field("addProduct")
def resolve_add_product(_, info, nombre, precio, stock):
    # Generar un nuevo ID (simplemente el máximo ID actual + 1)
    new_id = max([p["id"] for p in products]) + 1 if products else 1

    # Crear el nuevo producto
    new_product = {
        "id": new_id,
        "nombre": nombre,
        "precio": precio,
        "stock": stock,
        "disponible": stock > 0
    }

    # Añadir a la lista
    products.append(new_product)
    return new_product

@mutation.field("removeProduct")
def resolve_remove_product(_, info, id):
    global products
    initial_length = len(products)
    products = [p for p in products if p["id"] != int(id)]
    return len(products) < initial_length

# Crear el esquema ejecutable
schema = make_executable_schema(type_defs, query, mutation, product)

# Ruta para GraphQL
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # Playground para probar queries GraphQL en el navegador
    explorer = ExplorerGraphiQL(title="API GraphQL para Inventario")
    return explorer.html(None), 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True)