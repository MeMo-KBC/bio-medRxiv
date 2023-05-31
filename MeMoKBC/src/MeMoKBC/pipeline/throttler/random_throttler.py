from random import randint

def throt_rand(c):
    '''randomly returns True or False'''
    if randint(0, 10) >= 8:
        return False
    else:
        return True