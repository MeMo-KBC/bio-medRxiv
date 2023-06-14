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

## ideen für mehr lfs


# NameAbbTask
# copy from name_short_long lfs and add task mention
@labeling_function()
def candidate_mentions_outside_half_percentile(c):
    '''Checks if name short is in the lower half of the document'''
    matcher_name_short = c[0]
    matcher_task = c[1]
    short_vert_percentile = get_page_vert_percentile(matcher_name_short)
    if short_vert_percentile >= 0.5 and matcher_task >= 0.5:
        return TRUE
    else:
        return ABSTAIN

# mögliche fehlerquellen
# Abkürzung ist keine Namensabkürzung einer Person
# ist es möglich, auf nameshortlong- candidaten zuzugreifen und zu prüfen ob es einen long name zu dem kurzel gibt? - falls nicht -> false?


# NameShortLong



dummy_lfs = [
    candidate_mentions_outside_half_percentile,

]
