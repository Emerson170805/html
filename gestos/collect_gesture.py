import cv2
import mediapipe as mp
import csv
import time
import os

gesture_name = input("Nombre del gesto: ")
save_path = f'gestures/{gesture_name}.csv'
os.makedirs('gestures', exist_ok=True)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(2)

start_time = time.time()
duration = 20 #segundos

with open(save_path, mode='a', newline='') as f:
    writer = csv.writer(f)
    print(f"Grabando gesto '{gesture_name}' por {duration} segundos...")
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                landmarks = []
                for lm in handLms.landmark:
                    landmarks.extend([lm.x, lm.y, lm.z])
                if len(landmarks) == 63:
                    writer.writerow(landmarks + [gesture_name])

        cv2.imshow("Recolectando gesto", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
print("Datos guardados en", save_path)
