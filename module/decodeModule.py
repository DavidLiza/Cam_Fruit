#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = "David Lizarazo"
__version__    = "1.0.0"

from base64 import b64decode
from Crypto.Cipher import AES
import json

try:
    import module.log as log
    import module.constants as CONS
except:
    import log 
    import constants as CONS


logger = log.configure_logger('default')
key = b"Identica6045500*"


def __decodeBase64(data):
    try:
      return b64decode(data)
    except:
      print("Wrong QRs Type")
      return None


def __decrypt(data):
    decipher = AES.new(key, AES.MODE_ECB)
    return decipher.decrypt(data)

def decodeModule(data):

    decodedVar= __decodeBase64(data)
    if decodedVar != None :
      _dec =json.loads(__decrypt(decodedVar).decode("utf-8").replace("'", '"').split('}')[0] + '}')
      #logger.info('QR detected  {}'.format(_dec['id']))
      return _dec

    else :
      return None

if __name__ == '__main__':
    value = "quFjn+6qxFoyKi1i0ZCcdSn9aH+C0IZjsx+qn08q35FfoXKzIIMsXRKrQti2kAwP2fst275Ac3JNzezT1ljJPnGFsagOOw5BYxMLFqFtvNhYhz8y4dhTbbbP/wnS6nd5k40twFng2Lc4kdQ+nR2lsQ=="
    logger.debug(decodeModule(value))
