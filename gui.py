from tkinter import *

class AppGui():
    
    def __init__(self):
          
        self.root = Tk()        
        
        self.user = StringVar()
        self.passw = StringVar()
        self.url = StringVar()
        self.continuar = BooleanVar()
        
        self.root.geometry("800x150")
        self.root.title("Familysearch - Descargar Microfilme y Extraer texto")
        self.root.grid_columnconfigure((0,1), weight=1)
        Label3 = Label(self.root, text="Usuario Family Search", padx="10")
        Label4 = Label(self.root, text="Clave Family Search", padx="10")
        Label5 = Label(self.root, text="URL del Microfim", padx="10")

        Entry3 = Entry(self.root, textvariable=self.user)
        Entry4 = Entry(self.root, textvariable=self.passw)
        Entry5 = Entry(self.root, textvariable=self.url)
        Entry5.insert(0, "https://www.familysearch.org/ark:/61903/3:1:3QSQ-G92H-L4DZ?i=2&cat=25735")

        Label3.grid(row=3, column=0, pady=(10,0))
        Entry3.grid(row=3, column=1, sticky="ew",padx="10", pady=(10,0))
        Label4.grid(row=4, column=0, pady=(10,0))
        Entry4.grid(row=4, column=1, sticky="ew",padx="10", pady=(10,0))
        Label5.grid(row=5, column=0, pady=(10,0))
        Entry5.grid(row=5, column=1, sticky="ew",padx="10", pady=(10,0))

        BtnDown = Button(self.root)
        BtnDown.grid(row=6, column=0, pady=10)
        #BtnDown.configure(pady="0")
        BtnDown.configure(text='Descargar y extraer (HTR)', command=self.print_content)

        BtnQuit = Button(self.root)
        BtnQuit.grid(row=6, column=1, pady=10)
        #BtnQuit.configure(pady="0")
        BtnQuit.configure(text='Cerrar', command=self.quit)
        
        #button = Tkinter.Button(self.root, text = 'Cerrar', command=self.quit)

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