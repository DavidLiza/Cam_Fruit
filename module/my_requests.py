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

def API_verify ():
    print (CONS.bcolors.OKGREEN+"Api Verification"+CONS.bcolors.ENDC)

    return True

def __getImage():
    pass

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
    request_Frubana(
                    basekts     = 66 , 
                    product     ="product2", 
                    state       = "state2", 
                    num_pallets = 67 , 
                    pallets_id  = "palet2",
                    abs_weight  = 42 ,
                    final_weight= 36 , 
                    image=image)
                                       
def __thr_consume(): 
    bin_data = open('cache/limonsin.png', 'rb').read()
    image = bin_data


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


"""
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00U\x00\x00\x00k\x08\x06\x00\x00\x00\x06\x85\xce\x87\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00 cHRM\x00\x00z&\x00\x00\x80\x84\x00\x00\xfa\x00\x00\x00\x80\xe8\x00\x00u0\x00\x00\xea`\x00\x00:\x98\x00\x00\x17p\x9c\xbaQ<\x00\x00\x00\x06bKGD\x00\xff\x00\xff\x00\xff\xa0\xbd\xa7\x93\x00\x00\x00\x07tIME\x07\xe4\n\x1d\x05\x02 \xa6Q\xe4v\x00\x00\x00\x01orNT\x01\xcf\xa2w\x9a\x00\x00\x0e1IDATx\xda\xed\x9c{p[\xd5\x9d\xc7?\xe7J\xf2C\x96#\xc7J\xfc\xc0\x8f<l\x93l\ty,4\x0f\x02$3\xb4\x9d`\xb6\xc9\x96\xb6a\xfb"\x01:\xcc\xecn7\xb0\xcb.m\x93\x9dvf;\xbba)\x94\x920\x14f\x8a[J\xb3;\xd0\r\xd9\xb2y\xd0.)\t\x85\x840\x908\x0f\x8a\x13\xa7$v\xec\xc4\t~\xc8\xb6l\xd9\x96t\xcf\xfeq-\xe9\xca\x92l\xc9\xbe\xc7vw\xf4\x9d\x91}\xef\xd1\xb9\xe7\x9c\xdfG\xbf\xdfy\xe9^\t)\xa5$#K\xa5Mu\x03\xfe?*\x03U\x812P\x15(\x03U\x812P\x15(\x03U\x812P\x15(\x03U\x812P\x15(\x03U\x812P\x15(\x03U\x812P\x15(\x03U\x812P\x15(\x03U\x81\xecS\xdd\x80\xc9\x90\xec<\x00\xfe\xd3\xc8\xbeS`+@\xabzFi}b\xba\xef\xfc\xcb\xce\x03\xc8\xae}\xe0?\x05C\xcd\xc8\xc1\xe6X\x03\xb2+!\xab\x12ln\xc8\x9a\x03vw\xf4\xcd\xc1&\xa4w\x1f\x84\xbac\x0b\xb5\xb9\xd1\x16\xecC\xb8oQ\xd2\xe6i\x0bU6mC\xbf\xfal\x0c\x10\xd1\x0f\xd8@f[`x\xfe\xadh\x8b\xdeR\xd2\xf6i\x17\xfe\xb2\xe5q\xf4\xcb\xdb\xe3\xbdK\x07\xed\x92\x00\rB526\xfd\x8a@/K\xd37\x86\x9a\xd3\xcb\x9f\x86\xa6\x0f\xd4\xee#\x84.\xfc5\xf8O\'~_\x03\xbdD"B\t\xd2G\x00\x15\x01\x906F\x1f\x86\xb3*\x95\x992-\xa0\xca\x96\xc7\xd1/}g\xec|nH\xc5\x1f\xa5#\x85L\xf9\xb7)\xb3g\xca\xa1\xca\xc6o\xa0\xb7\xef\x02\x0c\x0f\x13\xd7\x04\xd2-\x91\xae\xf4\xca\x11\x03\x18\xfdm*@\x01\xe1\xbcQ\x99MS\n5T\xbf$6\xdc\xfbA\xf8\x86\xc1\xa4\x01U\xf4\x82vY ]\x12Y\x96\xe2E\xb6\x02evM\x19\xd48\xa0\x18\xe1\xad;\xa5\xd1\x1f\x8e\x90h\x07YH\xc2~R\xe6\x80tI\xc8M\xa3\x01CM\xcal\x9b\x12\xa8\xf2\xe3o%\x1d\x90\x92\x86\xaf\x03\x08\x91x\xf0q\x80\x9e\xaa\x87\x86\xeb\xe9?\x8dPd\xdf\xa4/S#\xf3\xcft\xafsc\x805+0\x81\x86x\xf7*\xb3qR&\xff\xe7\xdf\x7f\x97SG\x8f\x91\xe3\xe8 \xa7\xefE\xfc~;Z\x8f\xe0\xe6\xdb/S\xe8\x19P]}Ri\x0b\xf6!\n\xef\xb4\xbc\\\xe5P\x0f\xd4\xfd\x94\x9a%\x8b\xa8\xbei%\xa1\x0f\xe6F\'\xdd:\xa3\xc6\xc9\x8b\xfb%\'\x1ban)\xac\xbfM0\xb7\xd4\xfa\xb6\x89\xe2\xbfA\x9bo\xfd>\x80\xd2\xf0?\xb6\xff5\xee\xbc\xff\x9bT\xdf\xb4\x12\xd9\xf6|\xec*f\x8c\x9a\x0b\\\x825\xcb\x04n\x97\xe0\x81\x7f\x95\\\xbcb}\xfb\xe4\xf0T\xcejY\xee\xa9\xad\r\xa7\xd9\xfd\\\x1d\x00[~\xfcT$=\xc6KG6\xc2\x07d\xa7>\xc7\xb4\x14@\xc5ch\xe5\x8fZZ\xa6\xa5\xa3\xff\xb1\xfd\xaf\xb1\xeb\x89\x9dq\xe9q^j6j\x10\xb4V\x81\xb4\x83\xac\x8a\xfd|\x9b\xaeH\xe6\x94\xaa\x1a\xa3\x87\xe5\xdd\x0b\x16C\xb54\xfcw=\xb1\x93\xc5\xab\x96\xf3\xed\x9f\xfc\x88\xea\xc5\x8b"\xe9\xa3\x85\x99\xcc6\xd6\xf4rV,\xd0\x9b6K\xaa\xbe\x04;^Q;\x8e\xca\xfe\xd3\x13/d\x84&e\xf4\x0f\x1d\x1d\xfd\xb3\x1b\xec(A\xcb\x1e\xc0\xe1\xf2F\xd2\xec\xab\x8df-\xa9\x81\x0f~\xae\xd6[m\x9fz\x07\xdc\xab,+O\xf9<U\xb6=?f\x9e\xcb\xbf\xbb\x87\x0b\xbfz\x88\x8e\x13k#i/l\x13l\xb8\r\xea\xb6)\x0e\x7f@\xfaOYZ\x9ez\xa8]\xfb"\xc7"\xc9d\xfd\xba;^\xc6\xe1\xf2\xd2Q\xbf&\x02vS-\xec~L\xb0\xa4Fu\x0bA\x06\xbb\'^\x88I\xca\x97\xa9r\xd0Xc\x8bn\xd0\xda\x04\xbaG"g\xc5\xe6\xc9.l\xa3\xfc\xce\x17\xf1\xb7\xcdMiko,y{\xa1 ?\x8d\x0bB\xd6BU\xbfL\r\xaf\xf1\x1d \xed\x12r\x12gs\xb8\xbc\xcc\xa8\xae\xc7]]?\xe1*\x7f\xfd{c\xa0\xf3\xfa\x94[\x97P\x93\xb6\xf6\x97N\xd0\xabH{\x9ft<\xdaT\x0b[6\n\x1ey:5\xbf\x17\x13\xd9CH\xa0)\xfd\xde_\x8c\xb1\xeco=\xe7\xe2\xe0/\xca\xe9\xedHmUp\xb21\xba\xf2\xdaT\x0b\x87N\x90\x92\xb7\x8a\xa0{\xecLihJ\xa1\xca\x9c\xd1\xdfo=\x97G\xc3\xd1B\xf6<UE\xc3\xd1\x99\xa3\xe6\xdd\xf1\xb2\xe4\xa6\xcdp\xc7\xdfE\xc3\xben\xab\xa0`\x8c\xc8\x10\xdd\x80k\xb1\xa5vM\xeb;T\xf2\xddv\x8a\x8b\xca\xd0\x07fq\xf0\x17\x15\xa3z\xed\xc9F\xe3\x7f\xd3\x15\xe3\x05\xb0\xe6\xcf\xc7\xaeC\xf4\x08p\xc6{\xea\xab;\x9f\x06`\xf7\xce\x1d\x1cz\xe5?\xd3j\xb7\xf2\xd1_\xf4\x1b\xfd\xe9x\xb4pU\x17e\xda:d\xd0I\xc3\xd9z\xde?\xfa{Z\xcf\xb9X~\xd7U\x16\xae\xea\x8a\xc9\xfb\xbd\x07\x04\xee|\xc9\xdc\xd2\xd4\xa7a\xa2\x1f\x84\xee\x86\xc2\xd8\x89\xff\xa9\xc3\x079\xf6\xdb79u\xe4=\xfc\xbe>\xb6\xfc\xf0\x07\xd3\x0cjO\x01\xd2\xe9E\xe8@(\xbdM\x13a\xef\'\xb7\xfae\xfa\x1b\xeec\xe1\x82\xa5tz\xdb\x19\xb0\xbfO\xd9\xf5}qy\xe7\x94\xc2\x8f\x1eJo\xa1\xa0\xb5\t(\xb95.\xdd\xef\xeb\xc3\xdf\xd7G\xae+\x8f-?\xfc\x01e\x0b\xd3\xfb\x92P=T\xad\x12\xd1\xe5\xe5\xf0\x99\n\x0e\xbf[\xc9\xf7\x1e~\'-\xb0\x8e\xe2#\xe4\xbb\xcf\x12h_\xcam\xf3\xbaqU\xfe1.O\xc0W@O\xe3\x12\x9c%M\xe4\x96^L\xad]\x1d\xc2\xf8\xe6\xa0\xfc/\x12\xbc\t;~\xf7\xbf\xe3\xb6Y9\xd4\xf3\xbe%\xec\xdf\xeb\xa0\xb5;\x8f\xaf|\xe1\xa3\x84_\xea\x8d%-\xa7\x83\xec\xf2\x83$\xbb\xdb\xc7\x965@\xd7\x1fV\xd2Q\xbf\x16\xcf\xd2\xc3x\x96\x1d\x1a\xb5<\x11\x00\xad}\xf8d\xc1\x83\x91\xf4\x03u/PX2\x9b\x15\xb5\xeb\'d\xb3\xb2\r\x95\xd6\x86\xd3\xfc\xf2\xc9\x9d\xd4T\xe8,\xce\xdaCu\x85\x17\xbdB*\xdb3\r\xf8\nh9\xb0\x89\x80\xaf\x809\x1b\x9e\'\xbb\xb0-a\xbe\x81>;{^\xbd\x1eO\xf6\x00\x9e\xf2\x1a\xfa+\xee\xc5\xef3B}\xed\xc6\xafX\xd2\x16ePwm\xff7\xbe\xf6\xdd\xad\xd0\xf2:\xbcq\x97\x91\xe8@)X0\xe0\x9aw\xbbb\x8c\r\xdf\x8f5\x00\x9d\xbe\x1c\xa8}\x9b\xc2\xf9\xcb,o\x83\xb2)Uaq\x91qP\xbe\xced\xb1a\x94\xd5+\x18\xb3R\x01\nP\xb8\xf8n%@A1\xd4S\x87\x0f\x1a\'\xc5\xa6\x116\x00\xdaE\x81\xe8\x1a_\xb9\xe3\x91\x18\xae3\x0c\x94\xbcJ\xb8\xfd%e\xf5Y\nu\xc7\xc3\x7f\xcf/\xb7o\x07\xc0S\\\x84\xdf7<\xf5)\x1e1m\xd1A\xbb&\xd0\x9a\x04bP\x99m\x00\x88.a\x005G\xc7\xcd\x8f\xa9\xads\xbc}\xea\xd3\xfb.\x00\x02\xc2\x97\x0bA\xe7\xd5k4\x9e<\x83\xa7\xb8\x88\xb2\xaay\xf8}>\nK\x8a\xc0\xd7\x0c\xd7\xdeN^Xn\xa2~\xd6<\xe7\x94\xa6\xf3\x91\xc7\x89\xf2\x0f\xa7\xf8\x89\xbf\xe1\xc2\xe1\x86\n\xd34JJ\x10\x82y\xb3\xb3X\xbf\xfc\xba\xa9\x83\xfap]\x03\x17>\x19\x1a\xe6i4\xca\xdc\xc0\xa4,\xc2\xb6\x87\xd3M\x1fH4\xcd|\x8d9\x91\x98z\x84\x10\xc3\xa9\x12\xa4\x88\x96\'\x84\xa9\xe8\x11\x95\x9a\xebI\xd0\xc6o\xae\xf5\xb0~E\x9a\xf7\x0f%\xd0\xb8\xe6\xa9\xce,\x08\x85\x82\x08\x13\x05\x89\x1c>\x1f]\xd1|\xc3\xd7\r\x032\xe0\x98\r6\xa2 \x82E\x84\xeb0\xa4\x9b\xca\x14#\xbcXFj\x8aa\x1d)|$\xd7\xb0\xf2\xb2\xad\xf9\xeaf\xdc\xe1\xff\xf8K\xc7i\xb9\xe6\xe3\xdd3\xd7L&E=KD\x0c\x885!z$cR\xcc\xb0\x9398#J\x89\xfb\x80Fx\xa6H\x9a?z<#\xcf\xc1gWTP\xe2\xc9\xe5\xde\xda?\x9bZ\xa8\x00\r\x8d-|\xe1\x9f~\x13iw\xd8#\xa4\x1c\x11\xc9\xe6p\x16\x86w\x82\xe1}\x91\x10\x8f\xc4\xac\t\xa7\x08{\xab\x88\xf6*r\x84\x9f\x8d\xe6\\\xe6\xee(\x91{JX8o&{\x9e\xba\xdb\x12\x98aMh\x99\xba\xb0\xa6\x9c\xebJ\n\xe8\xf5\x87\x90\xc2\xf8\xe4\xa54u\x03\x11\xb2&\x0f\x8a\xe9&M@!\xd2\x15\x18\xff\xc3o\x8b\xc8{\x11\x86\xc3\x7fb\xd3\x04R\xd7\xd1\x03Cq\x1f,\x98\xc3?\xb6\x9f^Z\xe3\xb1\x14\xe8\x84\xa1\x02lX;\x9f_\x1dnM\x9e\xc1l\x19&\x90)\xe7\x1f\xed}\xb3\x97\x83>\xe4G\n[Z\x05~u]\xf5D\x11\xc4i\xc2\xf3\xd4-\x7f\xb5\x0cW\xae=\x9e\x930\xb1\x13\xe6s\x11{>\xf2\x95\xa8\x13\x15\t\xce\xcd\x07\x12dp\x08\x19\x0c \x84\x88y\x01qi\xc6K\xa3vu%5\xf3\'>\xda[\x0e\x15\xe0\xfe\xda\xb9F\xc8\x0b\x11\x03@\xc4\x0c\x15\xa6.\x01\x92;\x8f\x10\xf1\x1fF\x1c\xcc\xd8\x0fB\x86\x02\xc8\xc0@\xccl\xce\\\\"\xb9\x9cv\xfe\xf9A5O\xa8X\x02\xf5\xcb\x9fY\xc8\xba\xe5\xc5q\x16\xc7s3\xd1\x12\x89\xdc8\x9d4a\xf4\xe1\x81A\xe4\x90\x7f\xd4\xbc"A][7\xabY\xf7[\x06\x15`\xeb\xe6\x9b\xa9)u"\x86\x8b\x14\x11\xdf\x14q\x1e\x1b5M\x8bK7\x9b\x1e=\x161\xe9\x02@J\xf4\xc1>d`h\x18\\t02\x8e\xcdi\x98\xc0\xc2\x03\xeb\x17\xb0f\xb9\xf5}i\xc4\x16\xab\xb7\xfe\xb6>{\x84\xb7\xcfxM)#\x97R\xe6\xe3h\x9a\x8c\xc0K\x94\xc7T\x8e\x04\x19\x1cD\x86\x02\xc3\xd3\xabD\xcdOt\xad\x91\xb6u\xf3Rj\xd7X3\x1f\x9d4\xa8\x00u{\xea\xf9\xd9\xeb\x17\x11\xb6,\xeb\n\xd5\x83F\xdf\x19\nF\x97\xb7#\x8d\x11I\xdf\xa2\xd4\xe3d\xfb\xdf\xdeL\xf5<k\xd6\xf7\xa3I\xe9\xad\x94_~t/m]\x83\x08\x9b\x034[L\x08\x86e^\xfe\xc7\xa4\xeb\xba\x01R\xd7M^IdI\x1b\xbd.z\x9ehP\x92\x126\xde1\x8f-__\xa1\x1c\xe6\xa4@\x058\xf0V\x03?\xdb{\x8e+\xed~\x03\x80\xd0\x86_"\xd6\xb5\xc2\xff\xf5\x90\xb1\xdc\xb4\xa0Y\xcb\xae\xf7p\xdf\xe7kXv\xc3\x1c\xe5 \xcdR\xfe\xc5\xdf\x9d\xb7/\xe4\xea\xd5v\x9e\xdb}\x8a\x9e>\xc5\x9b\xa7&\xadX\\\xc6\x8e\xef|f\xd2\xea3K\xb9\xa7\xee\xf8\xf9Av\xfc\xc7\xb1)1n\xc5\x8de\xeczr\xd3\xa4\xd7\xab\xfc\xb6\x9f\xa9\x02\np\xect+\x7f8{q\xd2\xebU\xe2\xa9\'\xce\\\xe4\xe5\x83\x17\xb8\xfc\x89\x8f\x8f\xfe\xd8>\xbeB\x12-Y\xc7\xd1\xd2O\xcd\x9fE\xbe+\x9bR\x8f\x93m\x0f\xde\x9a~\x01\xe3i\xba\xd5P_x\xf5\x03\xea^;7)\x8dOW\xa5\xb3\x9c\xfc\xd7\x13\x1b\x94\xd7c9\xd4\xd5\x9bS\xbfCNJ\x1d\x7f\x7f/\xa1`\x10)\xf5\x94\xaf\x03\x10B\xc3f\xb7\x93\x9d\x93\x87\xcd\x96\xfax\xbbl\x81\x87g\xbe\xfb9+M\x8e\x93\xa5\xa3\xff\xfe\xc3\x1fE\x0b\xce\xc9\xc3\x9e\x9d\xcb`OgB`}\xbd]\xf8z\xbd\x13\xae\xb3\xb7\xbb\x93\xdc\\\x17\xf9n\x0fB\x1b{\x888q\xb6\xc3J\x93\x13\xcaR\xa8\x8d\xcd=\x91c\x87s\x06Bh\x08\xbb\x03\x19\x88\x9dJ\xf5\xf6t\xd0\xef\xeb\xa1\xb8h\x06\xf7n\\\xc5\xd2\x1b\xc6\xf7#1m\x9ft\xf3\xdb7?\xe47o~H 0\x84\xa7(\xb5m\xbc\xc6\x8f[\x95l\xf9\x85e-\xd4\x16\xe3)\x0f\xa1\x19\xfb\x95\x002\x18\xfb\x1d\xb1\xbf\xbf7\x02\xf4\xf9\'\xeeeQ\xc9\x8c\xf1WX5\x9b\r+\xab\xf9v^6\xbb\xf7\x1e\xc7\xd7\xdb\x85+\x7f\xe6\x98\x975^\xeaQ\n\xd5\xd2)U\xe3%\xc3S\xc3k~)\xf5\xb8\xd0\x1f\xf0\x1b\xf7\x8e?\xfa\xaduI\x81v\xbf\xf80]\xaf|?r\xde\xf1?O\xd1\xfb\xdc}\xb44%\x1e\x00\xbfq\xcf-\xb8\xf2\xb2\xe9\xf7\xf5\x90\x8a\x1a\x9b\xad}\xc4g\xa4,\x83\xda\xf8\xf1e|\xfd\x86W\x86\xd7\xf8z(\xfe\xa6\xa9@`\x08\x80\r+\x13o\xbd}\xf2F\x1dz\xae\x1b{g3m\'\xde\x00 \xf7\xf4^\xfaV|\r\xf7\x81\xed\t\xafYT<\x83\xd5\x9f\xaeFJ\x9dP(8v[[R\x83?^Y\x16\xfeW:\xfa#\xc7\x9am\xf8v\x13=~b!u\x9d\xe2\xa2\xe4!o\xefl"Xh\xac\xd5m\x1d\xcd\xb445\xe2.\xac$X8\x07[g\xf2_=\x0b\x97)u\x1d\xc6\xb8\x076\x1cQ\xaad\x9d\xa7\x9aBJ\xd8\r\xa8zp(.\xdfX#\xb4\x9e\xebF\xf3{\xd1\xfcFy\x9a\xdf\x8b\xad\xb3\x19\xcd\xefE\xe6&\x7f4\xc7\xd7o\x0c\x86\xa9L\xaf\xc2\x11\xa5J\xd6AM\x10Rz\x82Pt\xd8\xb3\xb8z\xad\x87_\xbf{>a9\x9e\xcf\xff\x03\xf6\xceft\xa7\x9b\xa1\xf2\x1b\xb1u6\xe3_|\x17\xf9\x87\x9e\xa5\xeb\xee\x7fOZ\xff;\xef\x9d\xc7f\xb3\xa74\xad\x02x\xeb\xbd\xf3)\xe5\x1b\x8f,\x0b\xff\xb6v\x7f\xe48\xd0\xd7M\xd0\xdf\x8b\x1e\x8c\xf7\x88\xbc\xfc\x99\x0cu\\\xe1\xf1g^\xa7x\xf6FVV\x15\xc5\xe5qo\xfa1\x00\xc68\xfe\xe9Hz\xb2\xc7M\xff\xe5\xa7\x87\xb8z\xad\x87\x19\x05\xb3So\xaf\xa9\xbb\xb2Z\x96Am\xbc\x14\r\x7f\xa9\x87\x90z(a\xbe\xac\xec\x1c\xf2\xf2gr\xf5Z\x17\x8f|\xff\x15V/\xaf\xa6jn\xea0\xcc\xf2\xf5\rq\xe4\xbd\xf3\x9c\xfc\xf0\x12\xce<7\xb9\xce\xd4\x9f\xd1<\xa7\xb0_\xb5\x04\xea\xf13\xe9\xfd\x1a\x99+\xbf\x00\x9b\xcdF{\x87\x97W\xf7\x1e\x9fP\xddBh\xe4\xbb=8\xf3\xd2\x9b\xef\xd6\x9fS\xb7\xb2\xb2\x04\xaa\xd9KSU\xae3\x9f\\g>C\x83\x03)M\x83\x12\xc9f\xb3\xe3\xc8\xca\x8a,4\xd2\xd1\x95\xf6i\x1e\xfe\xe6\xfe4]ee\xe7\x8c\xfb\xda\x89J\xd5r\xd5\x92\xd1\xff|\x8b\xda\x15\x8a*\xa9\x9a\xafZ\x13\xfe\xa3\xacP6\xde1\x9f\x9aJk\x1f\xfdNU\'\xce\xb6\xf3V}[\xd2y\xa9\xaa.\xc0\x12\xa8\xf99\x0ez\xfbb\x1b\xeer:x\xe6\x1fW)\xdd\xb8\x18K\xb5k`\x1b\xf0\xc5G\xfe\x9b\xb6\x8e\xf8.\xaat\xd68\x9fD\x1eC\x96\x84\xff\x97>;/.\xed\xa1{n\x98R\xa0f\xed~\xf2/q9c\x9f\xd4\xa8\xae\x98\xa1\xecN\x15\xcbv\xfe\x8f\x9fib\xff\x11cm~\xd7-\x95,[4\xb9\xdf\xb5\xa7\xa2\xa7_:F\xaf\x7f\x88\xeb<y\xdc\xff\xc5\x14~\x0c`\x9c\x9a\xb6\xbf\xf3\xff\xa7\xaci\xfd\xcb\x14\x7f\xaa\xca@U\xa0\x0cT\x05\xca@U\xa0\x0cT\x05\xca@U\xa0\x0cT\x05\xca@U\xa0\x0cT\x05\xca@U\xa0\x0cT\x05\xca@U\xa0\x0cT\x05\xca@U\xa0\x0cT\x05\xfa?"KL>\x9e\x1c\xa9\xa2\x00\x00\x00%tEXtdate:create\x002020-10-29T05:02:28+00:00\x08\xac\xe9\x99\x00\x00\x00%tEXtdate:modify\x002020-10-29T05:02:28+00:00y\xf1Q%\x00\x00\x00\x00IEND\xaeB`\x82'
"""