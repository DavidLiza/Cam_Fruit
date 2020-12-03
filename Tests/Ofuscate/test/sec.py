
def liza ():
    x = "ala"
    if x == "ala":
        print ("Yeap compar")
    try :
        raise Exception(123)

    except Exception as e:
        print (e)
        print (type(e))
        y = e.args
        if y[0] == 123:
                print ("Fuck Yeah")

if __name__ == "__main__":
    liza()