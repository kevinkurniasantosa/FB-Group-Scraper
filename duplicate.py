import operator
import string
import numpy as np 
import time
import random

name = 'Lele'
name2 = 'Dumbo'
age = 20
age2 = 30
gender = 'Male'
gender2 = 'Female'
# array = []
x = 1
y = 2

dic1 = {
    "name": name,
    "age": age,
    "gender": gender
}

dic2 = {
    "name": name,
    "age": age,
    "gender": gender
}

dic3 = {
    "name": 'Jennifer',
    "age": '24',
    "gender": 'Female'
}

dic4 = {
    "name": 'Kevin',
    "age": '21',
    "gender": 'Male'
}

dic5 = {
    "name": name,
    "age": age,
    "gender": gender
}

dics=[dic1,dic2,dic3,dic4,dic5]

def test():
    array = []

    for x in range(len(dics)): # 0 - 4
        duplicate = 0
        print(len(array))
        if len(array) == 0: 
            array.append(dics[x]) # 
            print('Num of output (di if): ' + str(len(array)))
        else:
            print('Num of output (di else): ' + str(len(array)))
            for y in range(len(array)): 
                print('Testing duplicate on index ' + str(y))
                print('Is ' + str(x) + ' equal to ' + str(y) + '?')
                if dics[x] == array[y]:
                    print('Duplication detected')
                    duplicate = duplicate + 1
                else:   
                    # array.append(dic1)
                    print('Not duplicate') 

            print('Duplicate : ' + str(duplicate))
            if duplicate == 2: # IF DETECT DUPLICATES 2 TIMES
                print('DETECTED 2 TIMES - STOP THE LOOP')
                break
            else:
                array.append(dics[x])

        print(array)
        time.sleep(1)
        print('---------------')
    
    print('Final results: ' + str(array))
    print('success')

if __name__ == '__main__':
    test()
        
       


