<?php
require 'funciones.php';
$hojas = obtenerHojas();
$productos = obtenerProductos();
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo Interactivo</title>
    <link rel="stylesheet" href="estilos/style1.css">
</head>
<body>
    <header>
        <h1>CATÁLOGO INTERACTIVO</h1>
    </header>

    <div class="container">
        <div class="slider">
            <div class="slides">
                <?php foreach ($hojas as $hoja): ?>
                    <div class="slide">
                        <?php if (!empty($hoja['id'])): ?>
                            <img src="imagen.php?id=<?= $hoja['id'] ?>" alt="Imagen hoja <?= $hoja['hoja'] ?>">
                        <?php endif; ?>
                        <div class="productos-container">
                            <?php foreach ($productos as $producto): ?>
                                <?php if ($producto['id_hoja'] == $hoja['id']): ?>
                                    <button class="producto-btn"
                                            style="left: <?= $producto['horizontal'] ?>%; top: <?= $producto['vertical'] ?>%;"
                                            onclick="mostrarInfo('<?= htmlspecialchars($producto['nombre']) ?>', <?= $producto['precio_menor'] ?>)">
                                        <?= htmlspecialchars($producto['nombre']) ?>
                                    </button>
                                <?php endif; ?>
                            <?php endforeach; ?>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        </div>

        <div class="slide-buttons">
            <button class="prev" onclick="prevSlide()">❮</button>
            <button class="next" onclick="nextSlide()">❯</button>
        </div>
    </div>

    <!-- Modal de producto -->
    <div class="modal" id="modal-info">
        <div class="modal-content">
            <span class="close" onclick="cerrarModal()">&times;</span>
            <h2 id="modal-titulo"></h2>
            <p id="modal-precio"></p>
            <button onclick="agregarAlCarrito()">Agregar al carrito 🛒</button>
        </div>
    </div>

    <!-- Panel lateral del carrito -->
    <div class="carrito" id="carrito">
        <h3>🛒 Carrito</h3>
        <ul id="lista-carrito"></ul>
        <h4>Total: S/. <span id="total-general">0.00</span></h4>
        <button class="send-whatsapp" onclick="enviarWhatsApp()">Enviar por WhatsApp</button>
    </div>

    <!-- Botón flotante del carrito -->
    <div class="carrito-icono" onclick="toggleCarrito()">🛒</div>

    <script src="scripts/main.js"></script>
</body>
</html>