def parallel(Ra,Rb):
    Rc = 1/(1/Ra+1/Rb)
    return Rc

R1, R2, R3, R4, R5, R6 = 50, 200, 75, 300, 125, 400

R40 = parallel(R4,(R5+R6))
R20 = parallel(R2,(R3+R40))


V = 10
V1 = V * (R20 / (R1+R20))
V2 = V1 * (R40 / (R3+R40))
V3 = V2 * (R6 / (R5+R6))
print('V1=',V1)
print('V2=',V2)
print('V3=',V3)
