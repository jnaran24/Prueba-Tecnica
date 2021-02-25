from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import datetime
import random
import glob
import os, shutil, time

UPLOAD_FOLDER = os.path.abspath("./pendientes/")
ALLOWED_EXTENSIONS = set(["jpg"])

def allowed_file(filename):

    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = "secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return redirect(url_for("upload_file"))

#Ruta para cargar la imagen
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if not "file" in request.files:
            return "No file part in the form."
        f = request.files["file"]
        if f.filename == "":
            return "No file selected."
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            
            #Paso 1: Inicia el metodo de identificar la posición de la imagen
            documento = Image.open("./pendientes/"+ filename)

            ancho_original  = documento.size[0] #Calculamos el ancho de cada documento
            altura_original = documento.size[1] #Calculamos el alto de cada documento
            if altura_original > ancho_original: #Si la altura es mayor que el ancho, la imagen es vertical
                documento_final = Image.open("./images/plantilla1.jpg")
                reductorV(documento_final, documento, ancho_original, altura_original)
            else: #Si el ancho es mayor que la altura, la imagen es horizontal
                documento_final = Image.open("./images/plantilla2.jpg")
                reductorH(documento_final, documento, ancho_original, altura_original)
            #return redirect(url_for("get_file", filename=filename))
        
    return """<!DOCTYPE html>
<html>
<center>
<head>
    <meta charset="utf-8">
    <title>Bienvenid@!\n Por favor adjunta la imagen a procesar</title>
</head>
<body>
    <h1>¡Bienvenid@!</h1><h1>Por favor adjunta la imagen a procesar</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
</body>
</center>
</html>"""

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


if __name__ == "__main__":
    app.run(debug=False)