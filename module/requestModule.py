# -*- coding: utf-8 -*-
__author__ = "Sebastian Estupiñan"
__copyright__ = "Copyright 2019, Ojo Biometrico"
__credits__ = ["Sebastian Estupiñan"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "David Lizarazo "
__email__ = "dlizarazo@identica-sa.com"
__status__ = "Development"


import requests
import requests.exceptions


try:
    import module.log as log
    import module.constants as CONS
except:
    import log 
    import constants as CONS

__logger = log.configure_logger('default')
__URL = 'http://192.223.10.244:40000'
__AUTH = '/api/authNU'
__API = '/api'


def __getApi(token, clientId, id, email, company, message, image):
    headers = {'content-type': 'application/json; charset=utf-8',
               'x-access-token': token}
    if image is None:
        json = {'email': email,
            'clientId': clientId,
            'serviceId': '53',
            'data': {
                'id': id,
                'company': company,
                'message': message,
                'biometrics': '1'
	    }}
    else:
        json = {'email': email,
            'clientId': clientId,
            'serviceId': '53',
            'data': {
                'id': id,
                'company': company,
                'message': message,
                'biometrics': '1',
		'image':image
            }}

    try:
        response = requests.post(__URL + __API, json=json, headers=headers)
        if 200 <= response.status_code <= 299:
            data = response.json()
            __logger.debug(data)
            #print (data)
            return data
        else:
            print('{} {}'.format(response.status_code, response.json()))
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        __logger.error("Exception occurred", exc_info=True)
        return None


def __getToken(**kwargs):
    headers = {'content-type': 'application/json; charset=utf-8'}
    json = {}
    for key, value in kwargs.items():
        json[key] = value

    try:
        response = requests.post(__URL + __AUTH, json=json, headers=headers, timeout=None)
        if response.status_code == 200:
            data = response.json()
            __logger.debug(data)
            return data
        else:
            __logger.error("OJE002 {}".format(response.status_code))
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        __logger.error("OJE003", exc_info=True)
        return None


def __getTest():
    headers = {'content-type': 'application/json; charset=utf-8'}
    json = {'serial': '866224035710382',
            'formato': '42',
            'company': 'Identica SA',
            'message': 'Esta es una prueba desde la funcion get_test',
            'biometrics': '1'}
    response = requests.post('http://192.168.1.6:40003/api/request2', json=json, headers=headers)
    if response.status_code == 200:
        data = response.json()
        __logger.debug(data)
    else:
        __logger.error(response.status_code)

def requestCT(id, email, password, company, message, image=None):
    tokenResponse = __getToken(email=email,password= password)
    if tokenResponse is not None:
        apiResponse = __getApi(tokenResponse['token'], tokenResponse['user']['clientId'], id, email, company, message, image)
        if apiResponse is not None:
            return apiResponse
    return None

if __name__ == '__main__':
    __getTest()
    #requestCT('1019128590', 'pruebas@identica.com', 'identica', 'Identica SA', 'Esta es una prueba de texto ')
