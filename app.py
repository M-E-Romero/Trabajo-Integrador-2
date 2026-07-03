from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("tienda.db")
    conn.row_factory = sqlite3.Row 
    return conn

# Página principal
@app.route("/")
def home():
    return render_template("index.html")

# Listar todos los productos
@app.route("/productos", methods=["GET"])
def listar_productos():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return jsonify([dict(p) for p in productos])

# Listar productos por categoría
@app.route("/productos/<path:categoria>", methods=["GET"])
def listar_por_categoria(categoria):
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos WHERE categoria = ?", (categoria,)).fetchall()
    conn.close()
    return jsonify([dict(p) for p in productos])

# Ver carrito
@app.route("/carrito", methods=["GET"])
def ver_carrito():
    conn = get_db_connection()
    carrito = conn.execute("""
        SELECT c.producto_id as id, p.nombre, p.precio, c.cantidad
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
    """).fetchall()
    conn.close()
    return jsonify([dict(item) for item in carrito])

# Agregar producto al carrito 
@app.route("/carrito", methods=["POST"])
def agregar_carrito():
    data = request.get_json()
    producto_id = data["id"]
    cantidad = data.get("cantidad", 1)

    conn = get_db_connection()
    item = conn.execute("SELECT cantidad FROM carrito WHERE producto_id = ?", (producto_id,)).fetchone()

    if item:
       
        conn.execute("UPDATE carrito SET cantidad = cantidad + ? WHERE producto_id = ?", (cantidad, producto_id))
    else:
        
        conn.execute("INSERT INTO carrito (producto_id, cantidad) VALUES (?, ?)", (producto_id, cantidad))

    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

# Eliminar producto 
@app.route("/carrito/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    conn = get_db_connection()
    item = conn.execute("SELECT cantidad FROM carrito WHERE producto_id = ?", (id,)).fetchone()
    if item:
        if item["cantidad"] > 1:
            conn.execute("UPDATE carrito SET cantidad = cantidad - 1 WHERE producto_id = ?", (id,))
        else:
            conn.execute("DELETE FROM carrito WHERE producto_id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

# Vaciar carrito (botón Borrar Todo)
@app.route("/carrito/vaciar", methods=["DELETE"])
def vaciar_carrito():
    conn = get_db_connection()
    conn.execute("DELETE FROM carrito")
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Carrito vaciado"})

# Calcular total del carrito
@app.route("/carrito/total", methods=["GET"])
def calcular_total():
    conn = get_db_connection()
    total = conn.execute("""
        SELECT SUM(p.precio * c.cantidad) as total
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
    """).fetchone()["total"]
    conn.close()
    return jsonify({"total": total if total else 0})
