import serial

print("Proccess Started")
with serial.Serial('/dev/ttyAMA0', 9600 ,timeout=10) as ser:
#with serial.Serial('/dev/serial0', 9600 ) as ser:
    ser.reset_input_buffer()
    ser.flush()
    
    
    #ser.write(b'12 ')
    #ser.write(b'12 \n')
    #print("Read ASAP:  {}".format(ser.read(ser.in_waiting)))
    while True:
        print("Read ASAP:  {}".format(ser.read()))
    
    #x = ser.read()          # read one byte
    s = ser.read(65)        # read up to ten bytes (timeout)
    #line = ser.readline()   # read a '\n' terminated line
    b = ser.read_all()
    #c = ser.readall()

#print("x : {}".format(x))
print("s : {}".format(s))
print("s : {}".format(s.decode("utf-8")))
#print("line : {}".format(line.decode("utf-8")))

print("b : {}".format(b))
print("b : {}".format(b.decode("utf-8")))

# cuenta de ahorros, # 50632127704


#x = ser.read()          # read one byte
#s = ser.read(65)        # read up to ten bytes (timeout)
#line = ser.readline()   # read a '\n' terminated line
#b = ser.read_all()
#c = ser.readall()
#self._serial.in_waiting


#yPO6cSaIQTpTkCnIqeIPLMnkkXQ1gytlXGBSoismMiZBRPfAm9ctalPr4AiujPpC