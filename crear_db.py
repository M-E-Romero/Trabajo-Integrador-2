import sqlite3

conn = sqlite3.connect("tienda.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio INTEGER NOT NULL,
    categoria TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS carrito (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
)
""")


productos_iniciales = [
    ("Jabón neutral", 5000, "Jabones"),
    ("Jabón de castillas", 6000, "Jabones"),
    ("Jabón de lavanda", 6000, "Jabones"),
    ("Shampoo sólido", 6500, "Shampoo/Acondicionador"),
    ("Acondicionador sólido", 6500, "Shampoo/Acondicionador"),
    ("Bálsamo descongestivo", 4000, "Bálsamos"),
    ("Bálsamo expectorante de tomillo", 4000, "Bálsamos"),
    ("Bálsamo de caléndula y lavanda", 5000, "Bálsamos"),
    ("Bálsamo labial Karité rojo", 5500, "Bálsamos"),
    ("Bálsamo labial Karité rosa", 5500, "Bálsamos"),
    ("Crema regenerativa caléndula", 12000, "Cremas"),
    ("Crema hidratante lavanda", 8000, "Cremas")
]

cursor.executemany("INSERT INTO productos (nombre, precio, categoria) VALUES (?, ?, ?)", productos_iniciales)


conn.commit()
conn.close()

print("base")
