def inputGuess():
    while(1):
        print('please input a 4 digit code')
        guess = input()
        if (len(guess) == 4):
            return(guess)

guess = inputGuess()
print(guess)
