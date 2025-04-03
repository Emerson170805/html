<?php include("funcion_hojas.php"); ?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Gestión de Hojas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">

<div class="container py-4">
    <h2 class="mb-4"><?= $editarDatos ? "Editar Hoja" : "Agregar Nueva Hoja" ?></h2>

    <div class="card mb-4">
        <div class="card-body">
            <form method="POST" enctype="multipart/form-data">
                <input type="hidden" name="id" value="<?= $editarDatos['id'] ?? '' ?>">

                <div class="mb-3">
                    <label class="form-label">Nombre de la hoja:</label>
                    <input type="text" class="form-control" name="hoja" required value="<?= $editarDatos['hoja'] ?? '' ?>">
                </div>

                <div class="mb-3">
                    <label class="form-label">Imagen (máx. 10MB):</label>
                    <input type="file" class="form-control" name="imagen" <?= $editarDatos ? '' : 'required' ?>>
                </div>

                <div class="mb-3">
                    <label class="form-label">Posición:</label>
                    <input type="number" class="form-control" name="posicion" required min="1" value="<?= $editarDatos['posicion'] ?? '' ?>">
                </div>

                <button type="submit" name="<?= $editarDatos ? 'editar' : 'agregar' ?>" class="btn btn-primary">
                    <?= $editarDatos ? 'Actualizar' : 'Guardar' ?>
                </button>
            </form>
        </div>
    </div>

    <h2 class="mb-3">Lista de Hojas</h2>

    <div class="table-responsive">
        <table class="table table-bordered table-hover align-middle text-center bg-white">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Hoja</th>
                    <th>Imagen</th>
                    <th>Posición</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $result = $conn->query("SELECT * FROM hojas ORDER BY posicion ASC");
                while ($row = $result->fetch_assoc()):
                ?>
                <tr>
                    <td><?= $row['id'] ?></td>
                    <td><?= htmlspecialchars($row['hoja']) ?></td>
                    <td>
                        <?php if (!empty($row['imagen'])): ?>
                            <img src="data:image/jpeg;base64,<?= base64_encode($row['imagen']) ?>" class="img-thumbnail" style="max-height: 100px;">
                        <?php else: ?>
                            Sin imagen
                        <?php endif; ?>
                    </td>
                    <td><?= $row['posicion'] ?></td>
                    <td>
                        <a href="?editar=<?= $row['id'] ?>" class="btn btn-sm btn-warning">✏️ Editar</a>
                        <a href="?eliminar=<?= $row['id'] ?>" onclick="return confirm('¿Eliminar este registro?')" class="btn btn-sm btn-danger">🗑️ Eliminar</a>
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
