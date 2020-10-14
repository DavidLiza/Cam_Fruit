import math

#--Test de distancias:
# https://www.sunearthtools.com/es/tools/distance.php
#--Fórmula del Haversine
# https://www.genbeta.com/desarrollo/como-calcular-la-distancia-entre-dos-puntos-geograficos-en-c-formula-de-haversine
# haversin(phi) = sin² ( phi/2 )
# a = sin²(Δlat/2) + cos(lat1) · cos(lat2) · sin²(Δlong/2)
# c = 2 · atan2(√a, √(1−a))
# d = R · c

def sindeg(val_grad):
   return math.sin( math.radians(val_grad) )

def cosdeg(val_grad):
   return math.cos( math.radians(val_grad) )

def atandeg(val_grad):
   return math.atan( math.radians(val_grad))

print ('Seno y coseno de 90')
print (sindeg(90))
print (cosdeg(90))

latitud_i = 4.6923724
longitud_i= -74.0655476

latitud_f = 4.69227
longitud_f= -74.06592

# Diferencias
dif_lat = latitud_i  - latitud_f
dif_lon = longitud_i - longitud_f
# Radio de la tierra en metros
radioT = 6371 * 1000
# Variables para la ecuacion
sin_lat =  sindeg( (dif_lat/2) )
sin_lon =  sindeg( (dif_lon/2) )

a_constant= (sin_lat**2) + (cosdeg(latitud_i) * cosdeg(latitud_f) * (sin_lon**2) )

c_constant = 2 * math.atan2( math.sqrt(a_constant) , math.sqrt(1-a_constant)  )

distance = radioT * c_constant

print ('Valor de distancia {}'.format(distance))
