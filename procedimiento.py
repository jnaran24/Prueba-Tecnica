from PIL import Image
import datetime
import random
import glob
import os, shutil
import cv2
import unittest

#Paso 1: Inicia el metodo de identificar la posición de la imagen
def identificadorPosicion():  
    path = glob.glob("./pendientes/*.jpg")
    for file in path: # bucle para recorrer la carpeta y leer miles de documentos
        documento = Image.open(file)
        ancho_original  = documento.size[0] #Calculamos el ancho de cada documento
        altura_original = documento.size[1] #Calculamos el alto de cada documento
        if altura_original > ancho_original: #Si la altura es mayor que el ancho, la imagen es vertical
            documento_final = Image.open("./templates/plantilla1.jpg")
            reductorV(documento_final, documento, ancho_original, altura_original)
        else: #Si el ancho es mayor que la altura, la imagen es horizontal
            documento_final = Image.open("./templates/plantilla2.jpg")
            reductorH(documento_final, documento, ancho_original, altura_original)

#Paso 2:#Paso 2: Si la imagen es horizontal y es mayor a la hoja A4 se reduce sin perder calidad
def reductorH (documento_final, documento, ancho_original, altura_original):
    ancho_ideal = 1123
    altura_ideal = 796

    if ancho_original > ancho_ideal or altura_original > altura_ideal:
        porcentaje_ancho = (ancho_ideal/float(documento.size[0]))
        tamaño_altura = int((float(documento.size[1])*float(porcentaje_ancho)))
        documento = documento.resize((ancho_ideal, tamaño_altura), Image.ANTIALIAS)
        mergeDocument(documento, documento_final)
    else:
        mergeDocument(documento, documento_final)

#Paso 3: Si la imagen es vertical y es mayor a la hoja A4 se reduce sin perder calidad
def reductorV (documento_final, documento, ancho_original, altura_original):
    ancho_ideal = 796
    altura_ideal = 1123

    if ancho_original > ancho_ideal or altura_original > altura_ideal:
        porcentaje_ancho = (ancho_ideal/float(documento.size[0]))
        tamaño_altura = int((float(documento.size[1])*float(porcentaje_ancho)))
        documento = documento.resize((ancho_ideal, tamaño_altura), Image.ANTIALIAS)
        mergeDocument(documento, documento_final)
    else:
        mergeDocument(documento, documento_final)    

#Paso 4: Se unen el documento requerido con la plantilla hoja A4
def mergeDocument (documento, documento_final):

    area = (0,0) #Identificamos la esquina superior izquierda
    documento_final.paste(documento, area)
    numero_aleatorio = str(random.randint(1, 1000))
    date_string = datetime.datetime.now().strftime("E"+"%Y%m%d%H%M%S"+numero_aleatorio)
    documento_final.save("./procesados/" + date_string + ".jpg")

#Paso 5: Se guarda el documento final en hoja A4 con un radicado unico 
def saveFinalDocument (documento_final):
    #Guardar el documento final con un radicado unico    
    numero_aleatorio = str(random.randint(1, 1000))
    date_string = datetime.datetime.now().strftime("E"+"%Y%m%d%H%M%S"+numero_aleatorio)
    documento_final.save("./procesados/" + date_string + '.jpg')

    
#Paso 6: Se eliminan todas las imagenes procesadas para evitar sobrecarga en maquina/servidor
def removeOldDocuments():
    pendientes = "./pendientes"
    for filename in os.listdir(pendientes):
        file_path = os.path.join(pendientes, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Fallo en eliminar documentos: %s. Razon: %s' % (file_path, e))


#Invocamos el primer metodo
identificadorPosicion()

# Cuando termine el procesamiento, se eliminan los archivos de la carpeta
removeOldDocuments() 

