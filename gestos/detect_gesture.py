import cv2
import mediapipe as mp
import joblib
import sys

# Cargar modelo
try:
    model = joblib.load('model/gesture_knn.pkl')
    print("✅ Modelo cargado correctamente")
except Exception as e:
    print("❌ Error al cargar el modelo:", e)
    sys.exit(1)

# Configurar MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

def mostrar_camara():
    # Intentar con diferentes índices de cámara
    for camera_index in [2]:
        cap = cv2.VideoCapture(camera_index)
        if cap.isOpened():
            print(f"📷 Cámara encontrada en índice {camera_index}")
            break
    else:
        print("❌ No se pudo encontrar ninguna cámara disponible")
        return False

    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Error leyendo el frame. Reintentando...")
                # Intentar reconectar la cámara
                cap.release()
                cap = cv2.VideoCapture(camera_index)
                continue

            # Procesamiento de imagen
            frame = cv2.flip(frame, 1)  # Voltear horizontalmente para efecto espejo
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(img_rgb)

            if result.multi_hand_landmarks:
                for handLms in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                    landmarks = [coord for lm in handLms.landmark for coord in (lm.x, lm.y, lm.z)]
                    
                    if len(landmarks) == 63:  # 21 landmarks * 3 coordenadas
                        try:
                            pred = model.predict([landmarks])[0]
                            cv2.putText(frame, f'Gesto: {pred}', (10, 50), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                                       cv2.LINE_AA)
                        except Exception as e:
                            print(f"⚠️ Error en predicción: {e}")

            cv2.imshow("Reconocimiento de Gestos", frame)

            # Control de salida
            key = cv2.waitKey(1)
            if key == 27:  # Tecla ESC
                print("🛑 Programa terminado por el usuario")
                cap.release()
                cv2.destroyAllWindows()
                return True
            elif key == ord('r'):  # Tecla R para reiniciar
                print("🔄 Reiniciando cámara...")
                cap.release()
                cv2.destroyAllWindows()
                return False

            # Verificar si la ventana fue cerrada
            if cv2.getWindowProperty("Reconocimiento de Gestos", cv2.WND_PROP_VISIBLE) < 1:
                print("🔄 Ventana cerrada. Reiniciando...")
                cap.release()
                cv2.destroyAllWindows()
                return False

        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")
            cap.release()
            cv2.destroyAllWindows()
            return False

# Bucle principal
while True:
    print("\nIniciando sistema de reconocimiento...")
    salir = mostrar_camara()
    if salir:
        break
    print("Reiniciando en 2 segundos...")
    cv2.waitKey(2000)  # Pequeña pausa antes de reiniciar