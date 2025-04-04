<?php
// Conexión
$host = "192.168.1.102";
$user = "emerson";
$pass = "77127859";
$dbname = "catalogo";

$conn = new mysqli($host, $user, $pass, $dbname);
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// AGREGAR
if (isset($_POST['agregar'])) {
    $nombre = $_POST['nombre'];
    $descripcion = $_POST['descripcion'];
    $precio_mayor = $_POST['precio_mayor'];
    $precio_menor = $_POST['precio_menor'];
    $stock = $_POST['stock'];
    $horizontal = $_POST['horizontal'];
    $vertical = $_POST['vertical'];
    $id_hoja = $_POST['id_hoja'];

    $stmt = $conn->prepare("INSERT INTO productos (nombre, descripcion, precio_mayor, precio_menor, stock, horizontal, vertical, id_hoja) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("ssddiidi", $nombre, $descripcion, $precio_mayor, $precio_menor, $stock, $horizontal, $vertical, $id_hoja);
    $stmt->execute();
    header("Location: productos.php");
    exit();
}

// EDITAR
if (isset($_POST['editar'])) {
    $id = $_POST['id'];
    $nombre = $_POST['nombre'];
    $descripcion = $_POST['descripcion'];
    $precio_mayor = $_POST['precio_mayor'];
    $precio_menor = $_POST['precio_menor'];
    $stock = $_POST['stock'];
    $horizontal = $_POST['horizontal'];
    $vertical = $_POST['vertical'];
    $id_hoja = $_POST['id_hoja'];

    $stmt = $conn->prepare("UPDATE productos SET nombre=?, descripcion=?, precio_mayor=?, precio_menor=?, stock=?, horizontal=?, vertical=?, id_hoja=? WHERE id=?");
    $stmt->bind_param("ssddiidii", $nombre, $descripcion, $precio_mayor, $precio_menor, $stock, $horizontal, $vertical, $id_hoja, $id);
    $stmt->execute();
    header("Location: productos.php");
    exit();
}

// ELIMINAR
if (isset($_GET['eliminar'])) {
    $id = $_GET['eliminar'];
    $conn->query("DELETE FROM productos WHERE id=$id");
    header("Location: productos.php");
    exit();
}

// CARGAR PARA EDICIÓN
$editarProducto = null;
if (isset($_GET['editar'])) {
    $id = $_GET['editar'];
    $res = $conn->query("SELECT * FROM productos WHERE id=$id");
    $editarProducto = $res->fetch_assoc();
}