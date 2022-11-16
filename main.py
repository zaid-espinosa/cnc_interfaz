from tkinter import *
from tkinter import ttk
from Phidget22.Phidget import *
from Phidget22.Devices.BLDCMotor import *
from PIL import Image, ImageTk
from tkinter import messagebox
import serial
import serial
import matplotlib.pyplot as plt
import numpy as np
import time

plt.style.use('ggplot')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

z=0
x=0
y=0

def conectar():
    serialPort = 'COM9'
    baudRate = 9600
    try:
        global serialConnection #Establece que serialConnection sera una variable global
        serialConnection = serial.Serial(serialPort,baudRate)
        print('Conexión exitosa')
    except:
        error = messagebox.askretrycancel("Error", "No se pudo conectar al puerto ",serialPort)
        if error == 'yes':
            interfaz.destroy()
    input_radio['state']=NORMAL
    input_segmentos['state']=NORMAL

def enviar():
    global bldcMotor0
    speed = float(Slide_vel.get())
    bldcMotor0 = BLDCMotor()
    bldcMotor0.setHubPort(0)
    bldcMotor0.setDeviceSerialNumber(673668)
    bldcMotor0.openWaitForAttachment(5000)
    bldcMotor0.setTargetVelocity(1)

def paro():
    global bldcMotor0
    bldcMotor0.close()

def desconectar():
    serialConnection.close()
    print('\nSe finalizo la conexión')

def Poioo():
    segmentos = segmento.get()
    rad = radio.get()
    cx = 0
    cy = 0

    angulo = np.linspace(0, 2 * np.pi, segmentos + 1)
    x = rad * np.cos(angulo) + cx
    y = rad * np.sin(angulo) + cy

    plt.clear()
    plt.set_title("Círculo")
    plt.set_xlabel("X")
    plt.set_ylabel("Y")

    for i in range(segmentos + 1):
        plt.plot(x, y, color="red", markersize=1)
        plt.plot(x[i], y[i], 'bo')
        line.draw()
        time.sleep(0.1)
        #
        xs = str((x[i]))
        ys = str((y[i]))
        zs = str(10)
        datos = [xs, ys, zs]
        datos = ", ".join(datos)
        serialConnection.write(datos.encode('ascii'))
        print(f'\n Eje x: {xs}\n Eje y: {ys}\n Profundidad: {zs}')

root = Tk()

root.geometry("600x400")
root.configure(bg = '#6D1A42' )
root.title("Interfaz CNC")

#Titulo
titulo = Label(root,text="Interfaz CNC 7SV1", bg="#6D1A42", fg = "white", font= ("Verdana", 20)).place(x = 150, y = 3)

#Logo IPN
logo = Image.open("D:\Imagenes\CNC\LOGO.png")
new_logo = logo.resize((53, 78))
ren_log = ImageTk.PhotoImage(new_logo)
Log = Label(root, image=ren_log, borderwidth = 0,  bg="#6D1A42").place(x = 525.048, y = 7.872)

#Botón ON/OF
img = Image.open("D:\Imagenes\CNC\ON.png")
new_img = img.resize((53, 53))
render = ImageTk.PhotoImage(new_img)
button = Button(root, image=render, borderwidth = 0,  bg="#6D1A42", command= enviar).place(x = 21.793, y = 63.332)

#Texto ON/OF
label = Label(root,text="On/Off", bg="#6D1A42", fg = "white", font= ("Verdana", 14)).place(x = 81.878, y = 84.398)

#Fondo_1
fond = Image.open("D:\Imagenes\CNC\ect.png")
new_fond = fond.resize((314, 244))
ren = ImageTk.PhotoImage(new_fond)
fondo = Label(root, image=ren, borderwidth = 0,  bg="#6D1A42").place(x = 21.114, y = 139.953)

#Fondo profundidad/radio/segmento
fond_1 = Image.open("D:\Imagenes\CNC\ect_rad.png")
new_fond1 = fond_1.resize((224, 92))
rend = ImageTk.PhotoImage(new_fond1)
fondoo = Label(root, image=rend, borderwidth = 0,  bg="#6D1A42").place(x = 361.033, y = 184.403)

#texto input profundidad
text_prof = Label(root,text="Profundidad: ",  bg="#cccccc", fg = "black", font= ("Verdana", 10)).place(x = 368.161, y = 245.977)

#entrada de profundidad
prof=IntVar()
input_prof = Entry(root, width=14, textvariable=prof, state = DISABLED)
input_prof.place(x = 483.626, y = 248.432)


#texto del input radio
text_radio = Label(root,text="Radio: ",  bg="#cccccc", fg = "black", font= ("Verdana", 10)).place(x = 367.891, y = 219.577)

#entrada de texto radio
radio = DoubleVar()
input_radio = Entry(root, width=14, textvariable=radio, state = DISABLED)
input_radio.place(x = 483.368, y = 220.024)

#texto del input segmentos
input_segmentos = Label(root,text="Segmentos: ",  bg="#cccccc", fg = "black", font= ("Verdana", 10)).place(x = 368.246, y = 191.105)

#entrada de texto segento
segmento=IntVar()
input_segmentos= Entry(root, width=14, textvariable=segmento, state = DISABLED)
input_segmentos.place(x = 483.656, y = 191.557)


#Fondo botenes stop start
ondoboto = Image.open("D:\Imagenes\CNC\ondo_boto.png")
fond1 = ondoboto.resize((224, 104))
rend_bot = ImageTk.PhotoImage(fond1)
fondbot = Label(root, image=rend_bot, borderwidth = 0,  bg="#6D1A42").place(x = 361.174, y = 282.346)

#Boton start
start = Image.open("D:\Imagenes\CNC\start.png")
but_start = start.resize((58, 58))
re_start = ImageTk.PhotoImage(but_start)
button_start = Button(root, image=re_start, borderwidth = 0,  bg="#cccccc", command=Poioo).place(x = 381.8, y = 286.003)

#Boton stop
stop = Image.open("D:\Imagenes\CNC\stop.png")
but_stop = stop.resize((70, 60))
re_stop = ImageTk.PhotoImage(but_stop)
button_stop = Button(root, image=re_stop, borderwidth = 0,  bg="#cccccc", state = DISABLED).place(x = 495.804, y = 286.215)

#Boton reset
reset = Image.open("D:\Imagenes\CNC\eset.png")
but_reset = reset.resize((101, 28))
re_reset = ImageTk.PhotoImage(but_reset)
button_reset = Button(root, image=re_reset, borderwidth = 0,  bg="#cccccc", state = DISABLED).place(x = 419.128, y = 354.641)

#Fondo connect
fondo_conne = Image.open("D:\Imagenes\CNC\ect_conne.png")
fond_con = fondo_conne.resize((101, 39))
rend_con = ImageTk.PhotoImage(fond_con)
button_connection = Label(root, image=rend_con, borderwidth = 0,  bg="#6D1A42").place(x = 483.702, y = 139.476)

#Fondo disconnect
fondo_disconne = Image.open("D:\Imagenes\CNC\ect_conne.png")
fond_discon = fondo_disconne.resize((101, 39))
rend_discon = ImageTk.PhotoImage(fond_discon)
button_disconnection = Label(root, image=rend_discon, borderwidth = 0,  bg="#6D1A42").place(x = 361.197, y = 139.529)

#Boton connect
connect = Image.open("D:\Imagenes\CNC\connect.png")
but_connect = connect.resize((93, 27))
re_connect = ImageTk.PhotoImage(but_connect)
button_connect = Button(root, image=re_connect, borderwidth = 0,  bg="#cccccc").place(x = 364.259, y = 145.136)

#Boton disconnect
disconnect = Image.open("D:\Imagenes\CNC\disconnect.png")
but_disconnect = disconnect.resize((94, 27))
re_disconnect = ImageTk.PhotoImage(but_disconnect)
button_disconnect = Button(root, image=re_disconnect, borderwidth = 0,  bg="#cccccc").place(x = 486.877, y = 144.991)

#-------Configuración---------
frame_derecha = Frame(root, bg='#C0C0C0', bd=1.5)
frame_derecha.place(relx=0.05, rely=0.38, relwidth=0.49, relheight=0.55)

#-------Gráfica---------
figure = plt.Figure()
plt = figure.add_subplot(1, 1, 1)
plt.set_xlabel("X")
plt.set_ylabel("Y")
plt.set_title("Gráfica de posición")
plt.tick_params(direction='out', length=1, width=2, colors='r', grid_color='r', grid_alpha=0.5)
plt.grid(color='gray', linestyle='dashed', linewidth=1, alpha=0.45)
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
line = FigureCanvasTkAgg(figure, frame_derecha)
line.get_tk_widget().pack(side=LEFT, fill=BOTH,expand=1)
#----------------------

root.mainloop()