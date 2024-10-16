try:
    import cv2
    import numpy as np
except ImportError:
    print("Advertencia: La librería 'opencv-python' no está instalada. Por favor, instálala usando 'pip install opencv-python'.")
    exit(1)

import time
import os

from datetime import datetime

# Verificar que la carpeta 'img' existe, si no, crearla
if not os.path.exists('img'):
    os.makedirs('img')

# Identifica las webcams activas disponibles
# def listar_webcams():
#     index = 0
#     arr = []
#     while True:
#         cap = cv2.VideoCapture(index)
#         if not cap.read()[0]:
#             break
#         else:
#             arr.append(index)
#         cap.release()
#         index += 1
#     return arr

# webcams_disponibles = listar_webcams()
# print(f"Webcams disponibles: {webcams_disponibles}")

# Inicializar la captura de video de la webcam que tengas disponible
cap = cv2.VideoCapture(0)

# Leer el primer frame para usar como referencia
ret, frame1 = cap.read()
frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
frame1_gray = cv2.GaussianBlur(frame1_gray, (21, 21), 0)

# Definir el intervalo de tiempo entre frames (en segundos)
frame_interval = 1/4  # 4 frames por segundo
# Si quieres más detecciones, puedes reducir el intervalo de tiempo, i.e. 1/16 -> 16 fps, 1/30 -> 30 fps
# Si quieres menos detecciones, puedes aumentar el intervalo de tiempo, i.e. 1 -> 1 fps o 2 -> 0.5 fps

# Posiciones de las ventanas
cv2.namedWindow("Feed de video")
cv2.moveWindow("Feed de video", 0, 0)

cv2.namedWindow("Umbral")
cv2.moveWindow("Umbral", 640, 0)

cv2.namedWindow("Diferencia de frames")
cv2.moveWindow("Diferencia de frames", 1280, 0)

while True:
    # Leer el siguiente frame
    ret, frame2 = cap.read()
    if not ret:
        break

    # Convertir a escala de grises y aplicar desenfoque gaussiano
    frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    frame2_gray = cv2.GaussianBlur(frame2_gray, (21, 21), 0)

    # Calcular la diferencia absoluta entre el primer frame y el actual
    frame_delta = cv2.absdiff(frame1_gray, frame2_gray)
    # Aplicar un umbral para binarizar la imagen
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    # Dilatar la imagen para reducir el ruido
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Encontrar contornos en la imagen umbralizada
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        motion_detected = True
        # Dibujar rectángulos alrededor del movimiento detectado
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 100, 0), 1)

    # Mostrar el frame con las detecciones
    cv2.imshow("Feed de video", frame2)
    cv2.imshow("Umbral", thresh)
    cv2.imshow("Diferencia de frames", frame_delta)

    # Si se detecta movimiento, guardar la imagen
    if motion_detected:
        # Imprimir mensaje de movimiento detectado
        tiempo_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
        print(f"Movimiento detectado @ {tiempo_actual} ", end="")
        # Dependiendod e la webcam que tengas, puede cambiar el tamaño de la imagen, por ende su peso
        #   Nota que si la imagen es muy pesada, puede tardar en guardarse, por eso el parametro de IMWRITE_JPEG_QUALITY
        #   Puedes ajustar la calidad de la imagen para reducir su peso, pero que considero que el 30% es suficiente para visualizar
        #   Si quieres una imagen de mayor calidad, puedes aumentar el porcentaje incluso a un 70%
        if cv2.imwrite(f"./img/movimiento_detectado_{tiempo_actual}.jpg", frame2, [cv2.IMWRITE_JPEG_QUALITY, 30]):
            # Si la imagen se guardó correctamente, imprimir un mensaje
            print("Imagen guardada", end="")
        else:
            # Si la imagen no se guardó correctamente, imprimir un mensaje de error
            print("Error al guardar la imagen", end="")
        print('.')
        time.sleep(1)
        # Puedes agregar lógica adicional si no quieres múltiples capturas consecutivas

    # Actualizar el frame de referencia
    frame1_gray = frame2_gray.copy()

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Esperar el intervalo de tiempo definido
    time.sleep(frame_interval)

# Liberar recursos y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
