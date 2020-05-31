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

    def __init__(self):
        self.microfilms = None
        self.driver = None

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
        self.microfilms = microfilms

        driver.get(microfilms)
        time.sleep(3)

        try:

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
            lista_jpgs = existentes( ruta_imgs ) 
            lista_txts = existentes( ruta_txts )
            
            lista_jpgs.sort()
            lista_txts.sort()
            
            lista_restantes_HTR = list( set(lista_jpgs) - set(lista_txts))

            # max pag descargada
            #if not lista_jpgs:
            if not lista_restantes_HTR:
                max_descargado = 1
            else:
                max_descargado = max(lista_txts)
                #max_descargado = max(lista_restantes_HTR) #max(lista_jpgs)

            print("Máx descargado: "+str(max_descargado))
            maxP = self.numero_maximo_imagenes()
            
            #numero_pag = self.numero_pagina_actual()

            self.ir_a_pagina( str(max_descargado+1) )
            time.sleep(3)
            #driver.refresh()
            numero_pag = self.numero_pagina_actual()

            WebDriverWait(driver,10).until(
                lambda driver:driver.find_element_by_css_selector(
                    "#ImageViewer div div.openseadragon-canvas canvas"
                    )
                )            

        except:
            print("Ocurrió algún error en la conexión")
            raise

        #self.log_win = AppGui()

        #self.ir_a_pagina( str(max_descargado) )

        while( numero_pag <= maxP ):

            time.sleep(1)
            # Si el jpg aún no existe en FS
            if resta_descargar( lista_jpgs , numero_pag): # and not img.exists():

                #flrm = Path("/tmp/record-image_.jpg")
                #flrm = Path.joinpath( Path('/tmp') , 'record-image*' )
                
                # BORRAR record-image*
                for f in Path("/tmp").glob("record-image*.*"):  #archivo[:-5]+".jpg"):
                    f.unlink()
                
                #if flrm.exists():
                #    flrm.unlink()        

                WebDriverWait(driver,10).until(
                    lambda driver:driver.find_element_by_css_selector(
                        "#ImageViewer div div.openseadragon-canvas canvas"
                        )
                    )  

                saveFieldElement=WebDriverWait(driver,10).until(
                    lambda driver:driver.find_element_by_css_selector("#saveLi > a.actionToolbarSaveButton")
                    )

                saveFieldElement.click()

                # Esperar que termine descarga y mover a workdir/img
                print('\nDescargando '+str(numero_pag), end ="")
                df_ok = self.download_finished( ruta_imgs, numero_pag, archivo, nombre_mf )

                app_log = 0

                if df_ok:
                    # Extraer texto 
                    #self.handprintear(app_log, numero_pag, ruta_imgs, ruta_txts, hold_imgs)
                    self.tesseract(app_log, numero_pag, ruta_imgs, ruta_txts, hold_imgs)                

                    time.sleep(3)
                    #numero_pag = self.numero_pagina_actual()
                    numero_pag+= 1
                #else:
                    # Falló  la descarga, timeout etc...
            else:
                # Si ya existe (nº).jpg paso al siguiente
                numero_pag+= 1
                
            self.ir_a_pagina(numero_pag)

        print("Finalizado")

        return driver

    def numero_maximo_imagenes(self):

        driver = self.driver        
        # Número máximo de imágenes.
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


        maxP = driver.find_element_by_class_name("afterInput").get_attribute("innerHTML")
        return int (maxP.replace("of ", "").strip() )

    def numero_pagina_actual(self):
        driver = self.driver
        nro_pagFieldElement=WebDriverWait(driver,10).until(
            lambda driver:driver.find_element_by_name("currentTileNumber")
            )
        WebDriverWait(driver,10).until(
            lambda driver:driver.
                find_element_by_name("currentTileNumber").
                get_attribute("value").
            isnumeric()
            )
        return int( nro_pagFieldElement.get_attribute("value").strip() )


    def ir_a_pagina(self, pagina):
    
        driver = self.driver
        
        WebDriverWait(driver,10).until(
            lambda driver:driver.
                find_element_by_name("currentTileNumber").
                get_attribute("value").
            isnumeric()
            )

        nro_pagFieldElement=WebDriverWait(driver,10).until(
            lambda driver:driver.find_element_by_name("currentTileNumber")
            )

        #nro_pagFieldElement = driver.find_element_by_name("currentTileNumber")
        nro_pagFieldElement.clear()
        nro_pagFieldElement.send_keys( str(pagina) )
        print("Yendo a pág.: "+ str(pagina) )
        nro_pagFieldElement.send_keys(Keys.RETURN)

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
                #-C -G 
                cmd = handprint+' -s google "'+ruta_jpg+'" -G -e -o "'+ruta_txts+'"'                
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

    def tesseract(self, AppLog, pagina, ruta_imgs, ruta_txts, hold_imgs):

        pagina = str(pagina)
        
        ruta_txt = Path.joinpath(ruta_txts, pagina + '.txt')        

        ruta_jpg_p = Path.joinpath(ruta_imgs, pagina + '.jpg')

        ruta_jpg = str( ruta_jpg_p )
        ruta_txts = str(ruta_txts)

        if ruta_txt.exists(): 
            print("\nReconocimiento de pág. "+pagina+" ya realizado")
        else:    
            print('\nOCR página '+pagina+'...' )

            try:
                cmd = 'tesseract "'+ruta_jpg+'" "'+ruta_txts+'/'+pagina+'" -l spa'
                res = subprocess.Popen(
                                cmd,
                                shell=True, 
                                stdout=subprocess.PIPE)


                while res.poll() is None:
                    s = res.stdout.readline()
                    s = s.decode(sys.getdefaultencoding()).rstrip()
                    print(s)

            except:
                print("\n\nOcurrió algún problema con OCR\n\n")
                raise
            
        # Si se ha destildado conservar las imágenes:   
        if hold_imgs == 0:
            try:
                os.remove( ruta_jpg_p )
            except:
                pass
            
        print("Tesseract terminado")



    def download_finished( self, ruta_imgs, numero_pag, archivo, nombre_mf ):
        
        numero_pag = str(numero_pag)
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
                print('El archivo temporal no se está descargando, o tarda demasiado.')
                wait = False

                numero_pag = str( int(numero_pag))
                time.sleep(4)
                driver = self.driver
                driver.get(self.microfilms)
                time.sleep(3)
                self.ir_a_pagina(numero_pag)
                time.sleep(2)
                #driver.refresh()
                time.sleep(4)
                retorno = False
                #self.numero_pagina_actual()
                pass
            else:
                retorno = True

        return retorno

def existentes( ruta ):
    lista = []
    for f in os.listdir(ruta):
        #lista.append(int(f[:-4]))
        if f.endswith(".jpg") or f.endswith(".txt"):
            lista.append(int(f.split('.', 1)[0]))        
            #lista.append(f.split('.', 1)[0])

    return lista
        
def resta_descargar( lista , nro_pag ):
    resta_descargar = int(nro_pag) not in lista
    return resta_descargar

