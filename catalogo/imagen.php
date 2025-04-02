<?php
require_once 'funciones.php';

if (isset($_GET['id'])) {
    $fila = obtenerImagenHoja($_GET['id']);

    if ($fila && $fila['imagen']) {
        header("Content-Type: image/jpeg");
        echo $fila['imagen'];
    }
}
?>