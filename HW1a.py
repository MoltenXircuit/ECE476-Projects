def parallel(Ra,Rb):
    Rc = 1/(1/Ra+1/Rb)
    return Rc

R1, R2, R3, R4, R5, R6 = 50, 250, 75, 300, 200, 450

Rab = R1+parallel(R2,(R3+parallel(R6,(R4+R5))))
print('Rab=',Rab)



