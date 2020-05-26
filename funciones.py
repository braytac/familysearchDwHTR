from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as options
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.common.keys import Keys
from gui import AppGui, AppLog
import subprocess
import unittest
import os
import sys
import re
import shutil
import time
from pathlib import Path

class FamilySearch(unittest.TestCase):

    #def __init__(self):
        #import main
        #from main import hold_imgs
        #print(hold_imgs)

    def setUp(self, firefox_bin):
        
        fp=webdriver.FirefoxProfile()

        fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
        fp.set_preference("browser.download.dir", "/tmp")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")
        firefox_options = Firefox_Options()
        firefox_options.binary = firefox_bin

        self.driver=webdriver.Firefox(firefox_profile=fp,
                                      options=firefox_options
                                      )
        
    def login(self, usuario, clave):
        
        driver = self.driver        
        driver.maximize_window()
        
        url="https://www.familysearch.org/auth/familysearch/login?fhf=true&returnUrl=%2F"
        
        driver.get(url)
       
        userName="userName"
        password="password"
        login="login"

        loginFieldElement=WebDriverWait(driver,10).until(
            lambda driver:driver.find_element_by_id(login)
            )

        passwordFieldElement=WebDriverWait(driver,10).until(
            lambda driver:driver.find_element_by_id(password)
            )
        userNameButtonElement=WebDriverWait(driver,10).until(
            lambda driver:driver.find_element_by_id(userName)
            )

        userNameButtonElement.clear()
        userNameButtonElement.send_keys(usuario)
        passwordFieldElement.clear()    
        passwordFieldElement.send_keys(clave)
        loginFieldElement.click()

        
    def secuencias( self, workdir, archivo, microfilms, hold_imgs ):

        driver = self.driver
        driver.get(microfilms)

        try:
            time.sleep(3)
            nro_pagFieldElement=WebDriverWait(driver,10).until(
                lambda driver:driver.find_element_by_name("currentTileNumber")
                )

            WebDriverWait(driver,10).until(
                lambda driver:driver.find_element_by_class_name("afterInput")
                )

            WebDriverWait(driver,10).until(
                lambda driver:driver.
                    find_element_by_class_name("afterInput").
                    get_attribute("innerHTML").
                    replace("of ", "").
                    isnumeric()
                )

            css_nombre_mf = "div.film-viewer-header div.film-number"
            nombre_mf=WebDriverWait(driver,10).until(
                        lambda driver:driver.find_element_by_css_selector(css_nombre_mf)
                        )
            nombre_mf = nombre_mf.get_attribute("innerHTML")
            nombre_mf = re.split('<', nombre_mf)[0].strip()
            
            ruta_imgs  = Path.joinpath( Path( workdir ), nombre_mf , 'img' )
            ruta_txts  = Path.joinpath( Path( workdir ), nombre_mf , 'txt' )

            ruta_txts.mkdir(parents=True,exist_ok=True)
            ruta_imgs.mkdir(parents=True,exist_ok=True)

            # archivos ya descargados
            lista = existentes( ruta_imgs ) 

            # max pag descargada
            if not lista:
                max_descargado = 0
            else:
                max_descargado = max(lista)

            maxP = driver.find_element_by_class_name("afterInput").get_attribute("innerHTML")
            maxP = maxP.replace("of ", "")

            WebDriverWait(driver,10).until(
                lambda driver:driver.
                    find_element_by_name("currentTileNumber").
                    get_attribute("value").
                isnumeric()
                )
            numero_pag = nro_pagFieldElement.get_attribute("value")

            WebDriverWait(driver,10).until(
                lambda driver:driver.find_element_by_css_selector(
                    "#ImageViewer div div.openseadragon-canvas canvas"
                    )
                )

            #nro_pagFieldElement.set_attribute("value",max_descargado)
            
            nro_pagFieldElement = driver.find_element_by_name("currentTileNumber")
            nro_pagFieldElement.clear()
            nro_pagFieldElement.send_keys(max_descargado)
            nro_pagFieldElement.send_keys(Keys.RETURN)

        except:
            print("Ocurrió algún error en la conexión")
            raise

        #self.log_win = AppGui()

        while( int(numero_pag) <= int(maxP) ):
            saveFieldElement=WebDriverWait(driver,10).until(
                lambda driver:driver.find_element_by_css_selector("#saveLi > a.actionToolbarSaveButton")
                )

            nextBtnFieldElement=WebDriverWait(driver,10).until(
                lambda driver:driver.find_element_by_class_name("next")
                )
            #img = Path.joinpath( Path( dir_imgs ) , numero_pag + ".jpg" )
            #img = Path( os.path.join( dir_imgs , numero_pag+".jpg") )

            if resta_descargar( lista , numero_pag): # and not img.exists():

                #flrm = Path("/tmp/record-image_.jpg")
                #flrm = Path.joinpath( Path('/tmp') , 'record-image*' )
                
                # BORRAR record-image*
                for f in Path("/tmp").glob("record-image*.*"):  #archivo[:-5]+".jpg"):
                    f.unlink()
                
                #if flrm.exists():
                #    flrm.unlink()        
                time.sleep(4)            
                saveFieldElement.click()

                # Esperar que termine descarga y mover a workdir/img
                print('\nDescargando '+str(numero_pag), end ="")
                download_finished( ruta_imgs, numero_pag, archivo, nombre_mf )

                # Extraer texto 
                app_log=0
                self.handprintear(app_log, numero_pag, ruta_imgs, ruta_txts, hold_imgs)

            nextBtnFieldElement.click()
            time.sleep(3)
            WebDriverWait(driver,10).until(
                lambda driver:driver.find_element_by_css_selector(
                    "#ImageViewer div div.openseadragon-canvas canvas"
                    )
                )

            WebDriverWait(driver,10).until(
                lambda driver:driver.find_element_by_name("currentTileNumber")
            )

            WebDriverWait(driver,10).until(
                lambda driver:driver.
                    find_element_by_name("currentTileNumber").
                    get_attribute("value").
                isnumeric()
                )
            numero_pag = driver.find_element_by_name("currentTileNumber").get_attribute("value")
        print("Finalizado")

        return driver


    def handprintear(self, AppLog, pagina, ruta_imgs, ruta_txts, hold_imgs):

        handprint = "/home/braytac/.local/bin/handprint"

        pagina = str(pagina)
        
        ruta_txt = Path.joinpath(ruta_txts, pagina + '.handprint-google.txt')        

        ruta_jpg_p = Path.joinpath(ruta_imgs, pagina + '.jpg')
        ruta_png_hp = Path.joinpath(ruta_txt, pagina + '.handprint.png')


        ruta_jpg = str( ruta_jpg_p )
        ruta_txts = str(ruta_txts)

        if ruta_txt.exists(): 
            print("\nReconocimiento de pág. "+pagina+" ya realizado")
        else:    
            print('\nHandprinteando página '+pagina+'...' )

            try:
                cmd = handprint+' -s google "'+ruta_jpg+'" -C -G -e -o "'+ruta_txts+'"'                
                res = subprocess.Popen(
                                cmd,
                                shell=True, 
                                stdout=subprocess.PIPE)


                while res.poll() is None:
                    s = res.stdout.readline()
                    s = s.decode(sys.getdefaultencoding()).rstrip()
                    print(s)

            except:
                print("\n\nOcurrió algún problema con handprint\n\n")
                raise
            
        if ruta_png_hp.exists():
            os.remove( ruta_png_hp )

        # Si se ha destildado conservar las imágenes:   
        if hold_imgs == 0:
            os.remove( ruta_jpg_p )


def download_finished( ruta_imgs , numero_pag, archivo, nombre_mf ):
    
    # nombre_mf: nombre del directori del microfilm/rollo
    time_out_dl = 0
    #wait for download complete
    wait = True
    
    while( wait == True ):
        
        tmpfile = Path.joinpath( Path('/tmp') , archivo )
        archivo_pagina = Path.joinpath( ruta_imgs , numero_pag+".jpg" )
        parttmpfile = Path.joinpath( Path('/tmp') , archivo+'.part' )
        
           
        if tmpfile.is_file() and not parttmpfile.is_file():
            time.sleep(1)
            wait = False
            #try:
            shutil.move( tmpfile , archivo_pagina )
            time.sleep(1)
            #except:
            #    print("Problema con "+ numero_pag)
            #    pass
        else:
            print(".", end ="")
            time.sleep(0.1)
            time_out_dl+=1
            
        if time_out_dl > 100:
            raise ValueError('El archivo temporal no se está descargando.')


# In[ ]:


def existentes( ruta ):
    lista = []
    for f in os.listdir(ruta):
        try:
            lista.append(int(f[:-4]))
        except:
            pass
    return lista
        
def resta_descargar( lista , nro_pag ):
    resta_descargar = int(nro_pag) not in lista
    return resta_descargar

