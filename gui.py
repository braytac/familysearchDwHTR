from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Listbox
from tkinter import Frame
from tkinter import BooleanVar
from tkinter import IntVar
from tkinter import StringVar
from tkinter import Text
from tkinter import filedialog
from tkinter import Checkbutton
from subprocess import Popen, PIPE, STDOUT
from tkinter import BOTH, END, LEFT
import tkinter.font as tkFont
import re
import time

class AppGui():

    def browse_button(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        global folder_path
        filename = filedialog.askdirectory()
        self.folder_path.set(filename)

    def init(self, config):

        _user, _passw, _jpgfile, _microfilm, _workdir, _hold_imgs = config


        self.root = Tk()  

        self.folder_path = StringVar()
        self.user = StringVar()
        self.passw = StringVar()
        self.url = StringVar()
        self.jpgfile = StringVar()
        self.hold_imgs = IntVar()

        self.continuar = BooleanVar()

        self.folder_path.set(_workdir)
        self.user.set(_user)
        self.passw.set(_passw)
        self.url.set(_microfilm)
        self.jpgfile.set(_jpgfile)
        self.hold_imgs.set(_hold_imgs)

        #self.root.grid_columnconfigure(0, weight=1)      
        self.root.geometry("800x260")
        self.root.title("Familysearch - Descargar Microfilme y Extraer texto")
        self.root.grid_columnconfigure((1,1), weight=1)

        LabelUser = Label(self.root, text="Usuario Familysearch", padx="10")
        LabelPass = Label(self.root, text="Clave Family Search", padx="10")
        LabelJpg = Label(self.root, text="Archivo por defecto del navegador ", padx="10")
        LabelUrl = Label(self.root, text="URL del Microfim", padx="10")

        EntryUser = Entry(self.root, textvariable=self.user)
        #EntryUser.insert(0, _user)

        EntryPass = Entry(self.root, show="*", textvariable=self.passw)

        EntryJpg = Entry(self.root, textvariable=self.jpgfile)

        EntryUrl = Entry(self.root, textvariable=self.url)
        EntryPath = Entry(self.root, textvariable=self.folder_path)        

        LabelUser.grid(row=3, column=0, pady=(10,0), sticky="e")
        EntryUser.grid(row=3, column=1, sticky="w",padx="10", pady=(10,0))
        LabelPass.grid(row=4, column=0, pady=(10,0), sticky="e")
        EntryPass.grid(row=4, column=1, sticky="w",padx="10", pady=(10,0))

        LabelJpg.grid(row=5, column=0, pady=(10,0), sticky="e")
        EntryJpg.grid(row=5, column=1, sticky="w",padx="10", pady=(10,0))
        
        LabelUrl.grid(row=6, column=0, pady=(10,0), sticky="e")
        EntryUrl.grid(row=6, column=1, sticky="ew",padx="10", pady=(10,0))

        btn_path = Button(text="Directorio destino", command=self.browse_button)
        btn_path.grid(row=7, column=0, pady=(10,0), sticky="e")
        EntryPath.grid(row=7, column=1, sticky="ew",padx="10", pady=(10,0))

        Check_hold_imgs = Checkbutton(self.root, onvalue = 1, offvalue = 0,
                text="Mantener las imágenes del Microfilm descargadas", 
                variable=self.hold_imgs)
        Check_hold_imgs.grid(row=8, columnspan="2", sticky="ew",padx="10", pady=(10,0))

        BtnDown = Button(self.root)
        BtnDown.grid(row=9, column=0, pady=10)

        BtnDown.configure(text='Descargar y extraer (HTR)', command=self.print_content)

        BtnQuit = Button(self.root)
        BtnQuit.grid(row=9, column=1, pady=10)

        BtnQuit.configure(text='Cerrar', command=self.quit)

        self.root.mainloop()

        
    def quit(self):
        self.root.destroy()
        self.continuar = False
        
    def print_content(self):
        if '' not in (self.user.get(), self.passw.get(), self.url.get()):
            self.continuar = True
            self.root.destroy()
        else:
            self.continuar = False

class Mainframe(Frame):
    # Mainframe contains the widgets
    # More advanced programs may have multiple frames
    # or possibly a grid of subframes
    
    def __init__(self,master,*args,**kwargs):
        # *args packs positional arguments into tuple args
        # **kwargs packs keyword arguments into dict kwargs
        
        # initialise base class
        Frame.__init__(self,master,*args,**kwargs)
        # in this case the * an ** operators unpack the parameters
        
        # put your widgets here
        self.stdout_txt = StringVar()
        
        btn_quit = Button(self)
        btn_quit.configure(text='Cancelar y salir', command=self.quit)
        btn_quit.pack()

        Label(self,textvariable = self.stdout_txt).pack()
        self.TimerInterval = 1000

        self.InitVal = ""
        import sys
        import subprocess
        cmd = "ping -c10 google.com" # cambiar por lo que corresponde
        resultado = subprocess.Popen(cmd, 
                                    shell=True, 
                                    stdout=subprocess.PIPE)

        print(resultado.poll())
        while resultado.poll() is None:
            salida = resultado.stdout.readline()
            salida = salida.decode(sys.getdefaultencoding()).rstrip()

        self.print_stdout()
        
    def print_stdout(self):

        self.after(self.TimerInterval, self.print_stdout)
   
class AppLog(Tk):
    
    def __init__(self):

        Tk.__init__(self)
               
        # set the title bar text
        self.title('En progreso...')
        # Make sure app window is big enough to show title 
        self.geometry('700x200')
      
        # create and pack a Mainframe window

        Mainframe(self).pack()
        
        # now start
        self.mainloop()

    def quit(self):
        self.root.destroy()

