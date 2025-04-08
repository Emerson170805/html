import cv2

def main():
    # Intentar abrir la cámara 2
    cap = cv2.VideoCapture(2)

    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara 2.")
        return

    cv2.namedWindow("Cámara 2", cv2.WINDOW_NORMAL)  # Asegura una sola ventana

    print("Presiona ESPACIO para capturar la foto. Presiona ESC para salir.")

    ventana_abierta = True

    while ventana_abierta:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error al leer desde la cámara.")
            break

        # Mostrar el frame en una única ventana
        cv2.imshow("Cámara 2", frame)

        key = cv2.waitKey(1)
        if key == 27:  # ESC para salir
            ventana_abierta = False
        elif key == 32:  # Espacio para tomar la foto
            cv2.imwrite("foto_capturada.jpg", frame)
            print("📸 Foto guardada como 'foto_capturada.jpg'")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
