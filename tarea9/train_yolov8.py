from ultralytics import YOLO

# Cargar el modelo YOLOv8 base (puedes cambiar a yolov8s.pt, yolov8m.pt, etc.)
model = YOLO("yolov8n.pt")  # n = nano, rápido y ligero

# Entrenar el modelo
model.train(
    data="/var/www/html/html/tarea9/data_set/data.yaml",  # Ruta a tu archivo YAML
    epochs=100,                 # Número de épocas
    imgsz=640,                  # Tamaño de las imágenes
    batch=16,                   # Tamaño del batch
    device=0,                   # Usa GPU CUDA (0 = primera GPU)
)
