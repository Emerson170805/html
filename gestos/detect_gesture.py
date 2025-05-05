import cv2
import mediapipe as mp
import joblib
import numpy as np
import sys

def normalize_landmarks(landmarks):
    """Normaliza los landmarks para hacerlos invariantes a posición y tamaño"""
    landmarks = np.array(landmarks).reshape(-1, 3)
    wrist = landmarks[0]  # Usamos la muñeca como punto de referencia
    landmarks -= wrist  # Centramos los puntos
    max_value = np.max(np.abs(landmarks))
    if max_value != 0:
        landmarks /= max_value  # Normalizamos a [-1, 1]
    return landmarks.flatten().tolist()

# Cargar modelo y label encoder
try:
    model = joblib.load('model/gesture_svm.pkl')
    le = joblib.load('model/label_encoder.pkl')
    print("✅ Modelo y encoder cargados correctamente")
except Exception as e:
    print(f"❌ Error al cargar los modelos: {e}")
    sys.exit(1)

# Configurar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

def initialize_camera(camera_index=0):
    """Intenta inicializar la cámara con diferentes índices"""
    for index in [camera_index, 0, 2, 3]:  # Prueba diferentes índices
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            print(f"📷 Cámara encontrada en índice {index}")
            return cap
    return None

def main():
    cap = initialize_camera(2)  # Cambia este número según tu cámara
    if not cap:
        print("❌ No se pudo inicializar ninguna cámara")
        return

    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Error leyendo el frame. Reintentando...")
                cap.release()
                cap = initialize_camera()
                if not cap:
                    break
                continue

            # Procesamiento de la imagen
            frame = cv2.flip(frame, 1)  # Efecto espejo
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(img_rgb)

            if result.multi_hand_landmarks:
                for handLms in result.multi_hand_landmarks:
                    # Dibujar landmarks
                    mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                    
                    # Extraer y normalizar landmarks
                    landmarks = [coord for lm in handLms.landmark for coord in (lm.x, lm.y, lm.z)]
                    if len(landmarks) == 63:  # 21 landmarks × 3 coordenadas
                        try:
                            norm_landmarks = normalize_landmarks(landmarks)
                            pred = model.predict([norm_landmarks])[0]
                            label = le.inverse_transform([pred])[0]
                            
                            # Mostrar predicción
                            cv2.putText(frame, f'Gesto: {label}', (10, 50),
                                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,
                                       cv2.LINE_AA)
                        except Exception as e:
                            print(f"⚠️ Error en predicción: {e}")

            # Mostrar frame
            cv2.imshow("Reconocimiento de Gestos", frame)

            # Control de salida
            key = cv2.waitKey(10)
            if key == 27:  # ESC para salir
                print("🛑 Programa terminado por el usuario")
                break
            elif key == ord('r'):  # R para reiniciar
                print("🔄 Reiniciando cámara...")
                cap.release()
                cap = initialize_camera()
                if not cap:
                    break

        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()