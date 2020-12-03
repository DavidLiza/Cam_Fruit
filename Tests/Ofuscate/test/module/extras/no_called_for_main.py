x = "ala"
if x == "ala":
  print ("Yeap compar")
try :
     raise Exception(123)

except 123:
    print ("Funciona")
except Exception as e:
     print (e)
     print (type(e))
     y = e.args
     print (e.args[0])
     print (y[0])
     if y[0] == 123:
             print ("Fuck Yeah")


