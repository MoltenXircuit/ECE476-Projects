from random import randrange

def randCode(code,min,max):
    newcode = ""
    for digit in range(len(code)):
        newcode += str(randrange(min,max+1))
    return(newcode)

def inputGuess():
    while(1):
        print('please input a 4 digit code')
        guess = input()
        if (len(guess) == 4):
            return(guess)
    
def checkGuess(code,guess):
    correct = 0
    for x in range(len(code)):
        if (guess[x] == code[x]):
            correct+=10
        else:
            if (guess.count(code[x]) > 0):
                correct+=1
    return correct

#-----------------main code section--------------
code = '1244'
attempts = 0
code = randCode(code,0,5)
while(1):
    guess = inputGuess()
    score = checkGuess(code,guess)
    print('guess:','score:')
    print(guess,'    ',int(score))
    attempts +=1
    if (score == 10*len(code)):
        break


print('number of attempts = ',attempts)