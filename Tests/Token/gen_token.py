import jwt

encoded_jwt = jwt.encode({'some':'payload'}, 'Identica' , algorithm= 'HS256' )
print (encoded_jwt)

decoded = jwt.decode(encoded_jwt, 'Identica' , algorithms=['HS256'] )
print (decoded)

