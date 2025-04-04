<?php
// Mostrar errores y capturar salida para escribir errores en un archivo
ini_set('display_errors', 1);
error_reporting(E_ALL);
ob_start();

header('Content-Type: application/json');

require_once __DIR__ . '/fpdf/fpdf.php';

try {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (!isset($_POST['carrito'])) {
            echo json_encode(['error' => 'No se recibió el carrito.']);
            exit;
        }

        $carrito = json_decode($_POST['carrito'], true);

        if (!$carrito || !is_array($carrito)) {
            echo json_encode(['error' => 'Carrito vacío o malformado.']);
            exit;
        }

        class PDF extends FPDF {
            function Header() {
                $this->SetFont('Arial', 'B', 14);
                $this->Cell(0, 10, utf8_decode('Lista de Productos del Carrito'), 0, 1, 'C');
                $this->Ln(5);
            }

            function Footer() {
                $this->SetY(-15);
                $this->SetFont('Arial', 'I', 8);
                $this->Cell(0, 10, utf8_decode('Página ') . $this->PageNo(), 0, 0, 'C');
            }
        }

        $pdf = new PDF();
        $pdf->AddPage();
        $pdf->SetFont('Arial', 'B', 12);
        $pdf->Cell(100, 10, 'Producto', 1);
        $pdf->Cell(40, 10, 'Precio', 1);
        $pdf->Cell(40, 10, 'Cantidad', 1);
        $pdf->Ln();

        $pdf->SetFont('Arial', '', 12);
        foreach ($carrito as $item) {
            $pdf->Cell(100, 10, utf8_decode($item['nombre']), 1);
            $pdf->Cell(40, 10, 'S/. ' . number_format($item['precio'], 2), 1, 0, 'R');
            $pdf->Cell(40, 10, $item['cantidad'], 1, 0, 'C');
            $pdf->Ln();
        }

        $filename = 'productos_carrito.pdf';
        $filepath = __DIR__ . '/' . $filename;
        $pdf->Output('F', $filepath);

        if (!file_exists($filepath)) {
            echo json_encode(['error' => 'No se pudo generar el PDF.']);
            exit;
        }

        echo json_encode(['file' => $filename]);
        exit;
    } else {
        echo json_encode(['error' => 'Método no permitido.']);
        exit;
    }
} catch (Throwable $e) {
    $errorLog = __DIR__ . '/error_pdf_log.txt';
    file_put_contents($errorLog, ob_get_clean() . "\n" . $e->getMessage() . "\n" . $e->getTraceAsString());
    echo json_encode(['error' => 'Error interno, revisa error_pdf_log.txt']);
    exit;
}
