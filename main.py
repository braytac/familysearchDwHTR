#!/usr/bin/env python
# coding: utf-8
from funciones import FamilySearch
from funciones import download_finished
from funciones import resta_descargar
import glob
import re
from pathlib import Path
from pathlib import PurePosixPath
from gui import AppGui
from config import Configurations
#python -m pip install -e git+https://github.com/caltechlibrary/handprint.git@master#egg=handprint  --user --upgrade
#pacman -S geckodriver

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



