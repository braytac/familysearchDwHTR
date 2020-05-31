#!/usr/bin/env python
# coding: utf-8
from funciones import FamilySearch
# from funciones import download_finished
from funciones import resta_descargar
import glob
import re
from pathlib import Path
from pathlib import PurePosixPath
from gui import AppGui
from config import Configurations
# python -m pip install -e git+https://github.com/caltechlibrary/handprint.git@master#egg=handprint  --user --upgrade
# pacman -S geckodriver
# ~/.local/bin/handprint -s google img/{399.jpg,400.jpg} -G -e -o txt/
# grep -ir blabla --include *.txt

handprint = "/home/braytac/.local/bin/handprint"
firefox_bin = "/usr/bin/firefox-developer-edition"

config = Configurations()
app = AppGui()
app.init( config.read() )

microfilms = app.url.get()
user = app.user.get()
passw = app.passw.get()
archivo = app.jpgfile.get()
workdir = app.folder_path.get()
hold_imgs = app.hold_imgs.get()    

config.update(user, passw, archivo, microfilms, workdir, hold_imgs)

# Continuar = True
if app.continuar.as_integer_ratio()[0] == 1:

    obj = FamilySearch()
    obj.setUp(firefox_bin)
    obj.login(user, passw)
    driver = obj.secuencias( 
             workdir, 
             archivo, 
             microfilms,
             hold_imgs)


"""

Si está escrito a máquina: 

convert -density 300 record-image_.jpg -depth 8 -strip -background white -alpha off file.tiff
tesseract file.tiff ocr -l sp

os.system('convert -density 300 "'+nombre_archivo+'" -depth 8 -strip -background white -alpha off file.tiff')
os.system("tesseract " + os.path.join(workdir,"file.tiff")+" ocr -l spa")



Done with ../microfilms/Film # 007625406/img/303.jpg
Done.


Descargando 304.....................................................................................................Traceback (most recent call last):
  File "main.py", line 37, in <module>
    driver = obj.secuencias( 
  File "/home/braytac/Documentos/handprint/familysearch_downs/limpito_github/funciones.py", line 173, in secuencias
    download_finished( ruta_imgs, numero_pag, archivo, nombre_mf )
  File "/home/braytac/Documentos/handprint/familysearch_downs/limpito_github/funciones.py", line 277, in download_finished
    raise ValueError('El archivo temporal no se está descargando.')
ValueError: El archivo temporal no se está descargando.
"""


