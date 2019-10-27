# Jeffrey Zhong
# monty hall game show problem simulation 


import random 


A = 'A'
B = 'B'
C = 'C'

doors = [A, B, C]


def simulate_stay(trials):
    """ 
    simulates if a computer stays on its door 
    """
    x = trials 
    win = 0 
    lose = 0 
    while x > 0:
        prize = random.choice(doors)
        selection = random.choice(doors) 
        if prize == selection: 
            win += 1 
        else: 
            lose += 1 
        x += -1
    print ("Win:" , win/trials*100,"%", " Lose:", lose/trials*100,"%")

def simulate_switch(trials):
    """ 
    simulates if a computer switches its door 
    """
    x = trials 
    win = 0 
    lose = 0 
    chose = [A, B, C]
    pick = [A, B, C]
    while x > 0:
        prize = random.choice(doors)
        selection = random.choice(doors)
        chose.remove(prize)
        if prize != selection:
           chose.remove(selection)
        elif prize == selection: # you lose :(
            chose.remove(random.choice(chose))
        reveal = chose[0]
        pick.remove(reveal)
        pick.remove(selection)
        if prize == pick[0]:
            win += 1 
        else: 
            lose += 1 
        x += -1
        chose = [A, B, C]
        pick = [A, B, C]
    print ("Win:" , win/trials*100,"%", " Lose:", lose/trials*100,"%")

def user_tries(): 
    """
    allows user to play the game
    """ 
    prize = random.choice(doors)
    vA = '[A]'
    vB = '[B]'
    vC = '[C]'
    visual = vA + ',' + vB + ',' + vC
    print (visual) 
    selection = input('Pick a Door: ')
    if selection == 'A':
        vA = '[X]'
        visual = vA + ',' + vB + ',' + vC
    elif selection == 'B':
        vB = '[X]'
        visual = vA + ',' + vB + ',' + vC
    elif selection == 'C':
        vC = '[X]'
        visual = vA + ',' + vB + ',' + vC
    print(visual)
    chose = [A, B, C]
    pick = [A, B, C]
    chose.remove(prize)
    if prize != selection:
           chose.remove(selection)
    elif prize == selection: 
        chose.remove(random.choice(chose))
    reveal = chose[0]
    if reveal == 'A':
        vA = '[ ]'
        visual = vA + ',' + vB + ',' + vC
    elif reveal == 'B':
        vB = '[ ]'
        visual = vA + ',' + vB + ',' + vC
    elif reveal == 'C':
        vC = '[ ]'
        visual = vA + ',' + vB + ',' + vC
    print('I will reveal a door that does not have a prize in it ... ')
    print(visual)
    move = input('Do you Keep or Change doors: ')
    if move == 'Keep':
        if selection == prize: 
            print('You Win!')
        else: 
            print('You Lose.')
    elif move == 'Change': 
        pick.remove(reveal)
        pick.remove(selection)
        if prize == pick[0]:
            print('You Win!')
        else: 
            print('You Lose.')
    else: 
        print('HEY! You should have typed in Keep or Change')



if __name__ == "__main__":
    print('Monty Hall Simulation')
    print('')
    trials = int(input('Amount of Trials: '))
    if trials == 1:
        user_tries()
    else:
        print('')
        print('Simulate Staying With Your Orginal Door: ')
        simulate_stay(trials)
        print('')
        print('Simulate Switching Doors: ')
        simulate_switch(trials)


