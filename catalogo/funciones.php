<?php
require_once 'conexion.php';

function obtenerHojas() {
    $conexion = conectar();
    $stmt = $conexion->query("SELECT * FROM hojas");
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

function obtenerProductos() {
    $conexion = conectar();
    $stmt = $conexion->query("SELECT * FROM productos");
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

function obtenerImagenHoja($id) {
    $conexion = conectar();
    $stmt = $conexion->prepare("SELECT imagen FROM hojas WHERE id = ?");
    $stmt->execute([$id]);
    return $stmt->fetch(PDO::FETCH_ASSOC);
}
?>