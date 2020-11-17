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
SENSORS   = True
N_SENSORS = 6


# Local Data base
DB_CONTENEDORES = 'eye_access.db'
DB_WIFI  = 'device.db'



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
