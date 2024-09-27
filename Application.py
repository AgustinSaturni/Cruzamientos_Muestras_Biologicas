import cv2
import numpy as np
import matplotlib.pyplot as plt
from Functions import Cruzar
import os
import json

# Obtener el directorio actual del script
directorio_actual = os.path.dirname(__file__)

def dibujar_y_eliminar_restante(imagen_gris, contornos,color):
    if color == "verde":
        color_contorno = (0, 255, 0)
    if color == "azul":
        color_contorno = (0, 0, 255)
    if color == "rojo":
        color_contorno = (255, 0, 0)
    # Crear una máscara negra del mismo tamaño que la imagen original
    mascara = np.zeros_like(imagen_gris)  
    # Dibujar los contornos en la máscara, llenando los contornos con color blanco
    cv2.drawContours(mascara, contornos, -1, color_contorno, thickness=cv2.FILLED)

    # Aplicar la máscara a la imagen original para mantener solo las áreas de los contornos
    imagen_filtada = cv2.bitwise_and(imagen_gris, mascara)
    return imagen_filtada


def calcular(imagen_roja,imagen_azul,imagen_verde):



    # Asegúrate de que las imágenes se carguen correctamente
    if imagen_roja is None:
        print("Error al cargar la imagen roja.")
    if imagen_azul is None:
        print("Error al cargar la imagen azul.")
    if imagen_verde is None:
        print("Error al cargar la imagen verde.")


    # Verificar si ambas imágenes se cargaron correctamente
    if imagen_roja is None or imagen_azul is None:
        print("Error al cargar una de las imágenes.")
    else:
        # Convertir las imágenes a escala de grises
        imagen_gris_roja = cv2.cvtColor(imagen_roja, cv2.COLOR_BGR2GRAY)
        imagen_gris_azul = cv2.cvtColor(imagen_azul, cv2.COLOR_BGR2GRAY)
        imagen_gris_verde = cv2.cvtColor(imagen_verde, cv2.COLOR_BGR2GRAY)
        
        # Aplicar un umbral para cada imagen
        _, umbral_roja = cv2.threshold(imagen_gris_roja, 0, 255, cv2.THRESH_BINARY)
        _, umbral_azul = cv2.threshold(imagen_gris_azul, 0, 255, cv2.THRESH_BINARY)
        _, umbral_verde = cv2.threshold(imagen_gris_verde, 0, 255, cv2.THRESH_BINARY)

        # Encontrar los contornos de cada imagen
        contornos_rojos, _ = cv2.findContours(umbral_roja, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contornos_azules, _ = cv2.findContours(umbral_azul, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contornos_verdes, _ = cv2.findContours(umbral_verde, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Dibujar los contornos en las imágenes originales
        imagen_roja_contornos = imagen_roja.copy()
        imagen_azul_contornos = imagen_azul.copy()
        imagen_verde_contornos = imagen_verde.copy()

        cv2.drawContours(imagen_roja_contornos, contornos_rojos, -1, (0, 0, 255), 2)  # Contornos en verde en la imagen roja
        cv2.drawContours(imagen_azul_contornos, contornos_azules, -1, (255, 0, 0), 2)  # Contornos en azul en la imagen azul
        cv2.drawContours(imagen_verde_contornos, contornos_verdes, -1, (0, 255, 0), 2)  # Contornos en azul en la imagen azul
        
        print(f"Calculando Area de Rojo dentro de Verde")
        imagen_contactos_rojo_en_verde,area_rojo_verde,contornos_positivos= Cruzar.cruce(imagen_verde,contornos_verdes,imagen_roja,contornos_rojos,"verde")


        imagen_contactos_rojo_en_verde=dibujar_y_eliminar_restante(imagen_verde_contornos,contornos_positivos,"verde")

        print(f"Calculando Area de Rojo dentro de Verde dentro de Azul",)
        imagen_contactos_rojo_en_verde_en_azul,area_rojo_verde_azul,contornos_positivos= Cruzar.cruce(imagen_azul,contornos_azules,imagen_contactos_rojo_en_verde,contornos_positivos,"azul")


        imagen_contactos_rojo_en_verde_en_azul=dibujar_y_eliminar_restante(imagen_azul_contornos,contornos_positivos,"azul")

        print(f"Calculando Area de Verde dentro de Azul")
        imagen_contactos_verde_en_azul,area_verde_azul,contornos_positivos = Cruzar.cruce(imagen_azul,contornos_azules,imagen_verde,contornos_verdes,"azul")


        imagen_contactos_verde_en_azul=dibujar_y_eliminar_restante(imagen_azul_contornos,contornos_positivos,"azul")

        print(f"Calculando Area de Rojo dentro de Azul")
        imagen_contactos_rojo_en_azul,area_rojo_azul,contornos_positivos = Cruzar.cruce(imagen_azul,contornos_azules,imagen_roja,contornos_rojos,"azul")

        # Mostrar la suma de las áreas
    
        imagen_contactos_rojo_en_azul=dibujar_y_eliminar_restante(imagen_azul_contornos,contornos_positivos,"azul")




        # Convertir las imágenes de BGR a RGB para matplotlib
        imagen_roja_rgb = cv2.cvtColor(imagen_roja_contornos, cv2.COLOR_BGR2RGB)
        imagen_azul_rgb = cv2.cvtColor(imagen_azul_contornos, cv2.COLOR_BGR2RGB)
        imagen_verde_rgb = cv2.cvtColor(imagen_verde_contornos, cv2.COLOR_BGR2RGB)




        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        # Mostrar la imagen con los contornos de contacto
        axs[0].imshow(imagen_roja_rgb)
        axs[0].set_title('Rojo')
        axs[0].axis('off')

        # Mostrar la imagen con los contornos rojos
        axs[1].imshow(imagen_verde_rgb)
        axs[1].set_title('Verde')
        axs[1].axis('off')


        # Mostrar la imagen con los contornos de contacto
        axs[2].imshow(imagen_contactos_rojo_en_verde)
        axs[2].set_title('Contornos Verdes en contacto con Rojos')
        axs[2].axis('off')


        # Mostrar las imágenes
        plt.tight_layout()
        plt.savefig(os.path.join(directorio_actual, 'Resultados', 'Contornos_Verdes_en_contacto_con_Rojos.png'), bbox_inches='tight', dpi=300)  # Cambia el nombre y formato según necesites




        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        # Mostrar la imagen con los contornos de contacto
        axs[0].imshow(imagen_contactos_rojo_en_verde)
        axs[0].set_title('Verde en Rojo')
        axs[0].axis('off')

        # Mostrar la imagen con los contornos rojos
        axs[1].imshow(imagen_azul_rgb)
        axs[1].set_title('Azul')
        axs[1].axis('off')


        # Mostrar la imagen con los contornos de contacto
        axs[2].imshow(imagen_contactos_rojo_en_verde_en_azul)
        axs[2].set_title('Contornos Azules en contacto con los Verdes en Rojo')
        axs[2].axis('off')


        # Mostrar las imágenes
        plt.tight_layout()
        plt.savefig(os.path.join(directorio_actual, 'Resultados', 'Contornos_Azules_en_contacto_con_los_Verdes_en_Rojo.png'), bbox_inches='tight', dpi=300)  # Cambia el nombre y formato según necesites




        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        # Mostrar la imagen con los contornos de contacto
        axs[0].imshow(imagen_verde_rgb)
        axs[0].set_title('Verde')
        axs[0].axis('off')

        # Mostrar la imagen con los contornos rojos
        axs[1].imshow(imagen_azul_rgb)
        axs[1].set_title('Azul')
        axs[1].axis('off')


        # Mostrar la imagen con los contornos de contacto
        axs[2].imshow(imagen_contactos_verde_en_azul)
        axs[2].set_title('Contornos Azules en contacto con Verdes')
        axs[2].axis('off')


        # Mostrar las imágenes
        plt.tight_layout()
        plt.savefig(os.path.join(directorio_actual, 'Resultados', 'Contornos_Azules_en_contacto_con_Verdes.png'), bbox_inches='tight', dpi=300)  # Cambia el nombre y formato según necesites



        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        # Mostrar la imagen con los contornos de contacto
        axs[0].imshow(imagen_roja_rgb)
        axs[0].set_title('Rojo')
        axs[0].axis('off')

        # Mostrar la imagen con los contornos rojos
        axs[1].imshow(imagen_azul_rgb)
        axs[1].set_title('Azul')
        axs[1].axis('off')


        # Mostrar la imagen con los contornos de contacto
        axs[2].imshow(imagen_contactos_rojo_en_azul)
        axs[2].set_title('Contornos Azules en contacto con Rojos')
        axs[2].axis('off')

        # Mostrar las imágenes
        plt.tight_layout()
        # Guardar la figura en un archivo
        plt.savefig(os.path.join(directorio_actual, 'Resultados', 'Contornos_Azules_en_contacto_con_Rojos.png'), bbox_inches='tight', dpi=300)  # Cambia el nombre y formato según necesites


    areas={
        "area_rojo_en_verde":area_rojo_verde,
        "area_rojo_en_verde_en_azul":area_rojo_verde_azul,
        "area_verde_en_azul":area_verde_azul,
        "area_rojo_en_azul":area_rojo_azul
    }

    return areas
    
    
def main():
    try:


        # Construir rutas relativas a partir del directorio actual
        imagen_roja_path = os.path.join(directorio_actual, 'Imagenes_Entrada', 'rojo.tif')
        imagen_azul_path = os.path.join(directorio_actual, 'Imagenes_Entrada', 'azul.tif')
        imagen_verde_path = os.path.join(directorio_actual, 'Imagenes_Entrada', 'verde.tif')

        # Cargar las imágenes usando las rutas relativas
        imagen_roja = cv2.imread(imagen_roja_path)
        imagen_azul = cv2.imread(imagen_azul_path)
        imagen_verde = cv2.imread(imagen_verde_path)

        areas = calcular(imagen_roja,imagen_azul,imagen_verde)

        # Guardar el diccionario en un archivo .txt
        with open(os.path.join(directorio_actual, 'Resultados', 'areas.txt'), 'w') as file:
            json.dump(areas, file, indent=4)  # indent=4 para una mejor legibilidad

        print("Termino todo OK")
    except:
        print("Ocurrio un error que rompio la ejecución.")


# Esto asegura que main() solo se ejecute si el script se ejecuta directamente
if __name__ == "__main__":
    main()