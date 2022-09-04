import tkinter
import webbrowser
import customtkinter as Ctk
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import ttk
from tkinter import simpledialog
from typing import List

import numpy as np
import pandas as pd
import math
import optimizadores as op
import plot as pl
import matplotlib.pyplot as plt
import matplotlib



from sympy import *
from PIL import  ImageTk
from PIL import  Image




Anto = 0
matplotlib.use('TkAgg')

root = Ctk.CTk()
root.title("Ajuste parametros")
root.iconbitmap("icono.ico")
root.geometry('1200x800')

bgcolor= "grey"
bgcolor2 = "#a1c7be"
colortexto = "#172c66"

frame = Ctk.CTkFrame(root, fg_color="#fef6e4")
frame.place(relwidth=1, relheight=1)

UNI = Ctk.CTkFrame(frame,fg_color = "#8bd3dd", border_width=2, border_color="black")
UNI.place(relx=0.65,rely=0.4, relheight=0.4,relwidth=0.33)


'''
bgimage = Image.open("fondo.jpg").resize([600,600])

Fondo= ImageTk.PhotoImage(bgimage)
back= Label(frame, image=Fondo)
back.image=Fondo
back.place(x=0,y=0)
'''

menubar = Menu(root)
root.config(menu=menubar)

def ayuda():

    Help = ImageTk.PhotoImage(Image.open("Ayuda.png"))
    Antoi= ImageTk.PhotoImage(Image.open("antoine.png"))
    def abrirlink(url):
        webbrowser.open_new(url)

    im = Toplevel()
    im.title("Información")
    notebook = ttk.Notebook(im)
    notebook.pack(pady= 10, expand = True)

    frame1= Frame(notebook, width=400, height=280, bg="white")
    frame2= Frame(notebook, width= 400, height=600,bg="white")
    frame3 =Frame(notebook, width=400, height=600, bg="white")

    Nara = Canvas(frame1, width=730, height=400, bg= "orange")

    frame1.pack(fill='both', expand=True)
    frame2.pack(fill='both', expand=True)
    frame3.pack(fill='both', expand=True)

    notebook.add(frame1, text='Acerca de...')
    notebook.add(frame2, text='Formato de datos')
    notebook.add(frame3, text='Coeficientes de Antoine')

    hel = Label(frame2, image=Help)
    img_antoine= Label(frame3, image=Antoi)
    img_antoine.image= Antoi
    hel.image =Help
    Titulo = Label(frame1, text= "Descripción", font= ("Times", 20,"bold"), bg="white")
    t2 = Label(Nara, text="Instrucciones", font=("Helvetica",13,"bold"), bg="orange")

    Instrucciones = Label(Nara, text="1. Dar click en el botón Abrir archivo y seleccionar el archivo que contiene toda la información como se especifíca en la ventana de formato de datos. Tambien tener en cuenta las unidades de los coeficientes de Antoine.\n\n"
                                     "2. Verificar que la información sea la correcta.\n\n"
                                     "3. Presionar el boton siguiente, aparecerá una ventana que pedira información correspondiente "
                                     "al optimizador y la función objetivo.\n\n"
                                     "4. Despúes de presionar el boton de resolver , se mostrará en el cajón de texto los parametros que se resolvieron así como el tiempo que le tomo a cada optimizador y la función objetivo que se utilizó\n\n"
                                     "5. Para visualizar los resultados se tiene que presionar el boton  de gráfica T-x,y o x-y.\n\n"
                                     "6. Por último los resultados obtenidos por la ultima optimización realizada se pueden descargar en un archivo excel con el botón de imprimir resultados.\n",
                          font=("Helvetica", 11, "bold"),
                          wraplength=650, justify=LEFT, bg="orange")
    Info = Label(frame1, text= "El programa de Ajuste de Datos para los modelos de Wilson, NRTL y UNIQUAC es una herramienta \n"
                               "que como su nombre lo indica obtiene los parametros de wilson correspondien-\n"
                               "tes a un sistema binario liquido vapor, por medio de optimizadores metaheur-\n"
                               "-isticos ( PSO, DE, JAYA). Para obtener los mejores resultados posibles por \n"
                               "favor sigue las instrucciones en las demas ventanas.", font =("Helvetica",14,"italic"), justify=LEFT, foreground="blue", bg="white")

    info_Ant = Label(frame3, text="Actualemte el programa  funciona solamente con el siguiente tipo de ecuación de Antoine  y las unidades de temperatura en los datos termodinámicos tienen que estar en Celcius.", font=("Times", 20, "bold"), wraplength=700, bg="white")
    Info.place(relx=0.05 , rely=0.2 )
    Link1 = Label(frame3 , text = "Si necesita convertir las unidades de los coeficientes lo puede realizar en la siguiente página ", font=("Arial", 12), bg="white")
    Link2 = Label(frame3,
                 text="https://www.envmodels.com/freetools.php?menu=antoine&lang=en ",
                 font=("Arial", 12), fg  = "blue", cursor="hand2", bg="white")
    Link2.bind("<Button-1>", lambda e:abrirlink("https://www.envmodels.com/freetools.php?menu=antoine&lang=en"))
    #https://www.envmodels.com/freetools.php?menu=antoine&lang=en
    Titulo.place(rely=0.1, relx=0.4)
    info_Ant.place(relx=0.1, rely=0.1)

    img_antoine.place(relx= 0.3, rely= 0.25)
    Link1.place(relx=0.1, rely=0.5)
    Link2.place(relx=0.1, rely=0.55)
    Nara.place(relx=0.05, rely= 0.45)

    t2.pack()
    Instrucciones.pack()
    Nara.create_window(100,50,window=t2)
    Nara.create_window(370, 235,window=Instrucciones)

    hel.pack()



Help_menu = Menu(menubar, tearoff= False)
Coeficientes_antoine= Menu(menubar, tearoff= false)

Help_menu.add_command( label='Instrucciones', command= ayuda)
menubar.add_cascade(label="Ayuda", menu=Help_menu, underline=0)




#----------------------------VARIABLES GLOBALES-----------------------------------------------------------------------------------
n = 10
opt1 = BooleanVar()
opt2 = BooleanVar()
opt3 = BooleanVar()

Tiposistema = IntVar()
Fobjetivo = IntVar()
param_r = np.array([0,0])
param_q = np.array([0,0])
param_qprima = np.array([0,0])
t = np.zeros(n)
x1 = np.zeros(n)
y1 = np.zeros(n)
P = 0.1
V1= 0.1
V2 = 0.1
direc = ""
Coef= np.zeros(3)
Coef2 = np.zeros(3)
Texto=1
Tabla= 1
de_var =[0,1]
UNI_var = []
Error_UNI =0
pso_var = [0,1]
jaya_var= [0,1]
Nrtl_var= [0,1]
de_e =0
pso_e = 0
jaya_e= 0
Mostrar=0
Config =0
NRTL_e = 0


#----------------------------------------------------------------------------------------------------------------------


#----------------------------FUNCIONES -----------------------------------------------------------------------------------
def obtener_path():
    global x1
    global t
    global y1
    global Coef
    global Coef2
    global P
    global direc
    global V1
    global V2
    global Mostrar
    global Config
    global param_r
    global param_q
    global param_qprima

    try:
        Config.withdraw()
    except:
        print("")

    Coef1A.delete(0, END)
    Coef1B.delete(0, END)
    Coef1C.delete(0, END)
    Coef2A.delete(0, END)
    Coef2B.delete(0, END)
    Coef2C.delete(0, END)
    Vmol1.delete(0, END)
    Vmol2.delete(0, END)
    Presion.delete(0, END)
    Path.delete(0,END)


    direc = filedialog.askopenfilename(title='Select file', filetypes=(('excel files','*.xlsx'),('all files', '*.*')))
    Path.insert(0,direc)
    data = pd.read_excel(direc, sheet_name=0)
    data2= pd.read_excel(direc, sheet_name=1)

    try:
        data3= pd.read_excel(direc,sheet_name=2)
        duni= pd.DataFrame(data3).to_numpy()

        param_r= np.array([duni[0][0], duni[1][0]])
        param_q = np.array([duni[0][1], duni[1][1]])
        param_qprima = np.array([duni[0][2], duni[1][2]])

        rs1_entry.insert(0,param_r[0])
        rs2_entry.insert(0, param_r[1])
        qs1_entry.insert(0,param_q[0])
        qs2_entry.insert(0, param_q[1])

        try:
            qprima_entry.insert(0, param_qprima[0])
            qprima_entry2.insert(0, param_qprima[1])
        except Exception as e:
            messagebox.showinfo("VARIABLES UNIQUAC", "No hay parametros q prima\n" + str(e))

    except Exception as e:
        messagebox.showinfo("VARIABLES UNIQUAC", "No hay parametros UNIQUAC en el archivo seleccionado \n" + str(e))


    Mostrar = Toplevel()
    mo= Label(Mostrar, text=data).pack()

    Pe = pd.DataFrame(data)
    datos = Pe.to_numpy()

    Q= pd.DataFrame(data2)
    datos2 = Q.to_numpy()
    m= len(datos2)

    n = len(datos)

    t = np.zeros(n)
    y1 = np.zeros(n)
    x1 = np.zeros(n)



    for i in range(n):
        t[i] = datos[i][0]
        x1[i] = datos[i][1]
        y1[i] = datos[i][2]


    for i in range(3):
        Coef[i] = datos2[0][i]
        Coef2[i]= datos2[1][i]

    V1 = datos2[0][3]
    V2 = datos2[1][3]
    P = datos2[0][4]

    Coef1A.insert(0, Coef[0])
    Coef1B.insert(0, Coef[1])
    Coef1C.insert(0, Coef[2])
    Coef2A.insert(0, Coef2[0])
    Coef2B.insert(0, Coef2[1])
    Coef2C.insert(0, Coef2[2])
    Vmol1.insert(0,V1)
    Vmol2.insert(0,V2)
    Presion.insert(0,P)
    Coef[2] = Coef[2] + 273.15
    Coef2[2] = Coef2[2] + 273.15

def next():
    global Texto
    global Parametros
    global x1
    global t
    global y1
    global Coef
    global Coef2
    global P
    global direc
    global V1
    global V2
    global Fobjetivo
    global Mostrar
    global Config
    global Tabla

    try:
        Mostrar.withdraw()
    except:
        print("")
# Presion.get()=="" or Coef1A.get()=="" or Coef2A.get()==""or Coef1B.get()==""or Coef2B.get()==""or Coef2C.get()==""or Coef1C.get()==""
    if Presion.get()=="1" :
        messagebox.showerror("Errro", "Faltan datos")
    else:
        Config = Ctk.CTkToplevel(height=800, width=1300, fg_color=bgcolor2)
        Config.title("Optimización")

        frame1 = Frame(Config, bg=bgcolor2)
        frame1.place(relheight=1, relwidth=1)
        bgcolor3 = "white"
        frame_wilson = Ctk.CTkFrame(Config, fg_color= bgcolor3, border_width=2, border_color="blue")
        frame_NRTL = Ctk.CTkFrame(Config, fg_color=bgcolor3, border_width=2, border_color="blue")
        frame_UNIQUAC = Ctk.CTkFrame(Config, fg_color=bgcolor3, border_width=2, border_color="blue")


        frame_wilson.place(relheight=0.45, relwidth=0.25, relx= 0.0625, rely=0.1)
        frame_NRTL.place(relheight=0.45, relwidth=0.25, relx=0.375, rely=0.1)
        frame_UNIQUAC.place(relheight=0.45, relwidth=0.25, relx=0.6875, rely=0.1)

        Wilson_titulo = Ctk.CTkLabel(Config, text="WILSON",text_font=("Arial","16","bold"), text_color="black")
        NRTL_titulo = Ctk.CTkLabel(Config, text="NRTL", text_font=("Arial", "16", "bold"), text_color="black")
        UNIQUAC_titulo = Ctk.CTkLabel(Config, text="UNIQUAC", text_font=("Arial", "16", "bold"), text_color="black")

        Wilson_titulo.place(relx=0.0625, rely=0.05)
        NRTL_titulo.place(relx=0.375, rely=0.05)
        UNIQUAC_titulo.place(relx=0.6875, rely=0.05)


        Lim_W = Ctk.CTkLabel(frame_wilson, text="Límites para el primer parametro", text_color="black", text_font=("Helvetica", "8"))
        Lim2_W = Label(frame_wilson, text="Límites para el segundo parametro", bg=bgcolor3, font=("Helvetica", "8"))
        ite_W = Label(frame_wilson, text="Numero de iteraciones", bg=bgcolor3, font=("Helvetica", "8"))
        po_W = Label(frame_wilson, text="Tamaño de poblacion", bg=bgcolor3, font=("Helvetica", "8"))

        Lim_N = Label(frame_NRTL, text="Límites para el primer parametro", bg=bgcolor3, font=("Helvetica", "8"))
        Lim2_N = Label(frame_NRTL, text="Límites para el segundo parametro", bg=bgcolor3,
                         font=("Helvetica", "8"))
        ite_N = Label(frame_NRTL, text="Numero de iteraciones", bg=bgcolor3, font=("Helvetica", "8"))
        po_N = Label(frame_NRTL, text="Tamaño de poblacion", bg=bgcolor3, font=("Helvetica", "8"))

        Lim_U = Label(frame_UNIQUAC, text="Límites para el primer parametro", bg=bgcolor3, font=("Helvetica", "8"))
        Lim2_U = Label(frame_UNIQUAC, text="Límites para el segundo parametro", bg=bgcolor3,
                         font=("Helvetica", "8", ))
        ite_U = Label(frame_UNIQUAC, text="Numero de iteraciones", bg=bgcolor3, font=("Helvetica", "8"))
        po_U = Label(frame_UNIQUAC, text="Tamaño de poblacion", bg=bgcolor3, font=("Helvetica", "8"))

        Texto = Text(Config)
        # VENTANA WILSON
        Liminf1_w =Entry(frame_wilson)
        Liminf1_w.insert(0,"-1000")
        Liminf2_w= Entry(frame_wilson)
        Liminf2_w.insert(0, "-1000")
        Limsup1_w= Entry(frame_wilson)
        Limsup1_w.insert(0, "2000")
        Limsup2_w = Entry(frame_wilson)
        Limsup2_w.insert(0, "2000")
        Pop_w = Entry(frame_wilson)
        itera_w= Entry(frame_wilson)
        Pop_w.insert(0,"20")
        itera_w.insert(0,"100")

        # VENTANA NRTL
        Liminf1_n = Entry(frame_NRTL)
        Liminf1_n.insert(0, "-1000")
        Liminf2_n = Entry(frame_NRTL)
        Liminf2_n.insert(0, "-1000")
        Limsup1_n = Entry(frame_NRTL)
        Limsup1_n.insert(0, "2000")
        Limsup2_n = Entry(frame_NRTL)
        Limsup2_n.insert(0, "2000")
        Pop_n = Entry(frame_NRTL)
        itera_n = Entry(frame_NRTL)
        Pop_n.insert(0, "20")
        itera_n.insert(0, "30")

        # VENTANA UNIQUAC
        Liminf1_u = Entry(frame_UNIQUAC)
        Liminf1_u.insert(0, "-1000")
        Liminf2_u = Entry(frame_UNIQUAC)
        Liminf2_u.insert(0, "-1000")
        Limsup1_u = Entry(frame_UNIQUAC)
        Limsup1_u.insert(0, "2000")
        Limsup2_u = Entry(frame_UNIQUAC)
        Limsup2_u.insert(0, "2000")
        Pop_u = Entry(frame_UNIQUAC)
        itera_u = Entry(frame_UNIQUAC)
        Pop_u.insert(0, "20")
        itera_u.insert(0, "30")


        Objetivo1 = Radiobutton(frame_wilson, bg=bgcolor3, text="Min γ1 y γ2", variable=Fobjetivo, value= 0)
        Objetivo2 = Radiobutton(frame_wilson, bg=bgcolor3, text="Min y", variable=Fobjetivo, value=1)
        Objetivo3 = Radiobutton(frame_wilson, bg=bgcolor3, text="Min GE/RT", variable=Fobjetivo, value=2)

        Imprimir = Ctk.CTkButton(Config, text= "Imprimir resultados", command= impri)
        Comparacion = Ctk.CTkButton(Config, text ="Comparar métodos", command= grafica2)

        Resol_U = Ctk.CTkButton(frame_UNIQUAC, text= "Resolver",
                               command= lambda: ResUNIQUAC(np.array([float(Liminf1_u.get()),float(Liminf2_u.get())]),
                                                           np.array([float(Limsup1_u.get()),float(Limsup2_u.get())]), 2,
                                                           int(Pop_u.get()),int(itera_u.get())), width=60, fg_color=bgcolor2, text_color="black")
        Resol_N = Ctk.CTkButton(frame_NRTL, text="Resolver",
                               command=lambda: ResNRTL(np.array([float(Liminf1_n.get()), float(Liminf2_n.get())]),
                                                          np.array([float(Limsup1_n.get()), float(Limsup2_n.get())]), 2,
                                                          int(Pop_n.get()), int(itera_n.get())), width=60, fg_color=bgcolor2, text_color="black")

        Resol_W = Ctk.CTkButton(frame_wilson,text= "Resolver",
                                command= lambda: Resolver(np.array([float(Liminf1_w.get()),float(Liminf2_w.get())]),
                                                          np.array([float(Limsup1_w.get()),float(Limsup2_w.get())]), 2,
                                                          int(Pop_w.get()),int(itera_w.get())),width=60, fg_color=bgcolor2, text_color="black")


        Graficar_W = Ctk.CTkButton(frame_wilson, text="Graficar x1,y1 -T", command= grafica , width=30, fg_color=bgcolor2, text_color="black")
        Graficar_N = Ctk.CTkButton(frame_NRTL, text="Graficar x1,y1 -T", command=GraficarNRTL, width=30, fg_color=bgcolor2, text_color="black")
        Graficar_U = Ctk.CTkButton(frame_UNIQUAC, text="Graficar x1,y1 -T", command=GraficarUNI, width=30, fg_color=bgcolor2, text_color="black")

        Graf_W= Ctk.CTkButton(frame_wilson, text="Gráficar x1-y1", command= grafxy, width=30, fg_color=bgcolor2, text_color="black")
        Graf_N = Ctk.CTkButton(frame_NRTL, text="Gráficar x1-y1", command=grafxy, width=30, fg_color=bgcolor2, text_color="black")
        Graf_U = Ctk.CTkButton(frame_UNIQUAC, text="Gráficar x1-y1", command=grafxy, width=30, fg_color=bgcolor2, text_color="black")

        columnas = ('parametro1', 'parametro2', 'parametro3', 'Er', 'T', 'Opt','Met')

        Tabla = ttk.Treeview(Config, columns= columnas, show= 'headings')
        Tabla.heading('parametro1', text='Primer parametro (cal/mol)')
        Tabla.heading('parametro2', text='Segundo parametro (cal/mol)')
        Tabla.heading('parametro3', text='Tercer parametro NRTL (a)')
        Tabla.heading('Er', text='Error')
        Tabla.heading('T', text='Tiempo')
        Tabla.heading('Opt', text='Optimizador')
        Tabla.heading('Met', text='Metodo')
        Tabla.column('T', width=100)
        Tabla.column('Opt', width=100)
        Tabla.column('Met', width=200)

        #Tabla.insert('',END,values= ('1','1','1','1','1','1'))
        Tabla.place(relx=0.05, rely=0.6)




        #WILSON
        Lim_W.place(relx=0.05, rely=0.05)
        Liminf1_w.place(relx=0.05, rely=0.13, relwidth=0.15)
        Limsup1_w.place(relx=0.25, rely=0.13, relwidth=0.15)

        Lim2_W.place(relx=0.05, rely=0.2)
        Limsup2_w.place(relx=0.25, rely=0.27, relwidth=0.15)
        Liminf2_w.place(relx=0.05, rely=0.27, relwidth=0.15)

        ite_W.place(relx=0.05, rely=0.35)
        itera_w.place(relx=0.05, rely=0.43, relwidth=0.15)

        po_W.place(relx=0.05, rely=0.5)
        Pop_w.place(relx=0.05, rely=0.57, relwidth=0.15)

        # NRTL
        Lim_N.place(relx=0.05, rely=0.05)
        Liminf1_n.place(relx=0.05, rely=0.13, relwidth=0.15)
        Limsup1_n.place(relx=0.25, rely=0.13, relwidth=0.15)

        Lim2_N.place(relx=0.05, rely=0.2)
        Limsup2_n.place(relx=0.25, rely=0.27, relwidth=0.15)
        Liminf2_n.place(relx=0.05, rely=0.27, relwidth=0.15)

        ite_N.place(relx=0.05, rely=0.35)
        itera_n.place(relx=0.05, rely=0.43, relwidth=0.15)

        po_N.place(relx=0.05, rely=0.5)
        Pop_n.place(relx=0.05, rely=0.57, relwidth=0.15)

        # UNIQUAC
        Lim_U.place(relx=0.05, rely=0.05)
        Liminf1_u.place(relx=0.05, rely=0.13, relwidth=0.15)
        Limsup1_u.place(relx=0.25, rely=0.13, relwidth=0.15)

        Lim2_U.place(relx=0.05, rely=0.2)
        Limsup2_u.place(relx=0.25, rely=0.27, relwidth=0.15)
        Liminf2_u.place(relx=0.05, rely=0.27, relwidth=0.15)

        ite_U.place(relx=0.05, rely=0.35)
        itera_u.place(relx=0.05, rely=0.43, relwidth=0.15)

        po_U.place(relx=0.05, rely=0.5)
        Pop_u.place(relx=0.05, rely=0.57, relwidth=0.15)


        #Texto.place(relx=0.5, rely=0.15, relwidth=0.47, relheight=0.7)
        Imprimir.place(relx= 0.7, rely= 0.9, relwidth= 0.20)

        Resol_W.place(relx=0.3, rely=0.65, relwidth=0.4)
        Resol_U.place(relx=0.3, rely=0.65, relwidth=0.4)
        Resol_N.place(relx=0.3, rely=0.65, relwidth=0.4)

        Graficar_W.place(relx=0.15, rely=0.8)
        Graf_W.place(relx=0.6, rely=0.8)
        Graficar_N.place(relx=0.15, rely=0.8)
        Graf_N.place(relx=0.6, rely=0.8)
        Graficar_U.place(relx=0.15, rely=0.8)
        Graf_U.place(relx=0.6, rely=0.8)
        Comparacion.place(relx = 0.5, rely = 0.9)

        #Objetivo1.place(relx=0.05, rely=0.75)
        #Objetivo2.place(relx=0.35,rely= 0.75)
        #Objetivo3.place(relx=0.55, rely=0.75)


        '''
        '''

tiempo_UNI = 0
tiempo_n = 0
tiempo_1 = 0

def agregar(cr, ll):
    if cr== 0:
        lb= np.insert(ll, 0, 0.2)
        return lb
    else:
        lu = np.insert(ll,0,0.5)
        return lu


def ResUNIQUAC(lb, ub, dim, Popsize,iters):
    global UNI_var, Error_UNI, tiempo_UNI
    Error_UNI, mejor_ruta_UNI, UNI_var, tiempo_UNI = op.de(lb, ub, dim, Popsize, iters, UNIQUAC)
    Tabla.insert('', END,values= (f'{UNI_var[0]:.4f}', f'{UNI_var[1]:.4f}','',f'{Error_UNI:.8f}',f'{tiempo_UNI:.4f}', 'DE', 'UNIQUAC' ))

def GraficarUNI():
    plt.close('all')
    plt.plot(x1, t, 'g-', y1, t, 'b-', pl.BublxUNIQUAC(x1, P, UNI_var, Coef, Coef2, param_r, param_q, param_qprima)[0],
             pl.BublxUNIQUAC(x1, P, UNI_var, Coef, Coef2, param_r, param_q, param_qprima)[2], 'r^'
             , pl.BublxUNIQUAC(x1, P, UNI_var, Coef, Coef2, param_r, param_q, param_qprima)[1],
             pl.BublxUNIQUAC(x1, P, UNI_var, Coef, Coef2, param_r, param_q, param_qprima)[2], 'r^')
    plt.axis([0, 1, t.min() - 5, t.max() + 5])
    plt.title('UNIQUAC')
    plt.ylabel('T (C)')
    plt.xlabel('x1, y1')
    plt.legend(["x1exp-t", "y1exp-t", "x1calc-t", "y1calc-t"])
    plt.text(0.02, t.max() + 3, "E=" + f'{Error_UNI:.8f}', bbox=dict(facecolor='red', alpha=0.5))
    plt.grid(True)
    plt.show()

def GraficarNRTL():
    plt.close('all')
    plt.plot(x1, t, 'g-', y1, t, 'b-', pl.BublxPNRTL(x1, P, Nrtl_var, Coef, Coef2, V1, V2)[0],
             pl.BublxPNRTL(x1, P, Nrtl_var, Coef, Coef2, V1, V2)[2], 'r^'
             , pl.BublxPNRTL(x1, P, Nrtl_var, Coef, Coef2, V1, V2)[1],
             pl.BublxPNRTL(x1, P, Nrtl_var, Coef, Coef2, V1, V2)[2], 'r^')
    plt.title('NRTL')
    plt.ylabel('T (C)')
    plt.xlabel('x1, y1')
    plt.legend(["x1exp-t", "y1exp-t", "x1calc-t", "y1calc-t"])
    plt.axis([0, 1, t.min() - 5, t.max() + 5])
    plt.text(0.02, t.max() + 3, "E=" + f'{NRTL_e:.8f}', bbox=dict(facecolor='red', alpha=0.5))
    plt.grid(True)
    plt.show()


def ResNRTL(lb, ub, dim, Popsize,iters):
    global Nrtl_var, NRTL_e, tiempo_n
    NRTL_e, mejor_ruta_n, Nrtl_var, tiempo_n = op.de(agregar(0,lb), agregar(1,ub), 3, Popsize, iters, fNRTL)

    Tabla.insert('', END,values= (f'{Nrtl_var[1]:.4f}', f'{Nrtl_var[2]:.4f}',f'{Nrtl_var[0]:.4f}',f'{NRTL_e:.8f}',f'{tiempo_n:.4f}', 'DE', 'NRTL' ))


def Resolver(lb, ub, dim, Popsize,iters):
    global Texto, de_var, pso_var, jaya_var, de_e, pso_e, jaya_e, Fobjetivo, tiempo_1
    obj= Fobjetivo.get()
    '''
    funcion = ""
    if obj == 0:
        fobj = fobj1
        funcion = "Minimización de coeficientes de actividad"
    elif obj == 1:
        fobj= fobj2
        funcion = "Minimización de fracción de vapor"
    else:
        fobj = f
        funcion = "Minimización de Ge/RT"
    '''

    de_e, mejor_ruta_1, de_var, tiempo_1 = op.de(lb, ub, dim, Popsize, iters, f)
    Tabla.insert('', END, values=(f'{de_var[0]:.4f}', f'{de_var[1]:.4f}', '', f'{de_e:.8f}', f'{tiempo_1:.4f}', 'DE', 'WILSON'))
    #mejor_eval_2, mejor_ruta_2, gBest_2, tiempo_2 = op.pso(lb, ub, dim, Popsize, iters, fobj)
    #mejor_eval_3, mejor_ruta_3, gBest_3, tiempo_3 = op.jaya(lb, ub, dim, Popsize, iters, fobj)

    #mejor_eval_n, mejor_ruta_n, gBest_NRTL, tiempo_n = op.de(agregar(0,lb), agregar(1,ub), 3, Popsize, iters, fNRTL)



    #print(mejor_eval_1, mejor_eval_2, mejor_eval_3)
    '''
    Texto.insert(END, str(gBest_1)+"de  "+f'{tiempo_1:.4f}'+ "s\n" + str(gBest_2)+"pso  "+f'{tiempo_2:.4f}'+ "s\n"+ f'{str(gBest_3)}' +"jaya  "+f'{tiempo_3:.4f}'+"s\n \n"+ str(gBest_NRTL) +"NRTL  "
                 +f'{tiempo_n:.4f}'+"s\n"+funcion+"\n")
    
                      f"{str(gBest_2)} de {tiempo_2:.4f}s \n"\
                      f"{str(gBest_3)} de {tiempo_3:.4f}s \n"\
                      f"{str(gBest_NRTL)} de {tiempo_n:.4f}s \n"\
                      f" {funcion:.4f}s \n"
                      '''

    #Texto.insert(END,)
    #pso_var = gBest_2
    #jaya_var = gBest_3
    #Nrtl_var = gBest_NRTL

    #pso_e = mejor_eval_2
    #jaya_e = mejor_eval_3
    #NRTL_e = mejor_eval_n



    #grafica(pl.BublxPaltern(x1, P, gBest, Coef, Coef2, V1, V2)[0], pl.BublxPaltern(x1, P, gBest, Coef, Coef2, V1, V2)[1],
            #pl.BublxPaltern(x1, P, gBest, Coef, Coef2, V1, V2)[2])




def impri():
    Dat_Wilson = pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)
    Dat_NRTL = pl.BublxPNRTL(x1, P, Nrtl_var, Coef, Coef2, V1, V2)
    DAT_UNIQUAC= pl.BublxUNIQUAC(x1, P, UNI_var, Coef, Coef2, param_r, param_q, param_qprima)

    res_Wilson = pd.DataFrame({'T':Dat_Wilson[2],
                           'x1':Dat_Wilson[0],
                            'y1':Dat_Wilson[1],
                            'γ1':Dat_Wilson[3],
                            'γ2':Dat_Wilson[4],
                            'Ge/RT':Dat_Wilson[5] })
    res_NRTL = pd.DataFrame({'T': Dat_NRTL[2],
                               'x1': Dat_NRTL[0],
                               'y1': Dat_NRTL[1],
                               'γ1': Dat_NRTL[3],
                               'γ2': Dat_NRTL[4],
                               'Ge/RT': Dat_NRTL[5]
                             })
    res_UNIQUAC = pd.DataFrame({'T': DAT_UNIQUAC[2],
                                'x1': DAT_UNIQUAC[0],
                                'y1': DAT_UNIQUAC[1],
                                'γ1': DAT_UNIQUAC[3],
                                'γ2': DAT_UNIQUAC[4],
                                'Ge/RT': DAT_UNIQUAC[5]
                                })
    param = pd.DataFrame({'Wilson':['Parametros: '+f'{de_var[0]:.4f} cal/mol : ' + f'{de_var[1]:.4f} cal/mol',
                                                          'Error: '+f'{de_e:.4f}',
                                                          'Tiempo: '+f'{tiempo_1:.4f} s',
                                                          'Nombre del algoritmo: diferential evolution'],
                          'NRTL ':['Parametros: ' + f'{Nrtl_var[0]:.4f} : ' + f'{Nrtl_var[1]:.4f} cal/mol :'+ f'{Nrtl_var[2]:.4f} cal/mol',
                                                           'Error: ' + f'{NRTL_e:.4f}',
                                                           'Tiempo: ' + f'{tiempo_n:.4f} s',
                                                           'Nombre del algoritmo: diferential evolution'],
                          'UNIQUAC ':['Parametros: ' + f'{UNI_var[0]:.4f} cal/mol : ' + f'{UNI_var[1]:.4f} cal/mol ',
                                    'Error: ' + f'{Error_UNI:.4f}',
                                    'Tiempo: ' + f'{tiempo_UNI:.4f} s',
                                    'Nombre del algoritmo: diferential evolution']})
    Nombre = simpledialog.askstring("Nombre", "Introducir el nombre del archivo")
    folder = filedialog.askdirectory()

    folder = folder + "/"+Nombre+".xlsx"
    with pd.ExcelWriter(folder) as writer:
        res_Wilson.to_excel(writer, sheet_name="Wilson")
        res_NRTL.to_excel(writer, sheet_name="NRTL")
        res_UNIQUAC.to_excel(writer, sheet_name="UNIQUAC")
        param.to_excel(writer, sheet_name="Parametros encontrados")

    #messagebox.showerror("Error", "No se ha resuelto el sistema")



def grafica2():

    #liq = pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)[0]
    #vap = pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)[1]
    #temp = pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)[2]

    plt.close('all')

    FIG= plt.figure(figsize=(15,5), constrained_layout=True)
    try:
        plt.subplot(131)
        plt.plot(x1 , t,'g-', y1, t,'b-', pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)[0], pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)[2],'r^'
                 , pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)[1],pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)[2], 'r^')
        plt.axis([0, 1, t.min()-5, t.max()+5])
        plt.title('WILSON')
        plt.ylabel('T (C)')
        plt.xlabel('x1, y1')
        plt.legend(["x1exp-t","y1exp-t", "x1calc-t", "y1calc-t" ])
        plt.text(0.02, t.max()+3,"E="+ f'{de_e:.8f}',bbox=dict(facecolor='red', alpha=0.5))
        plt.grid(True)
    except Exception as e:
        messagebox.showinfo("Graficar", "No se ha resuelto para WILSON \n")
    try:
        plt.subplot(132)
        plt.plot(x1, t, 'g-', y1, t, 'b-', pl.BublxPNRTL(x1, P, Nrtl_var, Coef, Coef2, V1, V2)[0],
                 pl.BublxPNRTL(x1, P, Nrtl_var, Coef, Coef2, V1, V2)[2], 'r^'
                 , pl.BublxPNRTL(x1, P, Nrtl_var, Coef, Coef2, V1, V2)[1],
                 pl.BublxPNRTL(x1, P, Nrtl_var, Coef, Coef2, V1, V2)[2], 'r^')
        plt.title('NRTL')
        plt.ylabel('T (C)')
        plt.xlabel('x1, y1')
        plt.legend(["x1exp-t", "y1exp-t", "x1calc-t", "y1calc-t"])
        plt.axis([0, 1, t.min() - 5, t.max() + 5])
        plt.text(0.02, t.max()+3, "E=" + f'{NRTL_e:.8f}', bbox=dict(facecolor='red', alpha=0.5))
        plt.grid(True)
    except Exception as e:
        messagebox.showinfo("Graficar", "No se ha resuelto para NRTL \n")

    try:
        plt.subplot(133)

        plt.plot(x1, t, 'g-', y1, t, 'b-', pl.BublxUNIQUAC(x1, P, UNI_var, Coef, Coef2, param_r, param_q, param_qprima)[0],
                 pl.BublxUNIQUAC(x1, P, UNI_var, Coef, Coef2, param_r, param_q, param_qprima)[2], 'r^'
                 , pl.BublxUNIQUAC(x1, P, UNI_var, Coef, Coef2, param_r, param_q, param_qprima)[1],
                 pl.BublxUNIQUAC(x1, P, UNI_var, Coef, Coef2, param_r, param_q, param_qprima)[2], 'r^')
        plt.axis([0, 1, t.min() - 5, t.max() + 5])
        plt.title('UNIQUAC')
        plt.ylabel('T (C)')
        plt.xlabel('x1, y1')
        plt.legend(["x1exp-t", "y1exp-t", "x1calc-t", "y1calc-t"])
        plt.text(0.02, t.max() + 3, "E=" + f'{Error_UNI:.8f}', bbox=dict(facecolor='red', alpha=0.5))
        plt.grid(True)
    except Exception as e:
        messagebox.showinfo("Graficar", "No se ha resuelto para UNIQUAC \n")
    #plt.savefig("T-x1,y1.png")
    plt.show()
    return


def grafica():
    #global x1, t, y1, Coef, Coef2, P, direc, V1, V2

    plt.close('all')

    #FIG= plt.figure(figsize=(12,7), constrained_layout=True)
    plt.plot(x1 , t,'g-', y1, t,'b-', pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)[0], pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)[2],'r^'
             , pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)[1],pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)[2], 'r^')
    plt.axis([0, 1, t.min()-5, t.max()+5])
    plt.title('WILSON')
    plt.ylabel('T (C)')
    plt.xlabel('x1, y1')
    plt.legend(["x1exp-t","y1exp-t", "x1calc-t", "y1calc-t" ])
    plt.text(0.02, t.max()+3,"E="+ f'{de_e:.8f}',bbox=dict(facecolor='red', alpha=0.5))
    plt.grid(True)

    '''
    plt.subplot(132)
    plt.plot(x1, t, 'g-', y1, t, 'b-', pl.BublxPaltern(x1, P, pso_var, Coef, Coef2, V1, V2)[0],
             pl.BublxPaltern(x1, P, pso_var, Coef, Coef2, V1, V2)[2], 'ro'
             , pl.BublxPaltern(x1, P, pso_var, Coef, Coef2, V1, V2)[1],
             pl.BublxPaltern(x1, P, pso_var, Coef, Coef2, V1, V2)[2], 'ro')
    plt.title('PSO')
    plt.ylabel('T (C)')
    plt.xlabel('x1, y1')
    plt.legend(["x1exp-t", "y1exp-t", "x1calc-t", "y1calc-t"])
    plt.axis([0, 1, t.min() - 5, t.max() + 5])
    plt.text(0.02, t.max()+3, "E=" + f'{pso_e:.8f}', bbox=dict(facecolor='red', alpha=0.5))
    plt.grid(True)

    plt.subplot(133)
    plt.plot(x1, t, 'g-', y1, t, 'b-', pl.BublxPaltern(x1, P, jaya_var, Coef, Coef2, V1, V2)[0],
             pl.BublxPaltern(x1, P, jaya_var, Coef, Coef2, V1, V2)[2], 'ro'
             , pl.BublxPaltern(x1, P, jaya_var, Coef, Coef2, V1, V2)[1],
             pl.BublxPaltern(x1, P, jaya_var, Coef, Coef2, V1, V2)[2], 'ro')
    plt.title('JAYA')
    plt.ylabel('T (C)')
    plt.xlabel('x1, y1')
    plt.legend(["x1exp-t", "y1exp-t", "x1calc-t", "y1calc-t"])
    plt.axis([0, 1, t.min() - 5, t.max() + 5])
    plt.text(0.02, t.max()+3, "E=" + f'{jaya_e:.8f}', bbox=dict(facecolor='red', alpha=0.5))
    plt.grid(True)
    '''
    #plt.savefig("T-x1,y1.png")
    plt.show()
    return

def grafxy():



    plt.close('all')
    FIG = plt.figure(figsize=(12, 5), constrained_layout=True)
    '''
    fig, axs = plt.subplots(ncols=1,nrows=3, figsize=(5.5, 3.5), constrained_layout=True)
    axs[1,1].annotate(f'axs[{1},{1}]',(0.5,0.5), transform=axs[1,1].transAxes,ha='center',va='center', color='darkgrey')
    '''
    plt.subplot(131)
    plt.plot([0,1],[0,1],'r--', x1 , y1, pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)[0] ,
             pl.BublxPaltern(x1, P, de_var, Coef, Coef2, V1, V2)[1], 'ro')
    plt.title('DE')
    plt.axis([0, 1, 0, 1])
    plt.ylabel('y1')
    plt.xlabel('x1')
    plt.legend(["","Exp", "Calculado" ])
    plt.grid(True)

    plt.subplot(132)
    plt.plot([0, 1], [0, 1], 'r--', x1, y1, pl.BublxPaltern(x1, P, pso_var, Coef, Coef2, V1, V2)[0],
             pl.BublxPaltern(x1, P, pso_var, Coef, Coef2, V1, V2)[1], 'ro')
    plt.title('PSO')
    plt.axis([0, 1, 0, 1])
    plt.ylabel('y1')
    plt.xlabel('x1')
    plt.legend(["", "Exp", "Calculado"])
    plt.grid(True)

    plt.subplot(133)
    plt.plot([0, 1], [0, 1], 'r--', x1, y1, pl.BublxPaltern(x1, P, jaya_var, Coef, Coef2, V1, V2)[0],
             pl.BublxPaltern(x1, P, jaya_var, Coef, Coef2, V1, V2)[1], 'ro')
    plt.title('JAYA')
    plt.axis([0, 1, 0, 1])
    plt.ylabel('y1')
    plt.xlabel('x1')
    plt.legend(["", "Exp", "Calculado"])
    plt.grid(True)

    plt.show()
    return




def fobj1(param):

    # ---------------Calculo de parametros de la ecuacion de wilson   -------------------------------------------------


    l1 = param[0]
    l2 = param[1]
    a12 = (V2 / V1) * math.exp(-l1 / (1.987 * 298.15))
    a21 = (V1 / V2) * math.exp(-l2 / (1.987 * 298.15))
    # ------------------------------------------------------------------------------------------------------------------

    # --------------- Getting experimental data through the function "exp" in file plot   ------------------------------
    x, gama1exp, gama2exp, gibbsexp = pl.experimental(t, x1, y1, Coef, Coef2, P)
    n = len(gibbsexp)
    x2 = pl.c2(x)

    #print(x, gama1exp, gama2exp, gibbsexp)
    # ------------------------------------------------------------------------------------------------------------------

    suma = 0

    for i in range(0, n):
        # Funcion objetivo (gamaexp1 -gamacalc1)^2 + (gamaexp2 -gamacalc2)^2
        r = (gama1exp[i] - math.exp(-math.log(x[i]+a12*x2[i]) + x2[i]*(a12/(x[i]+a12*x2[i]) - a21/(x2[i]+a21*x[i]))))**2 +\
            (gama2exp[i] - math.exp(-math.log(x2[i]+a21*x[i]) + x[i]*(-a12/(x[i]+a12*x2[i]) + a21/(x2[i]+a21*x[i]))))**2

        suma += r

    return suma


# ----------------------------------------------------------------------------------------------------------------------
def fobj2(param):
    # ---------------DATOS NECESARIOS QUE SE INTRODUZCAN POR EL USUARIO O CON ALGUNA BASE DE DATOS  --------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ---------------Calculo de paramestros de la ecuacion de wilson   -------------------------------------------------
    l1 = param[0]
    l2 = param[1]
    a12 = (V2 / V1) * math.exp(-l1 / (1.987 * 298.15))
    a21 = (V1 / V2) * math.exp(-l2 / (1.987 * 298.15))
    # ------------------------------------------------------------------------------------------------------------------

    # --------------- Getting experimental data through the function "exp" in file plot   ------------------------------
    x, gama1exp, gama2exp, gibbsexp = pl.experimental(t, x1, y1, Coef, Coef2, P)
    n = len(gibbsexp)
    x2 = pl.c2(x)
    # ------------------------------------------------------------------------------------------------------------------

    t1= pl.cortar(t)
    y_1 = pl.cortar(y1)

    psat1= pl.psatalternativa(Coef, t1)


    suma = 0

    for i in range(0, n):

        gama1 = math.exp(-math.log(x[i]+a12*x2[i])+x2[i]*(a12/(x[i]+a12*x2[i]) - a21/(x2[i]+a21*x[i])))

        r = (y_1[i] - gama1*x[i]*psat1[i]/P)**2

        suma += r

    return suma

# ----------------------------------------------------------------------------------------------------------------------


def f(param):

    l1 = param[0]
    l2 = param[1]

    x, gama1exp, gama2exp, gibbsexp = pl.experimental(t, x1, y1, Coef, Coef2, P)

    #x = np.array([0.1008, 0.1989, 0.301, 0.4012, 0.4993, 0.5998, 0.6989, 0.8001, 0.8976])
    #y = np.array([0.120355947163574, 0.36281859108538, 0.613547124059236, -0.061070855531744, -0.0496705413090824, 0.888657442475681, 0.669078589972542, 0.457330457630938, 0.243741235318766])



    n = len(x)

    if n != len(gibbsexp):
        print("el numero de datos en x y y es diferente ")

    suma = 0

    a12 = (V2 / V1) * math.exp(-l1 / (1.987 * 298.15))
    a21 = (V1 / V2) * math.exp(-l2 / (1.987 * 298.15))


    for i in range(0, n):
        # Funcion objetivo (Ge/RTexp - Ge/RTcalc)^2
        r = (gibbsexp[i] - (- x[i] * math.log(x[i] + (1 - x[i]) * a12) - (1-x[i]) * math.log(1 - x[i] + x[i] * a21)))**2

        suma += r

    return suma

def UNIQUAC(param):
    global direc
    global param_qprima
    global param_q
    global param_r


    u12 = param[0]
    u21 = param[1]

    x, gama1exp, gama2exp, gibbsexp = pl.experimental(t, x1, y1, Coef, Coef2, P)

    Ge_combinatoria= pl.valoresUNIQUAC( param_r , param_q, param_qprima, x)[0]
    thetaprimas = pl.valoresUNIQUAC( param_r , param_q, param_qprima, x)[1]

    #x = np.array([0.1008, 0.1989, 0.301, 0.4012, 0.4993, 0.5998, 0.6989, 0.8001, 0.8976])
    #y = np.array([0.120355947163574, 0.36281859108538, 0.613547124059236, -0.061070855531744, -0.0496705413090824, 0.888657442475681, 0.669078589972542, 0.457330457630938, 0.243741235318766])



    n = len(x)

    if n != len(gibbsexp):
        print("el numero de datos en x y y es diferente ")

    suma = 0
    x2 = pl.c2(x)
    t12 = exp(-u12 / (1.987 * 298.15))
    t21 = exp(-u21 / (1.987 * 298.15))


    for i in range(0, n):
        # Funcion objetivo (Ge/RTexp - Ge/RTcalc)^2
        r = (gibbsexp[i] - (Ge_combinatoria[i]+(-x[i]*param_qprima[0]*math.log(thetaprimas[0][i] + thetaprimas[1][i]*t21) - x2[i] * param_qprima[1]*math.log(thetaprimas[1][i] + thetaprimas[0][i]*t12))))**2

        suma += r

    return suma


#----------------------------------------------------------------------------------------------------------------------
def fNRTL(param):

    a = param[0]
    b12 = param[1]
    b21 = param[2]


    x, gama1exp, gama2exp, gibbsexp = pl.experimental(t, x1, y1, Coef, Coef2, P)

    #x = np.array([0.1008, 0.1989, 0.301, 0.4012, 0.4993, 0.5998, 0.6989, 0.8001, 0.8976])
    #y = np.array([0.120355947163574, 0.36281859108538, 0.613547124059236, -0.061070855531744, -0.0496705413090824, 0.888657442475681, 0.669078589972542, 0.457330457630938, 0.243741235318766])

    x2 = pl.c2(x)

    n = len(x)

    if n != len(gibbsexp):
        print("el numero de datos en x y y es diferente ")

    suma = 0

    #a12 = (V2 / V1) * math.exp(-l1 / (1.987 * 298.15))
    #a21 = (V1 / V2) * math.exp(-l2 / (1.987 * 298.15))

    t12 = b12 / (1.987 * 298.15)
    t21 = b21 / (1.987 * 298.15)
    G12 = exp(- a * t12)
    G21 = exp(- a * t21)



    for i in range(0, n):
        # Funcion objetivo (Ge/RTexp - Ge/RTcalc)^2
        r = (gibbsexp[i] - (x[i]*x2[i]*(t21*G21/(x[i]+G21*x2[i]) + t12*G12/(x2[i]+G12*x[i]))))**2

        suma += r

    return suma


#----------------------------Labels -----------------------------------------------------------------------------------
Tit = Ctk.CTkLabel(frame ,text ="Ajuste de Datos modelos termodinámicos", text_font=("Times", "20", "bold italic"), text_color= "#001858")

coefa1 = Ctk.CTkLabel(frame ,text ="Coeficientes de Antoine para el primer componente", text_font=("Helvetica", "10", "bold"),text_color = colortexto)
coefa2 = Ctk.CTkLabel(frame ,text ="Coeficientes de Antoine para el segundo componente", text_font=("Helvetica", "10", "bold"),text_color = colortexto)
A = Ctk.CTkLabel(frame, text= "A", text_font=("Helvetica", "10", "bold"),text_color = colortexto)
B = Ctk.CTkLabel(frame, text= "B", text_font=("Helvetica", "10", "bold"),text_color = colortexto)
C = Ctk.CTkLabel(frame, text= "C", text_font=("Helvetica", "10", "bold"),text_color = colortexto)
A1 = Ctk.CTkLabel(frame, text= "A", text_font=("Helvetica", "10", "bold"),text_color = colortexto)
B1 = Ctk.CTkLabel(frame, text= "B", text_font=("Helvetica", "10", "bold"),text_color = colortexto)
C1 = Ctk.CTkLabel(frame, text= "C", text_font=("Helvetica", "10", "bold"),text_color = colortexto)


Vm1 = Ctk.CTkLabel(frame ,text ="Vm1", text_font=("Helvetica", "10", "bold"),text_color = colortexto)
Vm2 = Ctk.CTkLabel(frame ,text ="Vm2", text_font=("Helvetica", "10", "bold"),text_color = colortexto)
cm = Ctk.CTkLabel(frame ,text ="cc/mol", text_font=("Helvetica", "10", "bold"),text_color = colortexto)
cm1 = Ctk.CTkLabel(frame ,text ="cc/mol", text_font=("Helvetica", "10", "bold"),text_color = colortexto)

Pres = Ctk.CTkLabel(frame ,text ="Presión del sistema",  text_font=("Helvetica", "10", "bold"),text_color = colortexto)
Kpa = Ctk.CTkLabel(frame ,text ="Kpa",  text_font=("Helvetica", "10", "bold"),text_color = colortexto)

K = Ctk.CTkLabel(frame ,text ="Unidades",  text_font=("Helvetica", "10", "bold"),text_color = colortexto)


Titulo_UNIQUAC = Ctk.CTkLabel(UNI, text="Variables UNIQUAC", text_font= ("Times","12", "bold"), text_color="black")
rs_label = Ctk.CTkLabel(UNI, text="rs", text_font=("Times","12"), text_color="black")
qs_label = Ctk.CTkLabel(UNI, text="qs", text_font=("Times","12"), text_color="black")
qprima_label= Ctk.CTkLabel(UNI, text="q'", text_font= ("Times", "12"), text_color="black")
uno = Ctk.CTkLabel(UNI, text="1", text_font=("Times","12"), text_color="black")
dos = Ctk.CTkLabel(UNI, text="2", text_font=("Times","12"), text_color="black")




#----------------------------------------------------------------------------------------------------------------------

#----------------------------Entrys -----------------------------------------------------------------------------------
color_entryuni = "#fef6e4"
Path = Ctk.CTkEntry(frame, placeholder_text= "Dirección del archivo",placeholder_text_color="black", fg_color="white", text_color="black", width=30)
Presion = Ctk.CTkEntry(frame, fg_color="white", text_color="black")
Coef1A = Ctk.CTkEntry(frame, fg_color="white", text_color="black")
Coef1B = Ctk.CTkEntry(frame, fg_color="white", text_color="black")
Coef1C = Ctk.CTkEntry(frame, fg_color="white", text_color="black")
Coef2A = Ctk.CTkEntry(frame, fg_color="white", text_color="black")
Coef2B = Ctk.CTkEntry(frame, fg_color="white", text_color="black")
Coef2C = Ctk.CTkEntry(frame, fg_color="white", text_color="black")
Vmol1 = Ctk.CTkEntry(frame, fg_color="white", text_color="black")
Vmol2 = Ctk.CTkEntry(frame, fg_color="white", text_color="black")
rs1_entry = Ctk.CTkEntry(UNI, fg_color=color_entryuni, text_color="#f582ae")
rs2_entry = Ctk.CTkEntry(UNI, fg_color=color_entryuni, text_color="#f582ae")
qs1_entry = Ctk.CTkEntry(UNI, fg_color=color_entryuni, text_color="#f582ae")
qs2_entry = Ctk.CTkEntry(UNI, fg_color=color_entryuni, text_color="#f582ae")
qprima_entry = Ctk.CTkEntry(UNI, fg_color=color_entryuni, text_color="#f582ae")
qprima_entry2 = Ctk.CTkEntry(UNI, fg_color=color_entryuni, text_color="#f582ae")


#----------------------------------------------------------------------------------------------------------------------

#----------------------------BOTONES-----------------------------------------------------------------------------------
Abrir = Ctk.CTkButton(frame, text="Abrir archivo", command=obtener_path, fg_color="#f582ae", hover_color="#f3d2c1", text_color="#001858")
sig = Ctk.CTkButton(frame, text="Siguiente", command=next, fg_color="#f582ae", hover_color="#f3d2c1", text_color="#001858")
Centi= Radiobutton(frame,bg=bgcolor, text= "C°",variable = Tiposistema, value= 0)
Kelvin= Radiobutton(frame,bg=bgcolor, text= "K", variable = Tiposistema, value= 1)


#----------------------------------------------------------------------------------------------------------------------





#root.filename = filedialog.askopenfilename(initialdir=/C, title ="Select a file", filetypes=("excel files","*.excl"))
#----------------------------Posición de todos los elementos -----------------------------------------------------------
Path.place(relwidth=0.3, relx=0.1, rely=0.1)
Abrir.place(relwidth=0.2, relx=0.5, rely=0.1)


Pres.place ( relwidth= 0.13, relx=0.1 , rely=0.2)
Presion.place(relwidth= 0.147, relx=0.23 , rely=0.2)
Kpa.place(relx=0.39 , rely=0.2, relwidth= 0.05)

coefa1.place(relx= 0.1, rely = 0.3 )
#K.place(relx= 0.70, rely=0.17)
#Centi.place(relx=0.7, rely=0.21)
#Kelvin.place(relx=0.7, rely=0.25)
A.place(relx=0.15, rely=0.35, relwidth= 0.01)
B.place(relx=0.35, rely=0.35, relwidth= 0.01)
C.place(relx=0.55, rely=0.35, relwidth= 0.01)
Coef1A.place(relx= 0.1, relwidth= 0.1, rely= 0.40)
Coef1B.place(relx= 0.3, relwidth= 0.1, rely= 0.40)
Coef1C.place(relx= 0.5, relwidth= 0.1, rely= 0.40)

coefa2.place(relx= 0.1, rely = 0.5 )
A1.place(relx=0.15, rely=0.55, relwidth= 0.01)
B1.place(relx=0.35, rely=0.55, relwidth= 0.01)
C1.place(relx=0.55, rely=0.55, relwidth= 0.01)
Coef2A.place(relx= 0.1, relwidth= 0.1, rely= 0.60)
Coef2B.place(relx= 0.3, relwidth= 0.1, rely= 0.60)
Coef2C.place(relx= 0.5, relwidth= 0.1, rely= 0.60)

Vm1.place(relx=0.1, rely= 0.70, relwidth= 0.05)
Vmol1.place(relx=0.15, rely= 0.70 ,relwidth= 0.10)
cm.place(relx=0.26, rely= 0.70, relwidth= 0.05)
Vm2.place(relx=0.31, rely= 0.70, relwidth= 0.05)
Vmol2.place(relx=0.35, rely= 0.70, relwidth= 0.10)
cm1.place(relx=0.46, rely=0.70,relwidth= 0.05 )

sig.place(relx=0.25, rely=0.8, relwidth=0.25, relheight=0.1)

rs_label.place(relx=0.32, rely = 0.2 , relwidth= 0.04)
qs_label.place(relx=0.65, rely = 0.2, relwidth= 0.04)
rs1_entry.place(relx= 0.2, rely= 0.3, relwidth=0.3)
rs2_entry.place(relx= 0.2, rely= 0.4, relwidth=0.3)
qs1_entry.place(relx= 0.55, rely= 0.3, relwidth=0.3)
qs2_entry.place(relx= 0.55, rely= 0.4, relwidth=0.3)
uno.place(relx= 0.1, rely= 0.3, relwidth= 0.04)
dos.place(relx= 0.1, rely = 0.4, relwidth= 0.04)
qprima_label.place(relx = 0.32, rely =0.5, relwidth= 0.04)
qprima_entry.place(relx= 0.2, rely=0.6, relwidth=0.3)
qprima_entry2.place(relx= 0.2, rely=0.7, relwidth=0.3)


Titulo_UNIQUAC.place(relx=0.2 , rely = 0.1)




Tit.pack()

#----------------------------------------------------------------------------------------------------------------------

root.mainloop()

