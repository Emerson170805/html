<?php
// Ejecuta el servidor Python si aún no está corriendo
exec("nohup python3 app.py > /dev/null 2>&1 &");

// Redirige al index.html
header("Location: index.html");
exit();
?>
