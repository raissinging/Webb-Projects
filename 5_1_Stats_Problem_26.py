# Number 26 page 303 in The Practice of Statistics Fith Edition For the AP Exam

import random 

def generate():
    lotto = []
    actual = []
    while len(lotto) < 6:
        num = random.randint(1,49)
        num = str(num)
        if num not in lotto:
            lotto.append(num)
    while len(actual) < 6:
        num = random.randint(1,49)
        num = str(num)
        if num not in actual:
            actual.append(num)
    #print (lotto,actual)
    for x in range(0,6):
        if lotto[x] == actual[x]:
            return 'True'
    return 'False' 

def test(trials):
    common = 0 
    for x in range(trials):
        check = generate()
        if check == 'True':
            common += 1 
    print(common,trials)
    print(common/trials*100, '%') 
        



