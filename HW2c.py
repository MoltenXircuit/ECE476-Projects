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

code = '2234'
guess = inputGuess()
score = checkGuess(code,guess)
print(guess,score)