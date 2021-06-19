import os
import sys
from shutil import rmtree

# librerias necesarias para grabar sonido
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import os 
from scipy.fft import fft,fftfreq,rfftfreq, rfft
from scipy import signal


import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from scipy.io import wavfile



##################################################################################################
# CONSTRUYENDO EL TONO
##################################################################################################

def getArrayDatosTono(duracion=.80,frecuencia_tono=440):
    '''
    Genera el array de datos que le corresponde a una frecuecia de una senoidal pura
    sin ruido

    return:
        fs -- frecuencia de muestreo del tono
        senoidal -- array de datos del tono 
    '''

    fs=44100 
    ts=1/fs
    t=np.arange(0,duracion,ts,dtype=np.float32)
    # C5	523,251       A4 440,000
    senoidal=np.sin(2*np.pi*frecuencia_tono*t)
    return fs,senoidal

def crearTono(nombre,duracion=.80,frecuencia_tono=440):
    '''
    Crea el array de datos de una senoidal a una frecuencia indicada 
    con una duracion especificada, con una frecuencia de muestreo 
    igual a 44100
    '''
    
    fs,arrayDatos=getArrayDatosTono(duracion,frecuencia_tono)
    write(nombre,fs,arrayDatos)


##################################################################################################
# CONSTANTES
##################################################################################################

# obteniendo la direccion de donde se encuentra el programa:

direccionTotal=sys.argv[0]
direccionPartes=os.path.normpath(direccionTotal)
direccionPartes=direccionPartes.split(os.sep)
ruta_direccionTotal = os.sep.join( direccionPartes[:-1] )
if len(direccionPartes)>1:
    ruta_direccionTotal+=os.sep


# una vez obtenida la direccion de donde se encuentra el programa
# se prosigue a declarar las rutas de los archivos que guardara
# el programa
DIR_RECURSOS=ruta_direccionTotal+'recursos/'

DIR_FRASES=DIR_RECURSOS+'frases/'
DIR_VOCALES=DIR_RECURSOS+'vocales/'

# crea estos directorios, en caso de ya existir no hacer nada...
os.makedirs(DIR_FRASES, exist_ok=True)
os.makedirs(DIR_VOCALES, exist_ok=True)


# opcciones del menu
LISTA_OPCCIONES=[
       'Grabar una frase',         
       'Graficar una frase',       
       'Escuchar una frase',       
       'Grabar vocales',  
       'Escuhar vocales',
       'Graficar vocales',  
       'Comparar vocales',
       'Tonos dmft',
       'Salir'           
            ]

NO_OPCCIONES=len(LISTA_OPCCIONES)
FS_TONO,ARRAY_TONO=getArrayDatosTono()



##################################################################################################################
#   GRABAR Y REPRODUCIR
##################################################################################################################

def getDatosSonido(nombre):
    '''
    Obtiene  datos de un archivo de  audio pero solo  si
    este tiene una extensión '.wav'

    Parámetros:
        nombre -- dato de tipo 'str' que representa el nombre del archivo
        de audio del cual se desean obtener sus datos, es importante mencionar
        que el nombre debe contener la ruta completa de en donde se encuentra
        almacenado el archivo.
    
    Returns:
        data -- array de datos que representan los valores de la señal de audio
        fs -- frecuencia de muestro del archivo de audio
    '''
    
    fs,data= wavfile.read(nombre)
    return data,fs


def reproducirSonido(array,fs,manual=True):
    '''
    Reproduce los datos de una señal de audio que estan contenidos en un array.
    La reproduccion puede ser manual o automatica:
        * Si la reproduccion es 'manual' esta función no reproducira la señal
        de audio hasta que el usuario lo indique(presione enter)
        * Si la reproduccion NO ES 'manual' esta funcion reproducira automaticamente
        la señal de audio.
    
    Parámetros:
        array -- array de datos que representa los valores de la señal de audio
        fs -- frecuencia de muestro de la señal de audio
        manual -- dato de tipo 'bool' que indica si la reproduccion de sonido es
        manual o no es manual
    '''

    if manual:
        input("Presiona enter para iniciar la reproduccion... ")
        print()
        print("Iniciando reproduccion")

    sd.play(array, fs)
    status = sd.wait() 

    if manual:
        print()
        print("reproduccion terminada")

def grabarSonido(nombreSonido,duracion=2):
    """
    Esta funcion grabara una señal de audio a una frecuencia de muestreo
    igual a 44,100 [Hz] y posteriormente la guardara en la ruta y con el
    nombre que indican el parametro: 'nombreSonido'.La grabación dudara
    el tiempo que se indique en el parametro 'duracion'

    Parámetros:
        nombreSonido -- Nombre completo del archivo de sonido que se guardara
        una vez terminado de grabar, dicho parametro debe contener la ruta completa
        de en donde se desea guardar el archivo de audio junto con el nombre, el nombre
        debe tener la terminacion '.wav'
        Ejemplo.
            nombreSonido='C:/Users/ronal/Desktop/miGrabacion.wav'
            duracion -- Indicara el tiempo que durara la grabación
    """

    nombreSonido=nombreSonido

    freq = 44100 # Sampling frequency
    duration = duracion # Recording duration
    
    print("Recuerda:")
    print("\t* La grabación iniciara despues del tono")
    print("\t* La grabación culiminara al reproducir el tono")
    print()
    input("Presiona enter para iniciar la grabacion... ")
    print()
    print("Iniciando grabacion...")
    reproducirSonido(ARRAY_TONO,FS_TONO,False)

    # Start recorder with the given values 
    # of duration and sample frequency
    recording = sd.rec(int(duration * freq), 
                    samplerate=freq, channels=1)
    sd.wait()


    reproducirSonido(ARRAY_TONO,FS_TONO,False)
    write(nombreSonido, freq, recording)
    print()
    print("Grabacion exitosa")
    

##################################################################################################################
#   FRASES
##################################################################################################################

def getNombresFrases():
    '''
    Gerara un string que contenga enlistados los nombres de los archivos de audio
    que se encuentran almacenados en la ruta:  'recursos/frases', dichos archivos
    de audio representan las frases de audio que ha grabado el usuario.
    El formato que seguira el string sera el siguiente:
               "1) Archivo_1.wav
                2) Archivo_2.wav
                3) Archivo_3.wav
                        .
                        .
                n) Archivo_n.wav
                "
    Posteriormente tambien creara una lista que contenga los nombres de los archivos de audio
    Una vez hecho todo lo anterior retornara la lista y el string generados.

    Returns:

        listaFrases_str -- string que contiene enlistados los nombres de los archivos 
        ya mencionados
        nombresFrases -- lista que contiene los nombres de los archivos de audio ya explicados
    '''

    nombresFrases=os.listdir(DIR_FRASES)
    listasFrases_str=['\t{}) {}\n'.format(noFrase+1,frase) for noFrase,frase in enumerate(nombresFrases) ]
    listasFrases_str=''.join(listasFrases_str)
    return listasFrases_str,nombresFrases


def grabarFrase():
    '''
    Su funcion principal es grabar una frase emitida por el usuario,
    posteriormente almacenarla, pero antes de grabar la frase, muestra
    los nombres de frases ya existentes y despues  pregunta 
    con que nombre se guardara la frase que grabara.
    '''
    
    frases_str,_=getNombresFrases()
    print("Frases existentes:")
    print(frases_str)
    print("ADVERTENCIA: El nombre de la frase que crees no puede"
    " ser igual a las ya existentes.")
    print()
    nombreFrase=input('Ingresa un nombre a la frase que grabaras: ')
    print()
    grabarSonido(nombreSonido=DIR_FRASES+nombreFrase+'.wav',duracion=4)


def escuharFrase():
    '''
    Reproduce el archivo de audio elegido por el usuario, el usuario
    solo puede elegir entre los archivos de audio que se han guardado
    como frases. 
    '''

    frases_str,frases_list=getNombresFrases()
    print("Frases existentes:")
    print(frases_str)
    
    while True:
        try:
            id_fraseDesea_escuchar=int(input('Ingresa el numero de la frase que deseas escuchar: '))
            fraseDesea_escuchar=frases_list[id_fraseDesea_escuchar-1]
            array,fs=getDatosSonido(DIR_FRASES+fraseDesea_escuchar)
            print()
            print("Frase a reproducir:",fraseDesea_escuchar)
            print()
            reproducirSonido(array=array,fs=fs)
            break
        except ValueError:
            print("Error: debes ingresar solo un numero")
        except IndexError:
            print("Error: ingresaste una opccion que no existe")
    
def graficarFrase():
    '''
    Grafica el archivo de audio elegido por el usuario, el usuario
    solo puede elegir entre los archivos de audio que se han guardado
    como frases.Las graficas que genera son las siguientes:
        - Señal de audio en el dominio del tiempo
        - Transformada de fouerier de la señal de audio
        - El espectrograma de la señal de audio
        - La señal en el dominio del tiempo asi como su espectrograma
    '''


    frases_str,frases_list=getNombresFrases()
    print("Frases existentes:")
    print(frases_str)
    
    while True:
        try:
            id_fraseDesea_escuchar=int(input('Ingresa el numero de la frase que deseas obtener sus graficas: '))
            fraseDesea_escuchar=frases_list[id_fraseDesea_escuchar-1]
            canal1,fs=getDatosSonido(nombre=DIR_FRASES+fraseDesea_escuchar)
            
            noMuestras=canal1.shape[0]
            ts=1/fs
            duracion=noMuestras*ts
            tiempo=np.arange(0,duracion,ts)
            normalized_canal1 = np.int16((canal1/canal1.max()) * 32767)
            yf = rfft(normalized_canal1)
            xf = rfftfreq(noMuestras, 1 / fs)


            plt.title("Señal en el tiempo")
            plt.plot(tiempo,canal1)
            plt.show()

            plt.title("Señal en la frecuencia")
            plt.plot(xf, np.abs(yf))
            plt.show()

            plt.title('Espectrograma de la señal')
            plt.xlabel('tiempo')
            plt.ylabel('frecuencia')
            plt.specgram(canal1,Fs=fs)
            plt.show()

            plt.subplot(211)
            plt.title('Espectograma de señal y señal en el tiempo')
            plt.plot(tiempo,canal1)
            plt.subplot(212)
            plt.specgram(canal1,Fs=fs)
            plt.show()

            break

        except ValueError:
            print("Error: debes ingresar solo un numero")
        except IndexError:
            print("Error: ingresaste una opccion que no existe")
        
##################################################################################################################
#   VOCALES
##################################################################################################################


def getNombresVocalistas():
    '''
    Gerara un string que contenga enlistados los nombres de las carpetas
    que se encuentran almacenadas en la ruta:  'recursos/vocales', el nombre
    de cada carpeta representa el nombre de cada persona que decidio grabarse
    diciendo las 5 vocales, y cada carpeta almacena dichos archivos de audio
    El formato que seguira el string sera el siguiente:
               "1) NombreCarpeta_1
                2) NombreCarpeta_2
                3) NombreCarpeta_3
                        .
                        .
                n) NombreCarpeta_n
                "
    Posteriormente tambien creara una lista que contenga los nombres de las carpetas,
    una vez hecho todo lo anterior retornara la lista y el string generado.

    Returns:
        listasCarpetas_str -- string que contiene enlistados los nombres de las carpetas
        nombresCarpetas -- lista que contiene los nombres de las carpetas
    '''

    nombresCarpetas=os.listdir(DIR_VOCALES)
    listasCarpetas_str=['\t{}) {}\n'.format(noCarpeta+1,nombreCarpeta) for noCarpeta,nombreCarpeta in enumerate(nombresCarpetas) ]
    listasCarpetas_str=''.join(listasCarpetas_str)
    return listasCarpetas_str,nombresCarpetas

def escuharVocales():
    '''
    Reproduce los archivos de audio de las grabaciones de vocales que hizo un usuario, dicho
    usuario tiene que ser elegido, atravez del menu que muestra esta funcion, en el cual vienen
    los nombres de todos los usuarios que han decidido grabarse diciendo las vocales.
    En pocas palabras muestra la lista de los nombres de usuarios que han decidido grabarse
    diciendo las vocales y posteriormente  pregunta a cual de ellos quiere escucharse.
    '''

    vocalista_str,vocalista_list=getNombresVocalistas()
    print("Vocalistas: ")
    print(vocalista_str)
    
    while True:
        try:
            id_vocalista_escuchar=int(input('Ingresa el numero del vocalista que deseas escuchar: '))
            vocalista_escuchar=vocalista_list[id_vocalista_escuchar-1]
            dir_vocalista=DIR_VOCALES+vocalista_escuchar+'/'
            print("Vocalista: ",vocalista_escuchar)
            for vocal in ['a','e','i','o','u']:
                array,fs=getDatosSonido(dir_vocalista+vocal+'.wav')
                print(f"Reproduciendo vocal : ' {vocal} ' ...")
                reproducirSonido(array=array,fs=fs,manual=False)
            break
        except ValueError:
            print("Error: debes ingresar solo un numero")
        except IndexError:
            print("Error: ingresaste una opccion que no existe")


def graficarVocales():
    '''
    Muestra la lista de los nombres de usuarios que han decidido grabarse
    diciendo las vocales y posteriormente  pregunta de cual de ellos quiere
    obtenerse las graficas de los archivos de audio de sus grabaciones diciendo
    las vocales, despues muestra dichas graficas, las cuales son:
        - Una ventana que muestra los archivos  de audio 'a','e','i','o','u'
        en el dominio del tiempo
        - Una ventana que muestra los archivos  de audio 'a','e','i','o','u'
        en el dominio de la frecuencia
    '''

    vocalista_str,vocalista_list=getNombresVocalistas()
    print("Vocalistas: ")
    print(vocalista_str)
    
    while True:
        try:
            id_vocalista_escuchar=int(input('Ingresa el numero del cual quieres obtener sus graficar: '))

            vocalista_escuchar=vocalista_list[id_vocalista_escuchar-1]
            dir_vocalista=DIR_VOCALES+vocalista_escuchar+'/'
            print("Vocalista: ",vocalista_escuchar)

            for numeroVocal,vocal in enumerate(['a','e','i','o','u']):

                array,fs=getDatosSonido(dir_vocalista+vocal+'.wav')
                noMuestras=array.shape[0]
                ts=1/fs
                duracion=noMuestras*ts
                tiempo=np.arange(0,duracion,ts)
                normalized_array = np.int16((array/array.max()) * 32767)
                yf = rfft(normalized_array)
                xf = rfftfreq(noMuestras, 1 / fs)

                titulo="vocal: ' {} ' ".format(vocal)

                plt.figure(1)
                # grafica de la vocal:'vocal' en el dominio del tiempo
                noGrafica=321+numeroVocal  # 5 renglones 1 columna...   
                plt.subplot(noGrafica)
                plt.plot(tiempo,array,label=titulo)
                plt.legend()

                plt.figure(2)
                # grafica de la vocal:'vocal' en el dominio de la frecuencia
                plt.subplot(noGrafica)
                plt.plot(xf, np.abs(yf),label=titulo)
                plt.legend()


            titulo_figura1='Señales en el tiempo, vocalista: '+vocalista_escuchar
            plt.figure(1).suptitle(titulo_figura1,fontsize=12)

            titulo_figura2='Tranformadas de las señales, vocalista: '+vocalista_escuchar
            plt.figure(2).suptitle(titulo_figura2,fontsize=12)

            plt.show()
            break
        except ValueError:
            print("Error: debes ingresar solo un numero")
        except IndexError:
            print("Error: ingresaste una opccion que no existe")


def graficarTodos():
    '''
    Muestra un ventana por cada vocal, dicha ventana contendra las
    graficas de las grabaciones de audio de cada persona que se grabo
    diciendo dicha vocal, la graficas estaran en el dominio del tiempo

    Aparte muestra un ventana por cada vocal, dicha ventana contendra las
    graficas de las grabaciones de audio de cada persona que se grabo
    diciendo dicha vocal, la graficas estaran en el dominio de la frecuencia
    '''

    # GRAFICARA LOS UNICOS 6 PRIMEROS...
    vocalista_str,vocalistas_list=getNombresVocalistas()

    if len(vocalistas_list)>2:
        for vocal in ['a','e','i','o','u']:
            print(f"Graficas de la vocal: ' {vocal} '.... ")

            for noVocalista,vocalista in enumerate(vocalistas_list[:6]):
                dir_vocalista=DIR_VOCALES+vocalista+'/'

                array,fs=getDatosSonido(dir_vocalista+vocal+'.wav')
                noMuestras=array.shape[0]
                ts=1/fs
                duracion=noMuestras*ts
                tiempo=np.arange(0,duracion,ts)
                normalized_array = np.int16((array/array.max()) * 32767)
                yf = rfft(normalized_array)
                xf = rfftfreq(noMuestras, 1 / fs)


                labelGraficas=vocalista
        
                plt.figure(1)
                # graficando en el dominio del tiempo
                noGrafica=321+noVocalista # 5 renglones 1 columna...   
                plt.subplot(noGrafica)
                plt.plot(tiempo,array,label=labelGraficas)
                plt.legend()

                plt.figure(2)
                # graficando en el dominio de la frecuencia
                plt.subplot(noGrafica)
                plt.plot(xf, np.abs(yf),label=labelGraficas)
                plt.legend()
            
            titulo_base="vocal ' {} '  ".format(vocal)
            

            titulo_figura1='Señal en el tiempo: '+titulo_base
            plt.figure(1).suptitle(titulo_figura1,fontsize=15)
            
            titulo_figura2='Transformada de la señal: '+titulo_base
            plt.figure(2).suptitle(titulo_figura2,fontsize=15)

            plt.show()


def grabarVocales():
    '''
    Mostrara una lista con los nombres de las personas que han decidio grabarse diciendo
    las vocales, posteriormente pedira el nombre de la persona que desea grabarse diciendo
    las vocales, una vez hecho lo anterior proseguira a hacer las grabaciones de las vocales
    y almacenarlas en una carpeta con el nombre de la persona que grabo dichas vocales, dicha
    carpeta se almacenara en la ruta: 'recursos/vocales/'
    '''

    frases_str,_=getNombresVocalistas()
    print("Vocalistas:")
    print(frases_str)
    print("ADVERTENCIA: Si ingresas un nombre de un vocalista ya existente, sus grabaciones se sobreescribiran")
    print()
    nombreVocalista=input('Ingresa nombre del vocalista: ')
    
    if os.path.isdir(DIR_VOCALES+nombreVocalista+'/'):
        rmtree(DIR_VOCALES+nombreVocalista)
    os.mkdir(DIR_VOCALES+nombreVocalista)
    
    dir_vocalista=DIR_VOCALES+nombreVocalista+'/'


    for vocal in ['a','e','i','o','u']:
        os.system ("cls")
        print("*********************************************")
        print(" Opccion elegida: Grabar vocales " )
        print("********************************************")
        print()
        print("VOCALISTA:",nombreVocalista)
        print("\nPRUEBA: AUDICION DE VOCALES")
        
        print("\n")
        print(f"INSTRUCCIONES: DURANTE 1.5 SEGUNDOS DECIR LA VOCAL......... {vocal}")
        print()
        grabarSonido(nombreSonido=dir_vocalista+vocal+'.wav',duracion=1.5)
        print()
        input("presionar enter para continuar...")

    os.system ("cls")
    print("*********************************************")
    print(" Opccion elegida: Grabar vocales " )
    print("********************************************")
    print("\n\n")
    print("PRUEBA DE AUDICION DE VOCALES FINALIZADA")
    print()
    print("Felicidades y hasta luego vocalista:",nombreVocalista)
    print()
    print()
    

##################################################################################################################
#   TONOS DTMF
##################################################################################################################

def generarSenal_conTonosDTMF():
    '''
    Pedira un cifra compuesta de 3 digitos, posteriormente obtendra la frecuencia
    que le corresponde a cada digito en funcion de los tonos DTMF, una vez obtenidas
    las frecuencias proseguira a hacer senoidales con esas frecuencias y posteriormente
    las sumara entre si, y finalmente obtendra las graficas de dicho resultado, dichas
    graficas son las siguientes:
        - Señal en el tiempo
        - Señal en la frecuencia
        - Densidad espectral de frecuencia de dicha señal
        - Señal en el tiempo y la frecuencia
        - Señal en el tiempo y densisdad espectral de potencia'

    TONOS DTMF:

    	        1209 Hz 1336 Hz	1477 Hz	1633 Hz
        697 Hz	  1	    2	    3	    A
        770 Hz	  4	    5	    6	    B
        852 Hz	  7	    8	    9	    C
        941 Hz	  *	    0	    #	    D

    FRECUENCIA QUE LE CORRESPONDE A CADA NUMERO:

        0=941+1477
        1= 697+1209
        2= 697+1336
        3= 697+1477
        4= 1209+1209
        5= 1209+1336
        6= 1209+1477
        7= 852+1209
        8= 852+1336
        9= 852+1477
        
    '''

    TONOS_DTMF=[
        941+1477,            # 0
        697+1209,            # 1
        697+1336,
        697+1477,
        1209+1209,
        1209+1336,
        1209+1477,
        852+1209,
        852+1336,
        852+1477,
    ]


    fs,senal=getArrayDatosTono(duracion=0.5,frecuencia_tono=100)

    while True:
        print()
        print("Ingresa tus tres ultimos digitos de cuenta:")
        tresDigitos_cuenta=input("R= ")
        senal=senal*0 #borrando los datos
        tituloGrafica='Tonos: '

        if 2<len(tresDigitos_cuenta)<4:        
            try:
                for digito_str in tresDigitos_cuenta[:3]:
                    digito_int=int(digito_str)
                    frecuencia_dtmf=TONOS_DTMF[digito_int]
                    _,tono_dtmf=getArrayDatosTono(duracion=0.5,frecuencia_tono=frecuencia_dtmf)
                    senal=senal+tono_dtmf
                    tituloGrafica+=digito_str+'='+str(frecuencia_dtmf)+'[Hz]  '

                noMuestras=senal.shape[0]
                ts=1/fs
                duracion=noMuestras*ts
                tiempo=np.arange(0,duracion,ts)

                normalized_senal= np.int16((senal/senal.max()) * 32767)
                yf = rfft(normalized_senal)
                xf = rfftfreq(noMuestras, 1 /fs)


                plt.figure(1).suptitle(tituloGrafica,fontsize=12)
                plt.title("Señal en el tiempo:")
                plt.plot(tiempo,senal)
                plt.show()

                plt.figure(2).suptitle(tituloGrafica,fontsize=12)
                plt.title("Señal en la frecuencia")
                plt.plot(xf, np.abs(yf))
                plt.show()


                plt.figure(3).suptitle(tituloGrafica,fontsize=12)
                plt.title("Densidad espectral de potencia")
                plt.psd(senal,512,fs)
                plt.plot()
                plt.show()


                plt.figure(4)
                plt.subplot(211)
                plt.title('Señal en el tiempo y la frecuencia')
                plt.plot(tiempo,senal)
                plt.xlabel('tiempo')
                plt.ylabel('amplitud')

                plt.subplot(212)
                plt.xlabel('frecuencia')
                plt.ylabel('amplitud')
                plt.plot(xf, np.abs(yf))
                plt.show()

                plt.figure(5)
                plt.subplot(211)
                plt.title('Señal en el tiempo y densisdad espectral de potencia')
                plt.plot(tiempo,senal)
                plt.xlabel('tiempo')
                plt.ylabel('amplitud')

                plt.subplot(212)
                plt.psd(senal,512,fs)
                plt.plot()
                plt.show()

                break

            except Exception as e:
                print(e)
        print()
        print("No ingresaste bien los datos....")


##################################################################################################################
#   MENU
##################################################################################################################

def mostrarMenu():
    '''
    Mostrara al usuario todas las acciones que puede realizar en el programa y posteriormente
    le preguntara al usuario que accion desea realizar
    '''

    os.system ("cls") 
    menu='''
*************************************
               MENU                  
*************************************
'''
    for noOpccion,opccion in enumerate(LISTA_OPCCIONES):
        menu+='        {}) {}         \n'.format(noOpccion+1,opccion)
    menu+='*************************************'
    menu=menu[1:] #Quitando el primer salto de linea del menu

    while True:
        opccionValida=False
        print()
        print(menu)
        opccionElegida=input("\nIngresa la opccion deseada: ")
        try:
            opccionElegida=int(opccionElegida)
            if 1<=opccionElegida<=NO_OPCCIONES:
                opccionValida=True
        except Exception as e:
            print("Error:",e)

        if opccionValida is False:
            print(f'''Error al escoger opccion,recuerda que:
            A) Solo hay {NO_OPCCIONES} opcciones posibles
            B) No se permiten letras como respuestas, solo
            numeros enteros''')
            #_=input("Presiona enter para continuar")
            input("Presiona enter para continuar... ")
            os.system ("cls") 
        else:
            return opccionElegida


def atenderOpccion(idOpccion):
    '''
    Realizara la accion elegida por el usuario y una vez finalizada, le preguntara
    al usuario si desea repetirla
    '''


    idOpccion-=1
    menu='''
*************************************
         OPCCION ELEIGIDA       
*************************************
'''
    for noOpccion,opccion in enumerate(LISTA_OPCCIONES):
        menu+='        {}) {}'.format(noOpccion+1,opccion)
        if noOpccion==idOpccion:
            menu+=" <=======\n"
            continue        
        menu+="         \n"

    menu+='*************************************'

    os.system ("cls")
    print(menu)
    print()
    print("¿La opccion marcada es la que realmente quieres?:\n")
    print("\t* Ingresa 1 si la respuesta es afirmativa\n")
    print("\t* Ingresa cualquier cosa diferente de 1 si\n"
        "\tla respuesta es negativa")
    estatus=input("\n\t R= ")

    if estatus=='1':
        while True:
            os.system ("cls")
            print("*********************************************")
            print(" Opccion elegida:{}".format( LISTA_OPCCIONES[idOpccion] ) )
            print("********************************************")
            print()
            
            if idOpccion==0:
                grabarFrase()
                pass
            elif idOpccion==1:
                graficarFrase()
                pass
            elif idOpccion==2:
                escuharFrase()
                pass
            elif idOpccion==3:
                grabarVocales()
            elif idOpccion==4:
                escuharVocales()
            elif idOpccion==5:
                graficarVocales()
            elif idOpccion==6:
                graficarTodos()
            elif idOpccion==7:
                generarSenal_conTonosDTMF()
            elif idOpccion==8:
                print("\n\nVuelve pronto n.n. \n\n")
                input("presiona enter para salir...")
                print("\n\n")
                sys.exit()

            print("")
            print("¿Deseas repetir la accion:{}?\n".format( LISTA_OPCCIONES[idOpccion] ) )
            print("\t* Ingresa 1 si la respuesta es afirmativa")
            print("\n\t* Ingresa cualquier cosa diferente de 1 si\n"
                "\tla respuesta es negativa")
            estatus=input("\n\t R= ")
            if estatus!='1':
                break


if __name__=='__main__':
    while True:
        opccionElegida=mostrarMenu()
        atenderOpccion(idOpccion=opccionElegida)


