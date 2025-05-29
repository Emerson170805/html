import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp

# Configurar TensorFlow para que use la GPU con crecimiento de memoria limitado
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

def main():
    print("GPUs disponibles:", tf.config.list_physical_devices('GPU'))

    modelo = tf.keras.models.load_model('modelo_emociones.h5')
    etiquetas = ['feliz', 'neutral', 'sorprendido', 'triste']

    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara.")
        return

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=10,  # Detectar hasta 10 rostros
        min_detection_confidence=0.5
    )

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error al capturar imagen.")
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resultados = face_mesh.process(rgb)

            if resultados.multi_face_landmarks:
                h, w, _ = frame.shape
                for rostro in resultados.multi_face_landmarks:
                    puntos = [(int(p.x * w), int(p.y * h)) for p in rostro.landmark]
                    xs, ys = zip(*puntos)
                    x1, y1 = max(min(xs) - 10, 0), max(min(ys) - 10, 0)
                    x2, y2 = min(max(xs) + 10, w), min(max(ys) + 10, h)

                    rostro_img = frame[y1:y2, x1:x2]
                    if rostro_img.size == 0:
                        continue

                    gris = cv2.cvtColor(rostro_img, cv2.COLOR_BGR2GRAY)
                    redimensionado = cv2.resize(gris, (48, 48)) / 255.0
                    entrada = np.expand_dims(np.expand_dims(redimensionado, -1), 0)

                    pred = modelo.predict(entrada, verbose=0)
                    emocion = etiquetas[np.argmax(pred)]

                    cv2.putText(frame, emocion, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

            cv2.imshow("Detector de emociones", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Tecla ESC para salir
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        face_mesh.close()

if __name__ == "__main__":
    main()
