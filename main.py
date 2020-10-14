#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "David Lizarazo"
__copyright__ = "Copyright 2010"
__credits__ = ["David Lizarazo"]
__version__ = "1.0.0"
__maintainer__ = "David Lizarazo"
__email__ = "davidlizarazovesga@hotmail.com"
__status__ = "Development"

from time import sleep
import os
import log
import base64
import Cython
import signals as signals              #For the threads creation 
import signal                          #Used to enable the key interrupt.
import py_compile                      #To enable wich file must be compile 
import threading                       #To create threads
from   datetime import datetime        #To get the moment when QR is scanned
import module.decodeModule      as decM    #To desencipt the QR information 
import module.gpioModule        as LEDS    #To enable and play GPIOS connected
import module.requestModule     as Flow    #To make the request to the servers
import module.databaseConsume   as SQL     #To consum the database 
import module.pidFileGen        as PID     #To get the number of the task thats doimg the process

_logger = log.configure_logger('default')
_logger.info('Started Task : {}'.format(PID.ret_pid()))
#PID.save_PID()

# TODO: Verificar si la camara se encuentra conectada


####################################################################################
# Estas variables deben cambiar cuando se consulta por primera vez la base de datos 
####################################################################################

face_counter    = 1
stop_for_frame  = threading.Lock()
stop_for_sc     = threading.Lock()  
folder_location = os.path.abspath(os.path.dirname(__file__))
py_compile.compile(os.path.join(folder_location ,os.path.basename(__file__)))




def keyboardInterruptHandler(signal, frame):
    print('KeyboardInterrupt (ID: {}) has been caught. Cleaning up...'.format(signal))
    _logger.info('Interrupt catched')
    try:
        LEDS.GPIO_PROC_OFF()
        LEDS.SALUTE_QR('ADIOS')
    except:
        print('Camera Destruction DONE before')
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)
signal.signal(signal.SIGTERM, keyboardInterruptHandler)

"""
    ***** **    *****  **** ****
    **    **    **  *  ***  ***
    **    **    *****     *    *
    ***** ****  **  *  **** ****
"""

class ThreadForSecondCamara(threading.Thread):

    def __init__(self, group=None, target=None, name=None):
        super().__init__(group=group, target=target, name=name)

        global face_counter
        self.__running  = True
        self.__camAval  = False
        self.__rotation = 180
        self.__width    = 640  #720
        self.__height   = 480  #480
        self.__path     = os.path.join(os.path.abspath(os.path.dirname(__file__)),'Personas_escaneadas')
        try: 
            if cameraCV.isOpened():
                self.__camAval = True
        except:
            print('No second Camara Found')

    def run(self):
        with stop_for_sc:        #Bandera de decoding para saber que se tomo la foto
          global face_counter
          if self.__camAval:
            with stop_for_frame: #Bandera de re configuracion de la camara 
               cameraCV.set(3,self.__width)
               cameraCV.set(4,self.__height)

               sleep(0.1)
               self.__ret, self.__frame = cameraCV.read()
               self.__frame =cv2.flip(self.__frame,self.__rotation)
               self.__img_name = 'face_{}.jpg'.format(face_counter)
               self.__final_dir = os.path.join(self.__path, self.__img_name)
               cv2.imwrite(self.__final_dir, self.__frame)
               cameraCV.set(3,320)
               cameraCV.set(4,240)
               sleep(0.1)
            self.__running = False
            face_counter += 1
          else:
             self.__running = False
             _logger.error('No second Camera Avaliable')

    @property
    def is_running(self):
        return self.__running


class ThreadForSounds(threading.Thread):

  def __init__(self,group=None,target=None,name=None,action=None, nameID ='Unicornio'):
     super().__init__(group=group,target=target,name=name)
     self.__nameID   = nameID 
     self.__action   = action
     self.__isrunning= False

  def run(self):
    self.__isrunning=True
    if self.__action == 'read':          # QR detected
      LEDS.GPIO_READ()
      self.__isrunning=False
      return
    if self.__action == 'val':          # HIT
      LEDS.GPIO_ACCEPTED()
      LEDS.SALUTE_QR(self.__nameID)
      self.__isrunning=False
      return
    if self.__action == 'init':         # INIT SOUND
      LEDS.GPIO_INIT()
      self.__isrunning=False
      return
    if self.__action =='noval':         # NO HIT
      LEDS.GPIO_REJECT()
      self.__isrunning=False
      return
    if self.__action == 'config':      # GPIO CONFIGURATION
      signals.Camara_frame.send(__name__) 
      LEDS.GPIO_CONF(LOGIC_ON='LOW')   #LOW for LEDs with comun ctode
      LEDS.SALUTE_QR('IdEntica S.A!')
    self.__isrunning=False

  @property
  def is_running(self):
    return self.__isrunning

"""
 ___
|      __   _ _   __   _   __
|     |__| | v | |__| |_\ |__|
|___  |  | |   | |  | | \ |  |
"""


class ThreadForFrame(threading.Thread):
   def __init__(self, group=None, target=None, name=None):
      super().__init__(group=group, target=target, name=name)
      global cameraCV
      self.__cam         =cameraCV
      self.__width       =320  #320
      self.__height      =240  #240 
      self.__framerate   =15
      self.__brightness  =62
      self.__contrast    =80
      self.__saturation  =3
      self.__sharpness   =90

      self.__isrunning = False
      self.__QRFound   = False
      self.__rotation  = 1
      self.__destruir  = True
      
   def run(self):
      
      if self.__cam is None or not self.__cam.isOpened():
        print ('Warning: Unable to open video source : ', self.__camPort)
        self.__del__()
        return
          
      #'CONFIGURACION DE CAMARA'
      self.__cam.set(3,self.__width)
      self.__cam.set(4,self.__height)
      self.__cam.set(5,self.__framerate)    #framerate#print(cameraCV.get(5))
      self.__cam.set(10,self.__brightness)  #brightness 60
      self.__cam.set(11,self.__contrast)    #contrast 70
      self.__cam.set(12,self.__saturation)  #Saturation (Blanco y negro) 0
      self.__cam.set(20,self.__sharpness)   #Sharpens 90
      sleep(5)

      signals.Sounds.send(__name__, action='init')
      print ('Configurado ...')

      temp='.'

      while self.to_terminate:
        with stop_for_frame:
          algo,frame = self.__cam.read()
          frame =cv2.flip(frame,self.__rotation)
          decodeObjects= pyzbar.decode(frame,symbols=[ZBarSymbol.QRCODE])
          try: #Importante la primer linea del Try
             qr_value=decodeObjects[0].data
             self.__qrfound = True
             signals.Decoding.send(inputqr=qr_value)
             #signals.Sounds.send(action='read')
          except Exception as e:
             self.__qrfound = False
      self.__isrunning = False

      self.cam_destruction()


   def __del__(self):          
      self.__destruir  = False 

   def cam_destruction(self):
         try:
            if self.__cam.isOpened():
               print("Camara destruida")
               self.__cam.release()
         except:
            print  ("Camera disconnected before call.")

   @property
   def to_terminate(self):
       return self.__destruir

   @property 
   def is_running(self):
     return self.__isrunning

   @property
   def QR_FOUND(self):
     return self.__QRFound

""" __
   |  \   __   __   __   _   __
   |   | |__  |    |  | | \ |__
   |__/  |__  |__  |__| |_/ |__
"""


class ThreadForDecoding(threading.Thread):
   def __init__(self, group=None, target=None, name=None,inputqr=None):
      super().__init__(group=group, target=target, name=name)
      self.__isrunning = False
      self.__qrsound   = False
      self.__inputqr   = inputqr
      self.__EMAIL     ='pruebas@identica.com'
      self.__PASSWORD  ='identica'
      self.__COMPANY   ='Identica SA'
      self.__MESSAGE   ='Autorizacion Match Persona'

   def time_scanned_hit(self):
      self.__now      = datetime.now()
      self.__qr_now   = self.__decode["fecha"]
      self.__dif_tim  = ((self.__now.year*10   - int(self.__qr_now[0:4])*10)   +  
                         (self.__now.month*10  - int(self.__qr_now[5:7])*10)   + 
                         (self.__now.day*10    - int(self.__qr_now[8:10])*10)  + 
                         (self.__now.hour*10   - int(self.__qr_now[11:13])*10) + 
                         (self.__now.minute - int(self.__qr_now[14:16])))
      self.__hit_time = False
      if  abs(self.__dif_tim) <= 1 : 
            self.__hit_time = True
      return self.__hit_time 
      

   def location_hit(self):
      self.__hit_loc = False
      self.__lat     = float(self.__decode["latitud"])
      self.__lon     = float(self.__decode["longitud"])
      if abs(self.__lat-Lat_fix)<Tol_Lat and abs(self.__lon-Lon_fix)<Tol_Lat:
          self.__hit_loc = True
      else:
         _logger.info('OJL000:{},{}'.format(self.__lat,self.__lon))
      return self.__hit_loc

   def run(self):
     global qr_temporal
     global face_counter
     self.__isrunning = True

     if self.__inputqr == None :
        print ("No QR passed")
        return 

     if qr_temporal != self.__inputqr: # Avoid multiple sounds to happen (Save the last QR) 
        signals.Sounds.send(__name__, action='read')
        qr_temporal=self.__inputqr
        self.__decode=decM.decodeModule(self.__inputqr)
        
        if not self.time_scanned_hit() and not self.location_hit() :
           signals.Sounds.send(action='val',nameID='Fuera de! Rango!')
           return

        if self.__decode != None :
            qr_value=self.__decode["id"] ## Borrarlo 
            try:
                flow_response=Flow.requestCT(self.__decode["id"],self.__EMAIL,self.__PASSWORD,self.__COMPANY,self.__MESSAGE)
                print (flow_response)
                if flow_response['code'] == 'TRANS000' :
        	        signals.Authentication.send(__name__,inputflow=flow_response) 
                return 

            except Exception as e:
                #_logger.info('OJE001 : {}'.format(flow_response['code']))
                print ('Process Error Decode, error : {}'.format(e))
                
     self.__qrsound   = False

   def __del__(self):
       self.__isrunning = False

   @property 
   def is_running(self):
     return self.__isrunning

   @property
   def qr_sound (self):
     return self.__qrsound 


"""
   --        ___  __
  |==|  |  |  |  |__
  |  |  |__|  |  |__
"""

class ThreadForAuthentication(threading.Thread):
   def __init__(self, group=None, target=None, name=None,inputflow=None):
      super().__init__(group=group, target=target, name=name)
      self.__isrunning = False
      self.__inputflow = inputflow
      self.__iduser    = self.__inputflow['message']['id']
      self.__EMAIL     ='pruebas@identica.com'
      self.__PASSWORD  ='identica'
      self.__COMPANY   ='Identica SA'
      self.__MESSAGE   ='Autorizacion Match Persona'


   def run(self):
      self.__isrunning = True
      if self.__inputflow['code']=='TRANS000':
         response_from_id = self.__inputflow['message']['authentication']['response']
         if response_from_id=='HIT':

         ##############################################################
         ## Consumo de base de datos 
         ## Cambiarlo a que consuma un servicio para la base de datos
         ##############################################################

            self.__database=SQL.DataBaseConsumption(databasename=folder_location+'/Module/kike') 
            self.__dataUser=self.__database.get_entrance(IdScanned=self.__iduser)
            if not self.__dataUser:
                 self.__dataUser=self.__database.get_entrance(IdScanned=self.__iduser,Authorized=False)
                            
                 if not self.__dataUser:
                    signals.Sounds.send(action='val',nameID='Usuario No Encontrado')
                    _logger.info('Usuario {} no encontrado en base de datos'.format(self.__iduser))
                 else:
                    signals.Sounds.send(action='val',nameID='Bienvenido!  '+self.__dataUser[0][0])
                    _logger.info('HIT CC:{} , SQL:{}'.format(self.__iduser,self.__dataUser))
                    # Accion de abrir puerta
                 return
          ###############################
          # FIN DE CONSUMO DE BASE DATOS
          ###############################

            signals.Second_Cam.send(__name__)
            _logger.info('HIT CC:{} , SQL:{}'.format(self.__iduser,self.__dataUser))
            signals.Sounds.send(action='val',nameID='Hola! '+self.__inputflow['message']['nombre1'] ) 
                      
            with stop_for_sc:   # Pausa hasta que se tome la foto a la persona.
                 pass

            with open(folder_location+'/Personas_escaneadas/face_{}.jpg'.format(face_counter-1), 'rb') as file:
                image = file.read()
                image = base64.b64encode(image)   
                Owner_response=Flow.requestCT(self.__dataUser[0][1],self.__EMAIL,self.__PASSWORD,self.__COMPANY,'Solicitud de ingreso : {}'.format(self.__dataUser[0][0]),image=image)
                if Owner_response['code']=='TRANS000':
                    response_from_owner = Owner_response['message']['authentication']['response']
                    if response_from_owner=='HIT':
                        signals.Sounds.send(action='val',nameID='Bienvenhiido!') 
                        _logger.info('Accesos autorizado')  
                    else:
                        signals.Sounds.send(action='val',nameID='Inthente! NuEevamente')    
                elif Owner_response['code']=='MCD005':
                    signals.Sounds.send(action='val',nameID='Autoizacion Denegada')
                    _logger.info('Autorizacion Denegada')
                else:
                    signals.Sounds.send(action='val',nameID='Comuniquece con su Aanfiitrihon!')
                    _logger.info('Anfitrion con ID access cerrado {}'.format(Owner_response['code']))

         else:  # No HIT
            _logger.info('OJL002')
            signals.Sounds.send(__name__, action='noval')
            signals.Sounds.send(action='val',nameID='Intente Nuevamente!')
            LEDS.GPIO_REJECT()

         pass
         ##########################################################
         # Revisar una bandera si se ha modificado la base de datos DE LOS PROPIETARIOS UNIAMENTE
         ##########################################################
         self.__dbflag = False
         if self.__dbflag :
            # Obtener los valores nuevos de la base de datos 
            # Llamar funcion de sqlite3 que actualice los datos 
            pass
         # Termina actualizacion de los datos     

      elif self.__inputflow== None:
         signals.Sounds.send(action='val',nameID='Dispositivo Desconectado!')
         self.__database=SQL.DataBaseConsumption(databasename=folder_location+'/Module/kike') 
         self.__dataUser=self.__database.get_entrance(IdScanned=self.__iduser)
         if not self.__dataUser:
              self.__dataUser=self.__database.get_entrance(IdScanned=self.__iduser,Authorized=False)
                            
              if not self.__dataUser:
                 signals.Sounds.send(action='val',nameID='Usuario No Encontrado')
                 _logger.info('Usuario {} no encontrado en base de datos'.format(self.__iduser))
              else:
                 signals.Sounds.send(action='val',nameID='Bienvenido!  '+self.__dataUser[0][0])
                 _logger.info('HIT CC:{} , SQL:{}'.format(self.__iduser,self.__dataUser))
                 # Accion de abrir puerta
              return


         #########################################
         # Llamar autenticacion para propietario
         #########################################
                       
      else:
         signals.Sounds.send(__name__, action='noval')
         _logger.info('OJE001 : {}'.format(self.__inputflow['code']))
       

   def __del__ (self):
     #print ("Authenbtiucation is DEAD ")
     self.__isrunning=False
       
   @property 
   def is_running(self):
     return self.__isrunning
  
""" __    __
   |  \  | _\
   |   | |<_
   |__/  |__/ 
"""

class ThreadForDataBase(threading.Thread):
   def __init__(self, group=None, target=None, name=None):
      super().__init__(group=group, target=target, name=name)
      self.__isrunning = False
      self.__database = 'eye_access'
      
   def run (self) : 
      pass
      # Si esta conectado a la red continua , sino envia mensaje sonoro
      # Si existe IDlocation en Owner SUPER USER , continua , sino entra a la dsiguiente consulta
        # Funcion de si existe un ID de dispositivo relacionado con IDlocation en MYSQL ojo ( EL ID DE DISPOSITIVO QUE SE ENCUENTRE EN UN DOCUMENTO QUE SE CONSULTARIA )
        # Obtiene y guarda en IDlocation dicha vairbale obtenida de la base de datos 
      # Si el numero de modificacion de la base de datos local no coincide con la ultima guardad en MYSQL entra a lo siguiente , sino contiua 
	# Obtiene los datos de la tablaMIXTA  de MYSQL seleccionando los que coincidan por IDlocation 



"""
   |\  /|   --   _____  _ 
   | \/ |  |==|    |    |\ |
   |    |  |  |  __|__  | \|
"""

class QR_Reader_CT:

   def __init__ (self):
      signals.Sounds.connect        (self.init_sounds)
      signals.Camara_frame.connect  (self.frame_capture)
      signals.Decoding.connect      (self.frame_decoding)
      signals.CamError.connect      (self.__del__)
      signals.Second_Cam.connect    (self.sec_cam)
      signals.Authentication.connect(self.authentication)
      self.init_sounds(__name__, action='config')

   def __del__(self):
      self.__disconnect()

   def init_sounds(self,sender, **kwargs):
      self.__thread_for_sounds = ThreadForSounds(action=kwargs['action'],nameID=kwargs['nameID'] if 'nameID' in kwargs else None)
      self.__thread_for_sounds.setDaemon(True)
      self.__thread_for_sounds.start()

   def frame_capture(self,sender):
      try:
        self.__thread_for_frame = ThreadForFrame()
        self.__thread_for_frame.setDaemon(True)
        self.__thread_for_frame.start()
      except Exception as e:
        print('Error_Ocurred frame_capture {}'.format(e))
        _logger.info('OJE004-FC : {}'.format(e))


   def frame_decoding(self,sender,**kwargs):
      #try:
        self.__thread_for_decoding = ThreadForDecoding(inputqr=kwargs['inputqr'])
        self.__thread_for_decoding.setDaemon(True)
        self.__thread_for_decoding.start()
      #except Exception as e:
      #  print('Error_Ocurred frame_decoding {}'.format(e))

   def authentication(self,sender,**kwargs):
      try:
        self.__thread_for_authen = ThreadForAuthentication(inputflow=kwargs['inputflow'])
        self.__thread_for_authen.setDaemon(True)
        self.__thread_for_authen.start()
      except Exception as e:
        print('Error_Ocurred authentication {}'.format(e))
        _logger.info('OJE004-AU : {}'.format(e))


   def sec_cam(self,sender):
      try:
        self.__thread_for_faces = ThreadForSecondCamara()
        self.__thread_for_faces.setDaemon(True)
        self.__thread_for_faces.start()
      except Exception as e:
        print('Error_Ocurred sec_cam {}'.format(e))
        _logger.info('OJE004-SC : {}'.format(e))
      

   def __disconnect(self):

       try:
         if self.__thread_for_authen is not None and self.__thread_for_authen.is_running:
            self.__thread_for_authen.join()

         if self.__thread_for_decoding is not None and self.__thread_for_decoding.is_running:
            self.__thread_for_decoding.join()

         if self.__thread_for_faces is not None and self.__thread_for_faces.is_running:
            self.__thread_for_faces.join()
       except:
         print('No decodign process done')
       
       if self.__thread_for_sounds  is not None and self.__thread_for_sounds.is_running:
          self.__thread_for_sounds.join()

       if self.__thread_for_frame is not None and self.__thread_for_frame.is_running:
          self.__thread_for_frame.__del__()
          self.__thread_for_frame.join()

       if cameraCV .isOpened():
           cameraCV .release()

def main():
    kike = QR_Reader_CT()
    while True:
       pass

if __name__ == '__main__':
    main()
