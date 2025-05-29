from ultralytics import YOLO
import cv2

def detectar_camara_unica():
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return

    cv2.namedWindow("Detección en cámara - YOLOv8", cv2.WINDOW_NORMAL)  # Crear ventana una sola vez

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error leyendo la cámara")
            break

        results = model(frame)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])
                etiqueta = model.names[cls]

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                texto = f"{etiqueta} {conf:.2f}"
                cv2.putText(frame, texto, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


        cv2.imshow("Detección en cámara - YOLOv8", frame)  # Actualiza ventana única

        if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
            break

    cap.release()
    cv2.destroyAllWindows()

detectar_camara_unica()
