<?php include("funcion_productos.php"); ?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Gestión de Productos</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">

<div class="container py-4">
    <h2 class="mb-4"><?= $editarProducto ? "Editar Producto" : "Agregar Producto" ?></h2>

    <div class="card mb-4">
        <div class="card-body">
            <?php $hojas = $conn->query("SELECT id, hoja FROM hojas ORDER BY posicion ASC"); ?>
            <form method="POST">
                <input type="hidden" name="id" value="<?= $editarProducto['id'] ?? '' ?>">

                <div class="row mb-3">
                    <div class="col">
                        <label class="form-label">Nombre:</label>
                        <input type="text" class="form-control" name="nombre" required value="<?= $editarProducto['nombre'] ?? '' ?>">
                    </div>
                    <div class="col">
                        <label class="form-label">Hoja (asociada):</label>
                        <select name="id_hoja" class="form-select" required>
                            <option value="">Seleccione hoja</option>
                            <?php while ($h = $hojas->fetch_assoc()): ?>
                                <option value="<?= $h['id'] ?>" <?= (isset($editarProducto['id_hoja']) && $editarProducto['id_hoja'] == $h['id']) ? 'selected' : '' ?>>
                                    <?= htmlspecialchars($h['hoja']) ?>
                                </option>
                            <?php endwhile; ?>
                        </select>
                    </div>
                </div>

                <div class="row mb-3">
                    <div class="col">
                        <label class="form-label">Precio Mayor:</label>
                        <input type="number" step="0.01" class="form-control" name="precio_mayor" required value="<?= $editarProducto['precio_mayor'] ?? '' ?>">
                    </div>
                    <div class="col">
                        <label class="form-label">Precio Menor:</label>
                        <input type="number" step="0.01" class="form-control" name="precio_menor" required value="<?= $editarProducto['precio_menor'] ?? '' ?>">
                    </div>
                    <div class="col">
                        <label class="form-label">Stock:</label>
                        <input type="number" class="form-control" name="stock" required value="<?= $editarProducto['stock'] ?? '' ?>">
                    </div>
                </div>

                <div class="row mb-3">
                    <div class="col">
                        <label class="form-label">Horizontal (cm):</label>
                        <input type="number" step="0.01" class="form-control" name="horizontal" value="<?= $editarProducto['horizontal'] ?? '' ?>">
                    </div>
                    <div class="col">
                        <label class="form-label">Vertical (cm):</label>
                        <input type="number" step="0.01" class="form-control" name="vertical" value="<?= $editarProducto['vertical'] ?? '' ?>">
                    </div>
                </div>

                <button type="submit" name="<?= $editarProducto ? 'editar' : 'agregar' ?>" class="btn btn-primary">
                    <?= $editarProducto ? 'Actualizar' : 'Guardar' ?>
                </button>
            </form>
        </div>
    </div>

    <h2 class="mb-3">Lista de Productos</h2>

    <div class="table-responsive">
        <table class="table table-bordered table-hover align-middle text-center bg-white">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Mayor</th>
                    <th>Menor</th>
                    <th>Stock</th>
                    <th>Horizontal</th>
                    <th>Vertical</th>
                    <th>ID Hoja</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $productos = $conn->query("SELECT * FROM productos ORDER BY id DESC");
                while ($row = $productos->fetch_assoc()):
                ?>
                <tr>
                    <td><?= $row['id'] ?></td>
                    <td><?= htmlspecialchars($row['nombre']) ?></td>
                    <td><?= $row['precio_mayor'] ?></td>
                    <td><?= $row['precio_menor'] ?></td>
                    <td><?= $row['stock'] ?></td>
                    <td><?= $row['horizontal'] ?></td>
                    <td><?= $row['vertical'] ?></td>
                    <td><?= $row['id_hoja'] ?></td>
                    <td>
                        <a href="?editar=<?= $row['id'] ?>" class="btn btn-sm btn-warning">✏️</a>
                        <a href="?eliminar=<?= $row['id'] ?>" onclick="return confirm('¿Eliminar este producto?')" class="btn btn-sm btn-danger">🗑️</a>
                    </td>
                </tr>
                <?php endwhile; ?>
            </tbody>
        </table>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
