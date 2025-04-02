import asyncio
import cv2
import mediapipe as mp
import websockets
import json

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

async def send_hand_data(websocket):
    print("🟢 Cliente conectado")
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            move_x = move_y = rotation_x = rotation_y = zoom_distance = None

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    thumb_tip = hand_landmarks.landmark[4]
                    index_tip = hand_landmarks.landmark[8]
                    pinky_tip = hand_landmarks.landmark[20]

                    if abs(thumb_tip.x - pinky_tip.x) < 0.05:
                        move_x, move_y = thumb_tip.x - 0.5, thumb_tip.y - 0.5

                    if abs(thumb_tip.x - index_tip.x) < 0.05:
                        rotation_x, rotation_y = index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y

            await websocket.send(json.dumps({
                "move_x": move_x,
                "move_y": move_y,
                "rotation_x": rotation_x,
                "rotation_y": rotation_y,
                "zoom_distance": zoom_distance
            }))

            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            cv2.imshow("Detección de Manos", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except websockets.exceptions.ConnectionClosedError:
        print("🔴 Cliente desconectado.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

async def main():
    print("🔵 Servidor WebSocket corriendo en ws://localhost:5000")
    async with websockets.serve(send_hand_data, "0.0.0.0", 5000):
        await asyncio.Future()

asyncio.run(main())
