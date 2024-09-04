def parallel(Ra,Rb):
    Rc = 1/(1/Ra+1/Rb)
    return Rc

R1, R2, R3, R4, R5, R6 = 50, 200, 75, 300, 125, 400


I = 10
I1 = I - I*(R2/(R2+R3+parallel(R4,(R5+R6))))
I3 = (I-I1)*(R4/(R4+R5+R6))
I2 = I-I1-I3
print('I1=',I1)
print('I2=',I2)
print('I3=',I3)