# Jeffrey Zhong 
# dicerolling.py
# Physics C: Lab One 

import random 

def roll(N):
    """
    simulates a roll of N 6-sided dice
    """
    dice = random.randint(1+(N-1),6*N)
    return dice 


def test(X,N):
    """ 
    performs roll(N) X amount of times and takes the average
    """ 
    sum = 0
    for num in range(X): 
        dice = roll(N)
        sum += dice
        num += 1 
    average = sum/X
    return average 

def data(): 
    """
    """
    for x in [1,2,3,10,100,671,1000]: 
        print( '(' + str(x) +','+ str(test(1000000,x)) +')') 


"""
results: 
(1,3.498764)
(2,7.001625)
(3,10.497964)
(10,35.007703)
(100,350.13176)
(671,2350.882926)
(1000,3501.422762)
""" 

