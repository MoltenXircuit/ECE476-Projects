from random import randrange

def randCode(code,min,max):
    newcode = ""
    for digit in range(len(code)):
        newcode += str(randrange(min,max+1))
    return(newcode)
code = '1234'
print(code)
code = randCode(code,0,5)
print(code)