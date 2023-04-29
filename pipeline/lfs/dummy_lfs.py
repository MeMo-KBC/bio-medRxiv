from snorkel.labeling import labeling_function
from random import randint

ABSTAIN = -1
FALSE = 0
TRUE = 1


@labeling_function()
def dummy_lf_rand(c):
    if randint(1, 10) <= 5:
        return TRUE
    else:
        return FALSE

@labeling_function()
def dummy_lf_rando(c):
    if randint(1, 10) <= 5:
        return TRUE
    else:
        return FALSE
    
@labeling_function()
def dummy_lf_randi(c):
    if randint(1, 10) <= 5:
        return TRUE
    else:
        return FALSE


dummy_lfs = [
    dummy_lf_rand,
    dummy_lf_rando,
    dummy_lf_randi
]