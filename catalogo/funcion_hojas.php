<?php
// Conexión a la base de datos
$host = "192.168.1.102";
$user = "emerson";
$pass = "77127859";
$dbname = "catalogo";

$conn = new mysqli($host, $user, $pass, $dbname);
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// Tamaño máximo en bytes (10MB)
$maxSize = 10 * 1024 * 1024;

// AGREGAR HOJA
if (isset($_POST['agregar'])) {
    $hoja = $_POST['hoja'];
    $posicion = intval($_POST['posicion']);

    // Validación del archivo
    if (!isset($_FILES['imagen']) || $_FILES['imagen']['error'] !== UPLOAD_ERR_OK) {
        die("Error al subir la imagen. Código: " . $_FILES['imagen']['error']);
    }

    if ($_FILES['imagen']['size'] > $maxSize) {
        die("La imagen supera el tamaño máximo permitido de 10MB.");
    }

    $imagen = file_get_contents($_FILES['imagen']['tmp_name']);

    // Verificar posición única
    $verifica = $conn->query("SELECT id FROM hojas WHERE posicion = $posicion");
    if ($verifica->num_rows > 0) {
        die("La posición ya está ocupada. Usa una diferente.");
    }

    // Insertar usando statement binario
    $stmt = $conn->prepare("INSERT INTO hojas (hoja, imagen, posicion) VALUES (?, ?, ?)");
    $null = NULL;
    $stmt->bind_param("sbi", $hoja, $null, $posicion);
    $stmt->send_long_data(1, $imagen);
    $stmt->execute();

    header("Location: hojas.php");
    exit();
}

// EDITAR HOJA
if (isset($_POST['editar'])) {
    $id = $_POST['id'];
    $hoja = $_POST['hoja'];
    $posicion = intval($_POST['posicion']);

    // Verificar posición única
    $verifica = $conn->query("SELECT id FROM hojas WHERE posicion = $posicion AND id != $id");
    if ($verifica->num_rows > 0) {
        die("Esa posición ya está asignada a otra hoja.");
    }

    if ($_FILES['imagen']['size'] > 0) {
        if ($_FILES['imagen']['size'] > $maxSize) {
            die("La imagen supera el tamaño máximo de 10MB.");
        }

        $imagen = file_get_contents($_FILES['imagen']['tmp_name']);
        $stmt = $conn->prepare("UPDATE hojas SET hoja=?, imagen=?, posicion=? WHERE id=?");
        $null = NULL;
        $stmt->bind_param("sbii", $hoja, $null, $posicion, $id);
        $stmt->send_long_data(1, $imagen);
        $stmt->execute();
    } else {
        $conn->query("UPDATE hojas SET hoja='$hoja', posicion=$posicion WHERE id=$id");
    }

    header("Location: hojas.php");
    exit();
}

// ELIMINAR HOJA
if (isset($_GET['eliminar'])) {
    $id = $_GET['eliminar'];
    $conn->query("DELETE FROM hojas WHERE id=$id");
    header("Location: hojas.php");
    exit();
}

// CARGAR HOJA PARA EDICIÓN
$editarDatos = null;
if (isset($_GET['editar'])) {
    $id = $_GET['editar'];
    $resultado = $conn->query("SELECT * FROM hojas WHERE id=$id");
    $editarDatos = $resultado->fetch_assoc();
}
?>
