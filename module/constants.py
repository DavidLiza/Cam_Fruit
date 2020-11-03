#! /usr/bin/python3.0

def __getserial():
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = None
  return cpuserial


# ID device
IDevice = __getserial()
# QR reader connected using SerialCable or USBcable ('s' o 'u')
QR_READER = 's'


# Local Data base
DB_OWNERS = 'eye_access.db'
DB_DATA   = 'location_info.db'

DB_CONTENEDORES = "contenedores.db"

#SUPER USER 
ID_SUPER  = 674178

class bcolors:
    #Colors
    HEADER = '\033[95m'  # MAGENTA
    OKBLUE = '\033[94m'  # BLUE
    OKGREEN = '\033[92m' # GREEN
    WARNING = '\033[93m' # YELLOW
    FAIL = '\033[91m'    # RED
    CIAN = '\033[96m'    # CIAN
    
    #Instructions
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
