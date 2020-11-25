# -*- coding: utf-8 -*-
__author__ = "David Lizarazo"
__version__ = "1.0.0"

import requests
import base64
import codecs
import requests.exceptions

try:
    import module.log as log
    import module.constants as CONS
except:
    import log 
    import constants as CONS

__logger = log.configure_logger('default')
__URL = 'https://federate-public-services.federate-dev.frubana.com/ops-mvps/perfect-arrive'
__AUTH = '/api/authNU'
__API = '/api'


def __setImage(token, image):

    headers = {'content-type': 'image/png' }
    if image is None:   return None

    try:
        my_url = __URL+'/image/'+token
        response = requests.post( my_url , 
                                data=image, 
                                headers=headers)

        if 200 <= response.status_code <= 299:
            data = response.json()
            print (data)
            return data
        else:
            print('{} {}'.format(response.status_code, response.json()))
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        print(CONS.bcolors.FAIL+"Exception occurred"+CONS.bcolors.ENDC)
        return None

def __getToken(**kwargs):
    headers = {'content-type': 'application/json; charset=utf-8'}
    json_send = {}
    for key, value in kwargs.items():
        json_send[key] = value

    try:
        response = requests.post(__URL , json=json_send, headers=headers )

        if response.status_code == 201:
            data = response.json()
            #__logger.debug(data)
            return data
        else:
            #__logger.error("REQ_ERROR {}".format(response.status_code))
            return None
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        #__logger.error("REQ_ERROR", exc_info=True)
        return None


def request_Frubana(    basekts, product, state, 
                        num_pallets, pallets_id,
                        abs_weight,final_weight, image=None):

    tokenResponse = __getToken( device= CONS.IDevice, #CONS.IDevice
                                baskets=basekts,
                                product=product,
                                state=state,
                                pallets_number=num_pallets,
                                pallets_id= pallets_id,
                                total_weight= abs_weight,
                                calculated_weight = final_weight) 

    if tokenResponse is not None:
        apiResponse = __setImage(tokenResponse["data"]["uuid"], image)
        print (apiResponse)

        if apiResponse is not None:
            return apiResponse
    return None

# --- Test ----

def __getTest():
    headers = {'content-type': 'application/json; charset=utf-8'}
    json_send ={
            'device': 'device2',
            'baskets': 56,
            "product": "product2",
            "state": "state2",
            "pallets_number": 45,
            "pallets_id": "palet2",
            "total_weight": 1.5,
            "calculated_weight": 1.8
        }

    response = requests.post(__URL,
                             json=json_send, 
                             headers=headers)

    print (response)

    if response.status_code == 201:
        data = response.json()

        print (data)
        print ("UUID DE DIFERENTES FORMAS")
        print (data["data"])
        print (data["data"]["uuid"])
        
    else:
        pass

def __ex_consume():
    with open('cache/limonsin.png', 'rb') as file:
        image = file.read()
        image = base64.b64encode(image)  
        print (image)

        request_Frubana(
                        basekts     = 66 , 
                        product     ="product2", 
                        state       = "state2", 
                        num_pallets = 67 , 
                        pallets_id  = "palet2",
                        abs_weight  = 42 ,
                        final_weight= 36 , 
                        image=image)
                    
def __sec_consume():
    
    bin_data = open('cache/limonsin.png', 'rb').read()
    image = bin_data
    #image = codecs.encode(bin_data, "hex_codec")
    #hex_data = bin_data.encode('hex')
    
    print (image)

    request_Frubana(
                    basekts     = 66 , 
                    product     ="product2", 
                    state       = "state2", 
                    num_pallets = 67 , 
                    pallets_id  = "palet2",
                    abs_weight  = 42 ,
                    final_weight= 36 , 
                    image=image)
                    



if __name__ == '__main__':
    #__getTest()
    #__ex_consume()
    __sec_consume()

    #requestCT('1019128590', 'pruebas@identica.com', 'identica', 'Identica SA', 'Esta es una prueba de texto ')
