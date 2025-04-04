<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

require_once __DIR__ . '/fpdf/fpdf.php';

try {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (!isset($_POST['carrito'])) {
            throw new Exception('No se recibió el carrito.');
        }

        $carrito = json_decode($_POST['carrito'], true);
        if (!$carrito || !is_array($carrito)) {
            throw new Exception('Carrito vacío o malformado.');
        }

        class PDF extends FPDF {
            function Header() {
                $this->SetFont('Arial', 'B', 14);
                $this->Cell(0, 10, mb_convert_encoding('Lista de Productos del Carrito', 'ISO-8859-1', 'UTF-8'), 0, 1, 'C');
                $this->Ln(5);
            }

            function Footer() {
                $this->SetY(-15);
                $this->SetFont('Arial', 'I', 8);
                $this->Cell(0, 10, mb_convert_encoding('Página ' . $this->PageNo(), 'ISO-8859-1', 'UTF-8'), 0, 0, 'C');
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
            $pdf->Cell(100, 10, mb_convert_encoding($item['nombre'], 'ISO-8859-1', 'UTF-8'), 1);
            $pdf->Cell(40, 10, 'S/. ' . number_format($item['precio'], 2), 1, 0, 'R');
            $pdf->Cell(40, 10, $item['cantidad'], 1, 0, 'C');
            $pdf->Ln();
        }

        $filename = 'productos_carrito.pdf';
        $filepath = __DIR__ . '/' . $filename;
        $pdf->Output('F', $filepath);

        if (!file_exists($filepath)) {
            throw new Exception('No se pudo generar el archivo PDF.');
        }

        echo json_encode(['file' => $filename]);
        exit;
    } else {
        throw new Exception('Método no permitido.');
    }
} catch (Throwable $e) {
    echo "<h2>Error en la generación del PDF</h2>";
    echo "<pre>";
    echo htmlspecialchars($e->getMessage()) . "\n\n";
    echo htmlspecialchars($e->getTraceAsString());
    echo "</pre>";
    exit;
}
