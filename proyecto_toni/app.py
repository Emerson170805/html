import asyncio
import cv2
import mediapipe as mp
import websockets
import json

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Abrir cámara
cap = cv2.VideoCapture(0)

async def send_hand_data(websocket, path):  # ✅ IMPORTANTE: debe recibir 'websocket' y 'path'
    print("🟢 Cliente conectado")
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                continue

            # Procesar imagen
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            hand_data = []
            thumb_positions = []

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for idx, landmark in enumerate(hand_landmarks.landmark):
                        hand_data.append({
                            "id": idx,
                            "x": landmark.x,
                            "y": landmark.y
                        })
                        if idx == 4:  # pulgar
                            thumb_positions.append((landmark.x, landmark.y))

            # Si hay 2 pulgares, calcular distancia para zoom
            zoom_distance = None
            if len(thumb_positions) == 2:
                x1, y1 = thumb_positions[0]
                x2, y2 = thumb_positions[1]
                zoom_distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5

            # Enviar por WebSocket
            await websocket.send(json.dumps({
                "hands": hand_data,
                "zoom_distance": zoom_distance
            }))

            await asyncio.sleep(1 / 30)  # ~30 FPS

    except websockets.exceptions.ConnectionClosed:
        print("🔴 Cliente desconectado")
    finally:
        cap.release()
        cv2.destroyAllWindows()

async def main():
    print("🔵 Servidor WebSocket en ws://localhost:5050")
    async with websockets.serve(send_hand_data, "localhost", 5050):  # ✅ Ya no dará error
        await asyncio.Future()  # Mantener servidor corriendo

# Ejecutar
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Servidor detenido")
        cap.release()
        cv2.destroyAllWindows()
