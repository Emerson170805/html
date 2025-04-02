let currentIndex = 0;
let productoActual = {};
const carrito = {};

document.addEventListener("DOMContentLoaded", function () {
    updateSlidePosition();
});

function updateSlidePosition() {
    const slides = document.querySelector('.slides');
    slides.style.transform = `translateX(-${currentIndex * 100}%)`;
}

function prevSlide() {
    if (currentIndex > 0) currentIndex--;
    updateSlidePosition();
}

function nextSlide() {
    const totalSlides = document.querySelectorAll('.slide').length;
    if (currentIndex < totalSlides - 1) currentIndex++;
    updateSlidePosition();
}

function mostrarInfo(nombre, precio) {
    productoActual = { nombre, precio };
    document.getElementById('modal-titulo').innerText = nombre;
    document.getElementById('modal-precio').innerText = `Precio: S/. ${precio.toFixed(2)}`;
    document.getElementById('modal-info').style.display = 'flex';
}

function cerrarModal() {
    document.getElementById('modal-info').style.display = 'none';
}

function agregarAlCarrito() {
    const nombre = productoActual.nombre;
    if (carrito[nombre]) {
        carrito[nombre].cantidad++;
    } else {
        carrito[nombre] = { precio: productoActual.precio, cantidad: 1 };
    }
    renderCarrito();
    cerrarModal();
}

function modificarCantidad(nombre, cant) {
    carrito[nombre].cantidad += cant;
    if (carrito[nombre].cantidad < 1) delete carrito[nombre];
    renderCarrito();
}

function renderCarrito() {
    const lista = document.getElementById('lista-carrito');
    lista.innerHTML = '';
    let totalGeneral = 0;

    Object.entries(carrito).forEach(([nombre, {precio, cantidad}]) => {
        const subtotal = precio * cantidad;
        totalGeneral += subtotal;
        lista.innerHTML += `
        <li>
            <span>${nombre}</span>
            <div>
                <button class="cantidad-btn" onclick="modificarCantidad('${nombre}', -1)">-</button>
                <span>${cantidad}</span>
                <button class="cantidad-btn" onclick="modificarCantidad('${nombre}', 1)">+</button>
            </div>
            <span>S/. ${subtotal.toFixed(2)}</span>
        </li>`;
    });

    document.getElementById('total-general').innerText = totalGeneral.toFixed(2);
}

function enviarWhatsApp() {
    let mensaje = 'Pedido desde catálogo:\n';
    Object.entries(carrito).forEach(([nombre, {cantidad, precio}]) => {
        mensaje += `${nombre} x${cantidad} = S/. ${(precio * cantidad).toFixed(2)}\n`;
    });
    mensaje += `Total: S/. ${document.getElementById('total-general').innerText}`;

    const numeroWhatsApp = '51947757355';
    const url = `https://wa.me/${numeroWhatsApp}?text=${encodeURIComponent(mensaje)}`;
    window.open(url, '_blank');
}

function toggleCarrito() {
    document.getElementById('carrito').classList.toggle('activo');
}

document.addEventListener('click', function (e) {
    const carrito = document.getElementById('carrito');
    const icono = document.querySelector('.carrito-icono');

    if (!carrito.contains(e.target) && !icono.contains(e.target)) {
        carrito.classList.remove('activo');
    }
});