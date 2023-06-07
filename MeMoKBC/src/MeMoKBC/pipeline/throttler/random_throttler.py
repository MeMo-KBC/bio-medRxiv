from random import randint

def throt_rand(c):
    '''randomly returns True or False'''
    #print(c[0].context.get_span())
    if c[0].context.get_span() in c[1].context.get_span():
        return True
    else:
        return False

    # if randint(0, 10) >= 8:
    #     return False
    # else:
    #     return True