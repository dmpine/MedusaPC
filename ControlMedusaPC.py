# -*- coding: utf-8 -*-
"""
Programa de control Medusa
Autor: Daniel Mauricio Pineda Tobon
Fecha de modificiación: 02032020
Versión del código: 1.91
Descripcion: Control de Medusa para SO Windows
"""

# Librerías requeridas
import numpy as np
import time, datetime, serial, cv2
import tkinter as tk
from functools import partial

# Creo la ventana principal para iniciar la librería tk
ventana = tk.Tk()
ventana.title("MEDUSA G V1.91 (ALPHA) - Plantopía, UNAL")
ventana.resizable(0, 0) # Para evitar que se pueda reescalar la ventana
# Ajusto el tamaño de la ventana
ventana.geometry("470x355")

########################################################################
###################### Variables globales importantes ##################
# Resolución de la cámara
resX = 1280
resY = 720
nbandas = 14 # No se tendrá en cuenta la blanca
# Numeros de puertos
puertosDisponibles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# Longitudes de onda disponibles
LongOndaStr = ["419nm", "446nm", "470nm", "502nm", "533nm", "592nm",\
               "632nm", "660nm", "723nm", "769nm", "858nm", "880nm",\
                   "950nm", "NOT", "BLA"]
blanco = 14
ser = 0
im_shape = (resY, resX)
dummyImg = np.zeros((im_shape[0], im_shape[1]))
# Longitudes de onda como variables
L419 = tk.IntVar()
L446 = tk.IntVar()
L470 = tk.IntVar()
L502 = tk.IntVar()
L533 = tk.IntVar()
L592 = tk.IntVar()
L632 = tk.IntVar()
L660 = tk.IntVar()
L723 = tk.IntVar()
L769 = tk.IntVar()
L858 = tk.IntVar()
L880 = tk.IntVar()
L950 = tk.IntVar()
LNOT = tk.IntVar()
LBLA = tk.IntVar()
# Es conveniente tenerlos en un vector
LongOnda = [L419, L446, L470, L502, L533, L592, L632, L660, L723, L769,\
                    L858, L880, L950, LNOT, LBLA]
# Variables de tiempo
activado = tk.IntVar()
Hi = tk.IntVar()
Mi = tk.IntVar()
Hf = tk.IntVar()
Mf = tk.IntVar()

# Creo una variable para cada banda de iluminación
iL419 = tk.IntVar()
iL446 = tk.IntVar()
iL470 = tk.IntVar()
iL502 = tk.IntVar()
iL533 = tk.IntVar()
iL592 = tk.IntVar()
iL632 = tk.IntVar()
iL660 = tk.IntVar()
iL723 = tk.IntVar()
iL769 = tk.IntVar()
iL858 = tk.IntVar()
iL880 = tk.IntVar()
iL950 = tk.IntVar()
iLNOT = tk.IntVar()
iLBLA = tk.IntVar()
# Es conveniente tenerlos en un vector
iLongOnda = [iL419, iL446, iL470, iL502, iL533, iL592, iL632, iL660, iL723, iL769,\
                    iL858, iL880, iL950, iLNOT, iLBLA]

########################################################################

########################################################################
############################### Funciones ##############################

# Función para encender/apagar un LED específico #######################
def switchLED(LED, opcion, permanente):
    if permanente == False:
        if opcion == 1:
            #serial.Serial(COM.get()).write(str.encode(str(LED) + 'H'))
            ser.write(str.encode(str(LED) + 'H' + "\r\n"))
        elif opcion == 2:
            #serial.Serial(COM.get()).write(str.encode(str(LED) + 'L'))
            ser.write(str.encode(str(LED) + 'L' + "\r\n"))
        else:
            #serial.Serial(COM.get()).write(str.encode("100L"))
            ser.write(str.encode("100L" + "\r\n"))
    else:
        if opcion == 1:
            #serial.Serial(COM.get()).write(str.encode(str(LED) + 'I'))
            ser.write(str.encode(str(LED) + 'I' + "\r\n"))
        elif opcion == 2:
            #serial.Serial(COM.get()).write(str.encode(str(LED) + 'L'))
            ser.write(str.encode(str(LED) + 'L' + "\r\n"))
        else:
            #serial.Serial(COM.get()).write(str.encode("100L"))
            ser.write(str.encode("100L" + "\r\n"))
        #TODO: Para iluminación programada luz permanente
########################################################################

# Función para conectar/desconectar el puerto serial: ##################
def Conectar(CON, COM, STAT):
    global ser
    if CON.get() == "Conectar":
        ser = serial.Serial(COM.get(), 9600, timeout=0)
        STAT.set("Arduino conectado")
        CON.set("Desconectar")
        #print(ser)
    elif CON.get() == "Desconectar":
        #serial.Serial(COM.get()).close()}
        ser.close()
        STAT.set("Arduino desconectado")
        CON.set("Conectar")
########################################################################
        
# Función para realizar vista previa de la cámara: #####################
def vistaPrevia(STAT):
    STAT.set("Vista previa en proceso...")
    switchLED(0, 0, False) # Apago todos los LEDs inicialmente
    switchLED(blanco, 1, False) # Activo el LED blanco
    time.sleep(0.5)
    # Selecciono la cámara de interés
    cap = cv2.VideoCapture(int(CAM.get()))
    # Ajusto la resolución
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resX)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resY)
    contadorTest = 0
    while(True):
        # Capturo un cuadro                
        retval, cuadro = cap.read()
        cv2.imshow("Medusa", cuadro)
        # En caso de que la cámara por alguna razón no funcione
        # o se desconecte inesperadamente, cierro el programa:
        if not retval:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            #print("Cancelado...")
            STATUS.set("Vista previa finalizada.")
            break
        elif k%256 == 32:                    
            #print("Imagen capturada\r\n")
            STATUS.set(str("Imagen " + str(contadorTest) + " capturada"))
            cv2.imwrite("Test" + str(contadorTest) + ".jpg", cuadro)
            contadorTest += 1
            time.sleep(1)
    switchLED(0, 0, False) # Apago todos los LEDs
    cap.release()
    cv2.destroyAllWindows()
########################################################################

# Función para seleccionar/deseleccionar todas las bandas para capturar/iluminar
def todoNada(bandas, incluir):
    if incluir == True:
        for i in bandas:
            i.set(1)
    else:
        for i in bandas:
            i.set(0)
########################################################################

# Función para tomar fotos: ############################################
def tomarFoto(CAM, nombre, numero, color, imRef):
    # Activo la cámara
    cap = cv2.VideoCapture(int(CAM.get()))
    # Ajusto la resolución
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resX)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resY)
    # Capturo varios cuadros
    nc = 0
    while(nc < 10):
        nc = nc + 1
        retval, cuadro = cap.read()
        time.sleep(0.1)
    cap.release()
    if color == False:
        # Convierto las imagenes en bn
        grisRef = cv2.cvtColor(imRef, cv2.COLOR_BGR2GRAY)
        gris = cv2.cvtColor(cuadro, cv2.COLOR_BGR2GRAY)
        # Guardo la imagen
        im = cv2.subtract(gris, grisRef)
        #vecFoto.append(im)
        global dummyImg
        dummyImg = im
        cv2.imwrite(str(numero) + '_' + str(nombre) + ".png", im)
    elif color == True:
        imCol = cv2.subtract(cuadro, imRef)
        #vecFoto.append(imCol)
        cv2.imwrite(str(numero) + '_' + str(nombre) + ".png", imCol)
        
    cv2.destroyAllWindows()
########################################################################

# Función combinada para iluminar y tomar fotos: #######################
def luzYfoto(LED, CAM, nombre, numero, color):
    # Primero se deben apagar todos los LEDs
    switchLED(0, 0, False)
    # Se captura una imagen de referencia con las luces apagadas
    # Activo la cámara
    cap = cv2.VideoCapture(int(CAM.get()))
    # Ajusto la resolución
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resX)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resY)
    # Capturo varios cuadros
    nc = 0
    while(nc < 10):
        nc = nc + 1
        retval, imRef = cap.read()
        time.sleep(0.1)
    cap.release()

    # Se enciende la luz correspondiente y se toma la imagen
    switchLED(LED, 1, False)
    # Capturamos la imagen
    tomarFoto(CAM, nombre, numero, color, imRef)
    # Se apagan de nuevo los LEDs
    switchLED(0, 0, False)
########################################################################

# Función combinada para iluminar y tomar fotos: #######################
def tomarConjuntos(CAM, NCONJ, TCONJ, INIT, STAT, activado):
    if INIT.get() == "INICIAR":
        # Envío un mensaje a la barra de estado
        STAT.set("Iniciando toma de conjuntos...")
        # Actualizo el nombre del botón
        INIT.set("DETENER")
        ventana.update()
        time.sleep(1.5)
        # Se deben apagar todos los LEDs
        switchLED(0, 0, False)
        # Creo vectores con los puertos seleccionados
        Puertos = []
        NombresFotos = []
        for i, j, k in zip(LongOnda, LongOndaStr, puertosDisponibles):
            if i.get() == 1:
                NombresFotos.append(j)
                Puertos.append(k)

        # Para contar el tiempo
        delayTot = int(TCONJ.get())
        conjTot = int(NCONJ.get())
        delay = 0
        step = 0.25
        for n in range(conjTot):
            STAT.set("Capturando imágenes, por favor espere.")
            ventana.update()
            switchLED(0, 0, False) #Pongo todo en 0 antes de tomar las fotos
            # Verifico si se consideró el blanco
            bd = 0
            for u in Puertos:
                if u != blanco:
                    bd = bd + 1
            lenPuertos = len(Puertos)
            IMGs = np.zeros((im_shape[0], im_shape[1], bd))
            for p, nomb, j, num in zip(Puertos, NombresFotos, range(bd+1), range(lenPuertos)):
                STAT.set("Capturando imágenes, por favor espere: " + LongOndaStr[p] + " (" + str(num+1) + " de " + str(lenPuertos) + ")")
                ventana.update()
                if p == blanco:
                    luzYfoto(p, CAM, nomb, n, True)
                else:
                    luzYfoto(p, CAM, nomb, n, False)
                    IMGs[:,:,j] = dummyImg
            if(TIMELAPSEPCA.get() == 1):
                ################# FUNCIÓN PCA ############################
                # Proceso de PCA
                STAT.set("Procesando imágenes para PCA...")
                ventana.update()
                time.sleep(1)
                # Convierto las matrices en vectores para facilitar los cálculos,
                # también se debe estandarizar todo
                IMG_matrix = np.zeros((IMGs[:,:,0].size, bd))
                for i in range(bd):
                    IMG_array = IMGs[:,:,i].flatten()  # covertimos 2d a 1d
                    IMG_arrayStd = (IMG_array - IMG_array.mean()) / IMG_array.std()
                    IMG_matrix[:,i] = IMG_arrayStd
                IMG_matrix.shape;
                
                # Se calculan los autovalores
                np.set_printoptions(precision=3)
                cov = np.cov(IMG_matrix.transpose())# Eigen Values
                EigVal,EigVec = np.linalg.eig(cov)
                print("Autovalores:\n\n", EigVal,"\n")
                
                # Se organizan los autovalores y autovectores
                order = EigVal.argsort()[::-1]
                EigVal = EigVal[order]
                # Se proyectan los datos en dirección de los autovectores resultando en la CP
                EigVec = EigVec[:,order]
                # Producto cruz (matricial)
                PC = np.matmul(IMG_matrix, EigVec)
                
                # Pasamos de los CP a imágenes
                # Reorganizamos los arreglos 1-d a 2-d
                PC_2d = np.zeros((im_shape[0],im_shape[1],bd))
                for i in range(bd):
                    PC_2d[:,:,i] = PC[:,i].reshape(-1, im_shape[1])# Normalizacion de 0 a 255
                PC_2d_Norm = np.zeros((im_shape[0], im_shape[1], bd))
                for i in range(bd):
                    PC_2d_Norm[:,:,i] = cv2.normalize(PC_2d[:,:,i],
                                    np.zeros(im_shape),0,255 ,cv2.NORM_MINMAX)
                    
                cv2.imwrite(str(n) + "_PC1.png", PC_2d_Norm[:,:,0])
                cv2.imwrite(str(n) + "_PC2.png", PC_2d_Norm[:,:,1])
                cv2.imwrite(str(n) + "_PC3.png", PC_2d_Norm[:,:,2])
                    
                STAT.set("¡PCA realizado correctamente!")
                    ##########################################################
                pass
            
            #TODO: Iluminación programada
            if n != conjTot:
                if activado.get() == 1:
                    LEDi = []
                    pui = []
                    for LEDi, pui in zip(iLongOnda, puertosDisponibles):
                        if LEDi.get() == 1:
                            IluminacionProgramada(pui, Hi.get(), Mi.get(), Hf.get(), Mf.get())
            
            # Para mostrar el progreso en la barra de estado
            while delay < delayTot:
                if n >= conjTot - 1:
                    break
                elif INIT.get() == "INICIAR":
                    n = conjTot
                    switchLED(0, 0, False)
                    break
                time.sleep(step)
                delay = delay + step       
                porc = 100 * (n+1) / conjTot
                STAT.set("Progreso: " + str(n+1) + " conjuntos de " + NCONJ.get() + " -> " + str(porc) + "%" )
                ventana.update()
            delay = 0
            if INIT.get() == "INICIAR":
                n = conjTot
                switchLED(0, 0, False)
                break

        # Apago todo de nuevo una vez completado el ciclo
        switchLED(0, 0, False)
        # Actualizo el nombre del botón
        INIT.set("INICIAR")
        STAT.set("Toma de conjuntos finalizada!")
    else:
        #STAT.set("Toma de conjuntos cancelada...")
        #switchLED(0, 0, False)
        INIT.set("INICIAR")
########################################################################

# Función para realizar iluminación programada: ########################
def IluminacionProgramada(puerto, Hi, Mi, Hf, Mf):
    tiempo = datetime.datetime.now()
    hora = tiempo.hour
    minuto = tiempo.minut
    switchLED(puerto, 1, True)
    # Para manipular con comodidad el tiempo 
    tActual = hora * 60 + minuto
    tInicial = Hi * 60 + Mi
    tFinal = Hf * 60 + ModuleNotFoundError
    if tInicial < tActual & tActual < tFinal:
        switchLED(puerto, 1, True)
    else:
        switchLED(0, 0, False)
########################################################################


############################# Fin Funciones ############################
########################################################################

########################################################################
##################### Configuración de la ventana ######################
########################################################################

# Creo dos frames principales para las dos funcionalidades
# de Medusa, uno para configurar la cámara y el puerto de datos,
# otro para configurar captura de fotos y otro para iluminación
# programada y contínua.
frConf = tk.Frame(ventana,
                  highlightbackground="black",
                  highlightcolor="black",
                  highlightthickness=1,
                  bd=5
                  )
frCap = tk.Frame(ventana,
                 highlightbackground="black",
                 highlightcolor="black",
                 highlightthickness=1,
                 bd=5)
frIlum = tk.Frame(ventana,
                  highlightbackground="black",
                  highlightcolor="black",
                  highlightthickness=1,
                  bd=5)
# frMultiVar = tk.Frame(ventana,
#                   highlightbackground="black",
#                   highlightcolor="black",
#                   highlightthickness=1,
#                   bd=5)
# Para actualizar la barra de estado
STATUS = tk.StringVar()
frStat = tk.Frame(ventana)
#stat = tk.StatusBar(ventana)

# De aquí en adelante agregaré todos los elementos para interactuar
###################################################################
###################################################################

############################# frConf ##############################
# Widgets para configuración de cámara y puerto (frConf)
# Variables para cámara y puerto de arduino
CAM = tk.StringVar()
COM = tk.StringVar()
CON = tk.StringVar()

lbCamara = tk.Label(frConf, text="P. cámara: ").pack(side="left")
txtCamara = tk.Entry(frConf, width=8, textvariable=CAM).pack(side="left")
lbPuerto = tk.Label(frConf, text=" P. Arduino: ").pack(side="left")
txtPuerto = tk.Entry(frConf, width=8, textvariable=COM).pack(side="left")
tk.Label(frConf, text=" ").pack(side="left")
btnConectar = tk.Button(frConf, 
                        textvariable=CON, 
                        bg="blue", 
                        fg="white",
                        command=partial(Conectar, CON, COM, STATUS)
                        ).pack(side="left")
tk.Label(frConf, text=" -->").pack(side="left")
btnPrev = tk.Button(frConf, 
                    text="Vista previa",
                    bg="green",
                    fg="white",
                    command=partial(vistaPrevia, STATUS)
                    ).pack(side="left")
tk.Label(frConf, text="<-- ").pack(side="left")
# Agrego los valores por defecto de los txt
CAM.set("0")
COM.set("COM0")
CON.set("Conectar")
# Agrego estos elementos al frame frConf
frConf.pack()
###################################################################

############################# frCap ###############################
# Widgets para configuración de cámara y puerto (frCap)
# Tenemos varios subframes
frCap_1 = tk.Frame(frCap)
frCap_2 = tk.Frame(frCap)
frCap_3 = tk.Frame(frCap)
frCap_4 = tk.Frame(frCap)
# En cada subframe organizo distintos widgets

btnSelect = tk.Button(frCap_1, text="Seleccionar todas", command=partial(todoNada, LongOnda, True)).pack(side="left")
tk.Label(frCap_1, text="   ").pack(side="left")
btnDeselect = tk.Button(frCap_1, text="Deseleccionar todas", command=partial(todoNada, LongOnda, False)).pack(side="left")
TIMELAPSEPCA = tk.IntVar()
TIMELAPSEPCA.set(0)
tk.Label(frCap_1, text=" ---- ").pack(side="left")
chkTimelapsePCA = tk.Checkbutton(frCap_1, text="¿Realizar PCA por conjunto?", variable=TIMELAPSEPCA).pack(side="left")


# Ubico todos los botones de checkeo de cada banda:
for i in range(5):
    tk.Checkbutton(frCap_2, 
                   text=LongOndaStr[i], 
                   variable=LongOnda[i]
                   ).grid(row=1, column=i)
for i in range(5):
    tk.Checkbutton(frCap_2, 
                   text=LongOndaStr[i+5], 
                   variable=LongOnda[i+5]
                   ).grid(row=2, column=i)
for i in range(5):
    tk.Checkbutton(frCap_2, 
                   text=LongOndaStr[i+5+5], 
                   variable=LongOnda[i+5+5]
                   ).grid(row=3, column=i)

# Variables para número de conjuntos y para tiempo entre conjuntos
NCONJ = tk.StringVar()
TCONJ = tk.StringVar()
INIT = tk.StringVar()
lbNconj = tk.Label(frCap_3, text="No. Conjuntos ").pack(side="left")
txtNconj = tk.Entry(frCap_3, textvariable=NCONJ, width=6).pack(side="left")
lbTconj = tk.Label(frCap_3, text="Intervalo (s) ").pack(side="left")
txtTconj = tk.Entry(frCap_3, textvariable=TCONJ, width=6).pack(side="left")
tk.Label(frCap_3, text=" ------->").pack(side="left")
btnIniciar = tk.Button(frCap_3, 
                       textvariable=INIT, 
                       command=partial(tomarConjuntos, CAM, NCONJ, TCONJ, INIT, STATUS, activado),
                       bg="red",
                       fg="white").pack(side="left")
tk.Label(frCap_3, text="<-------").pack(side="left")

# Agrego los valores por defecto de los txt
NCONJ.set("1")
TCONJ.set("0")
INIT.set("INICIAR")

# Opciones para recortar la imagen
RECORTAR = tk.IntVar()
RECORTAR.set(0)
chkRecortar = tk.Checkbutton(frCap_4, text="¿Recortar imagen?", variable=RECORTAR).pack(side="left")
RADIORECORTE = tk.StringVar()
RADIORECORTE.set("300")
tk.Label(frCap_4, text=" -- Radio de recorte (px): ").pack(side="left")
txtRecortar = tk.Entry(frCap_4, textvariable = RADIORECORTE, width=5).pack(side="left")
tk.Label(frCap_4, text="Posición: (").pack(side="left")
POSRECORTEX = tk.StringVar()
POSRECORTEX.set("400")
POSRECORTEY = tk.StringVar()
POSRECORTEY.set("200")
txtPOSX = tk.Entry(frCap_4, textvariable=POSRECORTEX, width=5).pack(side="left")
tk.Label(frCap_4, text=",").pack(side="left")
txtPOSY = tk.Entry(frCap_4, textvariable=POSRECORTEY, width=5).pack(side="left")
tk.Label(frCap_4, text=")").pack(side="left")

# Agrego estos subframes al frame principal
frCap_1.pack()
frCap_2.pack()
frCap_3.pack()
#frCap_4.pack()
frCap.pack()
###################################################################

############################# frIlum ###############################
# Widgets para configuración de cámara y puerto (frIlum)
# Tenemos varios subframes
frIlum_1 = tk.Frame(frIlum)
frIlum_2 = tk.Frame(frIlum)
frIlum_3 = tk.Frame(frIlum)
frIlum_4 = tk.Frame(frIlum)
# En cada subframe organizo distintos widgets

# Opción para activar o no la iluminación programada
tk.Checkbutton(frIlum_1, text="¿Activar iluminación programada?", variable=activado).pack()

# Hora inicial
lbHorai = tk.Label(frIlum_2, text="Hora inicial").pack(side="left")
txtHorai = tk.Entry(frIlum_2, textvariable=Hi, width=4).pack(side="left")
tk.Label(frIlum_2, text=":").pack(side="left")
txtMini = tk.Entry(frIlum_2, textvariable=Mi, width=4).pack(side="left")
# Hora final
tk.Label(frIlum_2, text="          ").pack(side="left")
lbHoraf = tk.Label(frIlum_2, text="Hora final").pack(side="left")
txtHoraf = tk.Entry(frIlum_2, textvariable=Hf, width=4).pack(side="left")
tk.Label(frIlum_2, text=":").pack(side="left")
txtMinf = tk.Entry(frIlum_2, textvariable=Mf, width=4).pack(side="left")

btnSelect = tk.Button(frIlum_3, text="Seleccionar todas", command=partial(todoNada, iLongOnda, True)).pack(side="left")
tk.Label(frIlum_3, text="      ").pack(side="left")
btnDeselect = tk.Button(frIlum_3, text="Deseleccionar todas", command=partial(todoNada, iLongOnda, False)).pack(side="left")

# Ubico todos los botones de checkeo de cada banda:
for i in range(5):
    tk.Checkbutton(frIlum_4, 
                   text=LongOndaStr[i], 
                   variable=iLongOnda[i]
                   ).grid(row=1, column=i)
for i in range(5):
    tk.Checkbutton(frIlum_4, 
                   text=LongOndaStr[i+5], 
                   variable=iLongOnda[i+5]
                   ).grid(row=2, column=i)
for i in range(5):
    tk.Checkbutton(frIlum_4, 
                   text=LongOndaStr[i+5+5], 
                   variable=iLongOnda[i+5+5]
                   ).grid(row=3, column=i)


# Agrego los valores por defecto de los txt
Hi.set(6)
Mi.set(0)
Hf.set(18)
Mf.set(0)

# Agrego estos subframes al frame principal
frIlum_1.pack()
frIlum_2.pack()
frIlum_3.pack()
frIlum_4.pack()
frIlum.pack()
###################################################################

############################# frStat ##############################
# Widgets para mostrar barra de estado
lbStat = tk.Label(frStat, 
                  textvariable=STATUS,
                  bg="grey",
                  width=350).pack(side="left")

# Agrego los valores por defecto de los txt
STATUS.set("ADVERTENCIA: Arduino no conectado")

# Agrego estos elementos al frame frConf
frStat.pack(side="left")
###################################################################

# Inicio la ventana
ventana.mainloop()





