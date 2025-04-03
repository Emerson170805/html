<?php
require_once 'conexion.php';

if (isset($_GET['id'])) {
    $id = intval($_GET['id']);
    $conn = conectar();

    $stmt = $conn->prepare("SELECT imagen FROM hojas WHERE id = ?");
    $stmt->execute([$id]);
    $fila = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($fila && !empty($fila['imagen'])) {
        header("Content-Type: image/jpeg"); // Cambia esto si agregas mime_type más adelante
        echo $fila['imagen'];
        exit;
    }
}

http_response_code(404);
echo "Imagen no encontrada.";
exit;
?>
