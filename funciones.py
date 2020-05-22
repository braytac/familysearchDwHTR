from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as options
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.common.keys import Keys
import unittest
import os
import shutil
import time
from pathlib import Path

class FamilySearch(unittest.TestCase):
    def setUp(self):
        
        fp=webdriver.FirefoxProfile()

        fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
        fp.set_preference("browser.download.dir", "/tmp")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")
        firefox_options = Firefox_Options()
        firefox_options.binary = "/usr/bin/firefox-developer-edition"

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

        """
        BBButton="(//a[contains(@href,'blackboard')])"
        coursebutton="(//a[contains(@href,'Course&id=_4572_1&url')])[1]"

        docbutton="(//a[contains(@href,'content_id=_29867_1')])"
        conbutton="(//a[contains(@href,'content_id=_29873_1')])"
        paperbutton="(//a[contains(@href,'/xid-26243_1')])"
        """

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
        """
        BBElement=WebDriverWait(driver,50).until(
            lambda driver:driver.find_element_by_xpath(BBButton)
            )
        BBElement.click()

        WebDriverWait(driver, 50).until(
            lambda driver: len(driver.window_handles) == 2
            )

        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        courseElement=WebDriverWait(driver,50).until(lambda driver:driver.find_element_by_xpath(coursebutton))
        courseElement.click()
    """
        
    def secuencias( self , dir_imgs , archivo , microfilms , lista ):

        driver = self.driver
        driver.get(microfilms)

        max_descargado = max(lista)

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
                download_finished( dir_imgs, numero_pag, archivo )

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


# In[ ]:


def download_finished( dir_imgs , numero_pag, archivo ):
    print('\nDescargando '+str(numero_pag), end ="")

    time_out_dl = 0
    #wait for download complete
    wait = True
    
    while( wait == True ):
        
        tmpfile = Path.joinpath( Path('/tmp') , archivo )
        archivo_pagina = Path.joinpath( Path(dir_imgs) , numero_pag+".jpg" )
        parttmpfile = Path.joinpath( Path('/tmp') , archivo+'.part' )
        
        #for fname in os.listdir('/tmp'):
            #if wait == True:
            #if fname == "record-image_.jpg":
            
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


def existentes( dir_imgs ):
    lista = []
    for f in os.listdir(Path(dir_imgs)):
        try:
            lista.append(int(f[:-4]))
        except:
            pass
    return lista
        
def resta_descargar( lista , nro_pag ):
    resta_descargar = int(nro_pag) not in lista
    return resta_descargar

