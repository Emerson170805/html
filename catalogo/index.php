<?php
require_once 'conexion.php';
$conn = conectar();

$hojas = $conn->query("SELECT id, hoja FROM hojas ORDER BY id ASC")->fetchAll(PDO::FETCH_ASSOC);
$productos = $conn->query("SELECT * FROM productos")->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Catálogo Interactivo A4</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="estilos.css" rel="stylesheet">
</head>
<body>

<header class="header-catalogo shadow-sm">
    <h1 class="titulo-catalogo">Catálogo Interactivo</h1>
</header>

<!-- Ícono flotante del carrito -->
<button id="iconoCarrito" class="btn btn-primary carrito-flotante position-fixed" onclick="mostrarCarrito()">
    🛒 <span id="contadorCarrito" class="badge bg-danger">0</span>
</button>

<!-- Contenedor principal -->
<div class="main-container d-flex justify-content-center align-items-center">
    <?php if (count($hojas) > 0): ?>
        <div class="hoja-a4">
            <div id="catalogoCarrusel" class="carousel slide carousel-fade h-100" data-bs-touch="true" data-bs-interval="false" data-bs-keyboard="true">
                <div class="carousel-inner h-100">
                    <?php foreach ($hojas as $index => $hoja): ?>
                        <div class="carousel-item h-100 <?= $index === 0 ? 'active' : '' ?>">
                            <div class="w-100 h-100 position-relative">
                                <img src="imagen.php?id=<?= htmlspecialchars($hoja['id']) ?>" alt="Hoja <?= htmlspecialchars($hoja['hoja']) ?>" class="imagen-hoja">

                                <?php foreach ($productos as $producto): ?>
                                    <?php if ($producto['id_hoja'] == $hoja['id']): ?>
                                        <button class="producto-btn"
                                            style="left: <?= floatval($producto['horizontal']) ?>%; top: <?= floatval($producto['vertical']) ?>%;"
                                            onclick='abrirModalProducto(<?= json_encode($producto, JSON_HEX_TAG | JSON_HEX_APOS | JSON_HEX_AMP | JSON_HEX_QUOT) ?>)'>
                                            S/. <?= number_format($producto['precio_menor'], 2) ?>
                                        </button>
                                    <?php endif; ?>
                                <?php endforeach; ?>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>

                <button class="carousel-control-prev" type="button" data-bs-target="#catalogoCarrusel" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon"></span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#catalogoCarrusel" data-bs-slide="next">
                    <span class="carousel-control-next-icon"></span>
                </button>
            </div>
        </div>

        <!-- Modal Producto -->
        <div class="modal fade" id="modalProducto" tabindex="-1" aria-labelledby="modalProductoLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title" id="modalProductoLabel">Producto</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p><strong>Nombre:</strong> <span id="modalNombreProducto"></span></p>
                        <p><strong>Descripción:</strong> <span id="modalDescripcionProducto"></span></p>
                        <p><strong>Precio:</strong> S/. <span id="modalPrecioProducto"></span></p>
                        <input type="number" id="modalCantidad" class="form-control" value="1" min="1">
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-success" onclick="agregarAlCarrito()">Añadir al carrito</button>
                        <button class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Carrito -->
        <div class="offcanvas offcanvas-end" tabindex="-1" id="carritoCanvas">
            <div class="offcanvas-header">
                <h5 class="offcanvas-title">Carrito de Compras</h5>
                <button type="button" class="btn-close" data-bs-dismiss="offcanvas"></button>
            </div>
            <div class="offcanvas-body">
                <div id="contenidoCarrito"></div>
                <hr>
                <button class="btn btn-success w-100 mb-3" onclick="enviarWhatsapp()">Enviar a WhatsApp</button>
                <p><strong>Total: S/. <span id="totalCarrito">0.00</span></strong></p>
            </div>
        </div>
    <?php endif; ?>
</div>

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
    let productoActual = {};
    let carrito = [];

    function abrirModalProducto(producto) {
        productoActual = producto;
        document.getElementById('modalProductoLabel').innerText = producto.nombre;
        document.getElementById('modalNombreProducto').innerText = producto.nombre;
        document.getElementById('modalDescripcionProducto').innerText = producto.descripcion || "Sin descripción.";
        document.getElementById('modalPrecioProducto').innerText = parseFloat(producto.precio_menor).toFixed(2);
        document.getElementById('modalCantidad').value = 1;

        new bootstrap.Modal(document.getElementById('modalProducto')).show();
    }

    function agregarAlCarrito() {
        const cantidad = parseInt(document.getElementById('modalCantidad').value);
        if (cantidad <= 0) return;

        const existente = carrito.find(p => p.id === productoActual.id);
        if (existente) {
            existente.cantidad += cantidad;
        } else {
            carrito.push({
                id: productoActual.id,
                nombre: productoActual.nombre,
                precio: parseFloat(productoActual.precio_menor),
                cantidad: cantidad
            });
        }

        document.getElementById('contadorCarrito').innerText = carrito.reduce((s, p) => s + p.cantidad, 0);
        actualizarCarrito();
        bootstrap.Modal.getInstance(document.getElementById('modalProducto')).hide();
    }

    function actualizarCarrito() {
        const contenedor = document.getElementById('contenidoCarrito');
        contenedor.innerHTML = '';

        let total = 0;
        carrito.forEach((p, i) => {
            const subtotal = p.precio * p.cantidad;
            total += subtotal;

            const item = document.createElement('div');
            item.className = 'mb-2';
            item.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${p.nombre}</strong><br>
                        <small>S/. ${p.precio.toFixed(2)} x ${p.cantidad} = S/. ${subtotal.toFixed(2)}</small>
                    </div>
                    <input type="number" min="1" value="${p.cantidad}" onchange="cambiarCantidad(${i}, this.value)" class="form-control form-control-sm w-25 text-end">
                </div>
            `;
            contenedor.appendChild(item);
        });

        document.getElementById('totalCarrito').innerText = total.toFixed(2);
    }

    function cambiarCantidad(index, valor) {
        carrito[index].cantidad = parseInt(valor);
        actualizarCarrito();
        document.getElementById('contadorCarrito').innerText = carrito.reduce((s, p) => s + p.cantidad, 0);
    }

    function mostrarCarrito() {
        new bootstrap.Offcanvas(document.getElementById('carritoCanvas')).show();
    }

    function enviarWhatsapp() {
        if (carrito.length === 0) {
            alert('El carrito está vacío.');
            return;
        }
    
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = 'prueba.php'; // <-- enviará los datos aquí
    
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'carrito';
        input.value = JSON.stringify(carrito);
    
        form.appendChild(input);
        document.body.appendChild(form);
        form.submit(); // <-- redireccionará con datos
    }
    

    document.addEventListener('keydown', e => {
        const carrusel = document.getElementById('catalogoCarrusel');
        if (e.key === 'ArrowRight') new bootstrap.Carousel(carrusel).next();
        if (e.key === 'ArrowLeft') new bootstrap.Carousel(carrusel).prev();
    });
</script>
</body>
</html>
