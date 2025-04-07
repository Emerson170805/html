# Instalar antes:
# pip install ultralytics opencv-python

from ultralytics import YOLO
import cv2

# Cargar el modelo YOLOv8 pre-entrenado
modelo = YOLO('yolov8n.pt')

# Iniciar captura desde la cámara web
camara = cv2.VideoCapture(0)

# Asegurar que la cámara esté abierta correctamente
if not camara.isOpened():
    print("Error: No se puede acceder a la cámara.")
    exit()

# Crear ventana en pantalla completa
cv2.namedWindow('YOLO Tiempo Real', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('YOLO Tiempo Real', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    # Leer frame desde la cámara
    ret, frame = camara.read()

    if not ret:
        print("Error: No se puede recibir el frame desde la cámara.")
        break

    # Hacer predicción (detección de objetos)
    resultados = modelo.predict(frame, stream=True, verbose=False)

    # Procesar resultados
    for res in resultados:
        cajas = res.boxes.xyxy.cpu().numpy()
        confianzas = res.boxes.conf.cpu().numpy()
        clases = res.boxes.cls.cpu().numpy()
        nombres = res.names

        # Dibujar cajas y etiquetas
        for caja, confianza, clase in zip(cajas, confianzas, clases):
            x1, y1, x2, y2 = map(int, caja)
            etiqueta = f"{nombres[int(clase)]} {confianza:.2f}"

            # Dibujar caja
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Fondo de etiqueta
            (ancho, alto), _ = cv2.getTextSize(etiqueta, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (x1, y1 - alto - 10), (x1 + ancho, y1), (0, 255, 0), cv2.FILLED)

            # Texto etiqueta
            cv2.putText(frame, etiqueta, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Mostrar frame en pantalla completa
    cv2.imshow('YOLO Tiempo Real', frame)

    # Salir al pulsar la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
camara.release()
cv2.destroyAllWindows()
