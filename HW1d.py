def parallel(Ra,Rb):
    Rc = 1/(1/Ra+1/Rb)
    return Rc
j = (-1)**0.5

Z1, Z2, Z3, Z4, Z5, Z6, Z7 = 20, j*100, 30, -1*j*150, 40, j*200, 100

Zab = Z1+parallel(Z2,(Z3+parallel(Z4,(Z5+parallel(Z6,Z7)))))
print('Zab=',Zab)
