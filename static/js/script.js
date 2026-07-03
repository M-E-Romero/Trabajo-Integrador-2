// Referencias
const productosDiv = document.getElementById("productos");
const carritoDiv = document.getElementById("carrito");
const carritoBody = document.getElementById("carrito-body");
const totalDiv = document.getElementById("total");
const btnTodo = document.getElementById("btnTodo");
const btnCarrito = document.getElementById("btnCarrito");
const btnFiltro = document.getElementById("btnFiltro");
const categoriasDiv = document.getElementById("categorias");
const btnBorrarTodo = document.getElementById("borrarTodo");

// Mostrar productos
function mostrarProductos(lista) {
  productosDiv.innerHTML = "";
  lista.forEach(p => {
    const div = document.createElement("div");
    div.classList.add("producto");
    div.innerHTML = `
      <div class="producto-top">
        <img src="/static/img/img${p.id}.png" alt="${p.nombre}">
        <h3>${p.nombre}</h3>
        <p>$${p.precio}</p>
      </div>
      <div class="producto-bottom">
        <button class="add-btn" data-id="${p.id}">
          <img src="/static/img/carrito.png" alt="Agregar al carrito">
        </button>
      </div>
    `;
    productosDiv.appendChild(div);
  });

  // Eventos de agregar al carrito
  document.querySelectorAll(".add-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = parseInt(btn.dataset.id);
      agregarAlCarrito(id);
    });
  });
}

// Cargar productos desde backend
function cargarProductos() {
  fetch("/productos")
    .then(res => res.json())
    .then(data => mostrarProductos(data));
}

// Filtrar por categoría
function cargarPorCategoria(cat) {
  const encodedCat = encodeURIComponent(cat);   // 
  fetch(`/productos/${encodedCat}`)
    .then(res => res.json())
    .then(data => mostrarProductos(data));
}


// Mostrar carrito
function mostrarCarrito(lista) {
  carritoBody.innerHTML = "";
  lista.forEach(item => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.nombre}</td>
      <td class="cantidad">
        <button class="menos" data-id="${item.id}">
          <img src="/static/img/menos.png" alt="Quitar">
        </button>
        <span>${item.cantidad}</span>
        <button class="mas" data-id="${item.id}">
          <img src="/static/img/mas.png" alt="Agregar">
        </button>
      </td>
      <td>$${item.precio * item.cantidad}</td>
    `;
    carritoBody.appendChild(tr);
  });

  // Eventos + y -
  document.querySelectorAll(".mas").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = parseInt(btn.dataset.id);
      agregarAlCarrito(id);
    });
  });
  document.querySelectorAll(".menos").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = parseInt(btn.dataset.id);
      eliminarProducto(id);
    });
  });

  // Actualizar total
  fetch("/carrito/total")
    .then(res => res.json())
    .then(data => {
      totalDiv.textContent = `Total: $${data.total}`;
    });
}

// Cargar carrito desde backend
function cargarCarrito() {
  fetch("/carrito")
    .then(res => res.json())
    .then(data => mostrarCarrito(data));
}

// Agregar producto al carrito
function agregarAlCarrito(id) {
    const btn = document.querySelector(`.add-btn[data-id="${id}"]`);
  if (btn) {
    btn.classList.add("clicked");
    setTimeout(() => btn.classList.remove("clicked"), 1000); // vuelve al color normal en 1s
  }

  fetch("/carrito", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: id, cantidad: 1 })
  })
  .then(() => cargarCarrito());
}

// Eliminar producto del carrito
function eliminarProducto(id) {
  fetch(`/carrito/${id}`, { method: "DELETE" })
    .then(() => cargarCarrito());
}

// Vaciar carrito
btnBorrarTodo.addEventListener("click", () => {
  fetch("/carrito/vaciar", { method: "DELETE" })
    .then(() => cargarCarrito());
});

// Navegación
btnTodo.addEventListener("click", () => {
  productosDiv.classList.remove("oculto");
  carritoDiv.classList.add("oculto");
  cargarProductos();
});

btnCarrito.addEventListener("click", () => {
  productosDiv.classList.add("oculto");
  carritoDiv.classList.remove("oculto");
  cargarCarrito();
});

btnFiltro.addEventListener("click", () => {
  categoriasDiv.classList.toggle("oculto");
});

// Filtrar por categoría
document.querySelectorAll(".cat-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const cat = btn.dataset.cat;
    productosDiv.classList.remove("oculto");
    carritoDiv.classList.add("oculto");
    cargarPorCategoria(cat);
  });
});


// Inicial
cargarProductos();
