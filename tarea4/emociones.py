import cv2
import mediapipe as mp
from deepface import DeepFace

# Inicializar Mediapipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Iniciar la captura de video
cap = cv2.VideoCapture(2)

# Definir colores para diferentes emociones
color_emociones = {
    "angry": (0, 0, 255),      # Rojo
    "disgust": (0, 128, 0),    # Verde oscuro
    "fear": (128, 0, 128),     # Morado
    "happy": (0, 255, 255),    # Amarillo
    "neutral": (255, 255, 255),# Blanco
    "sad": (255, 0, 0),        # Azul
    "surprise": (255, 165, 0)  # Naranja
}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a RGB (Mediapipe usa RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar malla facial
    results = face_mesh.process(rgb_frame)

    # Dibujar la malla facial si se detecta un rostro
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                h, w, _ = frame.shape
                x, y = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

    try:
        # Analizar la emoción del rostro
        resultado = DeepFace.analyze(rgb_frame, actions=['emotion'], enforce_detection=False)
        emocion = resultado[0]['dominant_emotion']

        # Traducir emoción al español
        traducciones = {
            "angry": "Enojado",
            "disgust": "Disgustado",
            "fear": "Miedo",
            "happy": "Feliz",
            "neutral": "Neutral",
            "sad": "Triste",
            "surprise": "Sorprendido"
        }

        emocion_texto = traducciones.get(emocion, "Desconocido")

        # Obtener color correspondiente a la emoción
        color = color_emociones.get(emocion, (255, 255, 255))

        # Mostrar la emoción detectada en pantalla con color
        cv2.putText(frame, f"Emoción: {emocion_texto}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

    except Exception as e:
        print(f"Error: {e}")

    # Mostrar la imagen con la malla facial y la emoción
    cv2.imshow("Detector de emociones con malla facial", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
