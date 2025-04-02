// conexion.php
<?php
function conectar() {
    $host = "localhost";
    $usuario = "emerson";
    $clave = "77127859";
    $bd = "catalogo";

    try {
        $conexion = new PDO("mysql:host=$host;dbname=$bd;charset=utf8", $usuario, $clave);
        $conexion->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        return $conexion;
    } catch (PDOException $e) {
        die("Conexión fallida: " . $e->getMessage());
    }
}
?>