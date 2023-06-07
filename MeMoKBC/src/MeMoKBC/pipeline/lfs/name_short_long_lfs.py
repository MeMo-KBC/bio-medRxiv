from fonduer.utils.data_model_utils.visual import get_page_vert_percentile
from snorkel.labeling import labeling_function

ABSTAIN = -1
FALSE = 0
TRUE = 1

@labeling_function()
def name_short_outside_half_percentile(c):
    '''Checks if name short is in the lower half of the document'''
    matcher_name_short = c[0]
    short_vert_percentile = get_page_vert_percentile(matcher_name_short)
    if short_vert_percentile >= 0.5:
        return TRUE
    else:
        return ABSTAIN
 
 
@labeling_function()
def name_full_in_top_percentile(c):
    '''Checks if name long is in the top percentile of the document'''
    matcher_name_full = c[1]
    full_vert_percentile = get_page_vert_percentile(matcher_name_full)
    if full_vert_percentile <= 0.25:
        return TRUE
    else:
        return ABSTAIN
    

@labeling_function()
def word_count(c):
    '''Checks if name short has less than or equal to 8 letters'''
    name_short = c[0]
    short_string = name_short.context.get_span()
   
    if len(short_string) <= 8:
        return TRUE
    else:
        return ABSTAIN
    

@labeling_function()
def small_letter_count(c):
    '''Checks if name short has less than or equal to 2 small letters'''
    name_short = c[0]
    name_short_string = name_short.context.get_span()
    lowercase_count = sum(1 for w in name_short_string if w.islower())

    if lowercase_count <= 2:
        return TRUE
    else:
        return ABSTAIN


@labeling_function()
def check_all_uppercase_letters(c):
    '''Checks if all name short uppercase letters are in name long'''
    name_short = c[0]
    name_long = c[1]
    
    short_string = name_short.context.get_span()
    long_string = name_long.context.get_span() 
    
    uppercase_set = set(char for char in long_string if char.isupper())

    letters = ''.join(char for char in short_string if char.isalpha() and char.isupper())


    for letter in letters:
        if letter not in uppercase_set:
            return ABSTAIN
    
    return TRUE



short_long_lfs = [
    name_short_outside_half_percentile,
    name_full_in_top_percentile,
    word_count,
    small_letter_count,
    check_all_uppercase_letters
]