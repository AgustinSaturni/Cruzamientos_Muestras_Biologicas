import cv2
import numpy as np


def cruce(imagen_importante, contornos_importantes, imagen_secundaria, contornos_secundarios, color):
    if color == "verde":
        color_contorno = (0, 255, 0)
    if color == "azul":
        color_contorno = (0, 0, 255)
    if color == "rojo":
        color_contorno = (255, 0, 0)

    # Crear una máscara negra para los contornos de contacto
    imagen_contactos = np.zeros_like(imagen_importante)  # Esto crea una imagen negra del mismo tamaño

    # Crear una imagen en blanco para dibujar los contornos
    contornos_comunes = np.zeros_like(imagen_secundaria)

    # Dibujar los contornos de la imagen secundaria en blanco
    cv2.drawContours(contornos_comunes, contornos_secundarios, -1, (255, 255, 255), 1)

    # Variable para almacenar la suma de las áreas
    suma_areas = 0

    # Lista para almacenar los contornos que dieron positivo
    contornos_positivos = []

    # Comparar los contornos de la imagen importante con los de la imagen secundaria
    for contorno_importante in contornos_importantes:
        contacto_encontrado = False

        # Verificar si algún punto del contorno importante toca un contorno secundario
        for punto in contorno_importante:
            x, y = punto[0]
            # Si el punto del contorno importante toca algún contorno secundario
            if contornos_comunes[y, x].all() != 0:
                # Dibujar el contorno importante en la imagen de contacto
                cv2.drawContours(imagen_contactos, [contorno_importante], -1, color_contorno, 2)
                # Calcular el área del contorno importante y sumarla
                suma_areas += cv2.contourArea(contorno_importante)
                contacto_encontrado = True
                contornos_positivos.append(contorno_importante)  # Agregar el contorno a la lista de positivos
                break

        # Si no se encontró contacto, verificar si el contorno importante contiene algún contorno secundario
        if not contacto_encontrado:
            for contorno_secundario in contornos_secundarios:
                for punto in contorno_secundario:
                    x, y = punto[0]
                    punto2 = (float(x), float(y))  # Convertir a float los puntos
                    resultado = cv2.pointPolygonTest(contorno_importante, punto2, False)

                    if resultado == 1:  # El punto está dentro del contorno importante
                        # Dibujar el contorno importante en la imagen de contacto
                        cv2.drawContours(imagen_contactos, [contorno_importante], -1, color_contorno, 2)
                        # Calcular el área del contorno importante y sumarla
                        suma_areas += cv2.contourArea(contorno_importante)
                        contornos_positivos.append(contorno_importante)  # Agregar el contorno a la lista de positivos
                        break

    return imagen_contactos, suma_areas, contornos_positivos
