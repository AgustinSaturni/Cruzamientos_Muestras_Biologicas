# Cruzamiento de Marcadores Intracelulares en muestras Biológicas

Editor Markdown es un editor online que se ejecuta en tu navegador y que funciona tanto con tus archivos locales como con varios servicios de almacenamiento cloud.

## Función

La función del script es analizar imágenes de fluorescencia de una muestra biológica registrada en un microscopio confocal con tres canales que representan distintos marcadores intracelulares. Se busca encontrar co-localizaciones entre distintos pares de marcadores y entre los tres a la vez para cuantificar cuánto de uno de los marcadores se encuentra libre y cuánto se encuentra asociado a uno de los marcadores o a los otros dos marcadores en simultáneo.
Este trabajo se hizo en el marco de un aporte a un compañero que esta cursando su doctorado en Biología Molecular y que resultó de ayuda en el análisis de muestras para aportar información a un paper científico posteriormente publicado en la revista 

## Pasos para probarlo

1-Instalar anaconda (https://www.anaconda.com/download)
2-Crear una carpeta nueva en un destino accesible por el usuario.
2-Crear un entorno conda con python 3.9  (conda create --prefix "ruta_carpeta_nueva" python=3.9)
3-Activar el entorno. (conda activate "ruta_carpeta_nueva")
4-Instalar las librerias requeridas:
*   OpenCv: conda install -c conda-forge opencv
*   MatplotLib: conda install matplotlib

5-Clonar dentro de la carpeta nueva este repositorio.

6-Correr el programa python posicionados dentro de la carpeta clonada.(python Application.py)

obs: Las imágenes de prueba se toman de la carpeta Imagenes_Entrada y los resultados (imagenes cruzadas + .txt con áreas medidas) en la carpeta Resultados.

