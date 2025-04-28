from ultralytics import YOLO
import cv2

# Cargar el modelo YOLOv8 preentrenado
# Puedes usar 'yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt', o 'yolov8x.pt' según tu necesidad
model = YOLO('yolov8n.pt')  # Elige un modelo más grande si quieres mejor precisión

# Abrir la cámara o un video
cap = cv2.VideoCapture(0)  # Usa 0 para la webcam o coloca la ruta de un video aquí

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Realizar la detección
    results = model.predict(frame, conf=0.5)  # Puedes ajustar el 'conf' (confidence threshold)

    # Dibujar resultados
    annotated_frame = results[0].plot()

    # Mostrar el frame
    cv2.imshow("Reconocimiento de animales con YOLOv8", annotated_frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
