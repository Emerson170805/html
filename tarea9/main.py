from ultralytics import YOLO
import cv2

clases = ['feliz', 'normal', 'raiva', 'surpreso', 'triste']

def detectar_expresiones_en_vivo(cam_index=2, model_path='yolo11n.pt'):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print(f"No se pudo abrir la cámara {cam_index}")
        return

    ventana = f"Detección expresiones - Modelo {model_path}"
    cv2.namedWindow(ventana, cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se recibió frame")
            break

        results = model(frame)[0]

        for box, cls, score in zip(results.boxes.xyxy, results.boxes.cls, results.boxes.conf):
            clase_idx = int(cls)
            # Solo procesar si clase_idx está dentro de rango
            if clase_idx >= 0 and clase_idx < len(clases):
                x1, y1, x2, y2 = map(int, box)
                etiqueta = clases[clase_idx]
                confianza = float(score)

                if confianza > 0.5:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    texto = f"{etiqueta} {confianza:.2f}"
                    cv2.putText(frame, texto, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (0,255,0), 2)
            else:
                print(f"Clase desconocida detectada: {clase_idx}")

        cv2.imshow(ventana, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detectar_expresiones_en_vivo(cam_index=2, model_path='yolo11n.pt')
