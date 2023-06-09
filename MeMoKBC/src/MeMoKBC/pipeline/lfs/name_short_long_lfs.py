from fonduer.utils.data_model_utils.visual import get_page_vert_percentile
from snorkel.labeling import labeling_function

ABSTAIN = -1
FALSE = 0
TRUE = 1

@labeling_function()
def name_short_outside_half_percentile(c):
    '''Checks if name short is in the lower half of the document'''
    name_short, name_full = c
    try:
        short_vert_percentile = get_page_vert_percentile(name_short)
    except:
        print(c)
        return ABSTAIN
    if short_vert_percentile >= 0.5:
        return TRUE
    else:
        return ABSTAIN
 
 
@labeling_function()
def name_full_in_top_percentile(c):
    '''Checks if name long is in the top percentile of the document'''
    name_short, name_full = c
    full_vert_percentile = get_page_vert_percentile(name_full)
    if full_vert_percentile <= 0.25:
        return TRUE
    else:
        return ABSTAIN



def get_page_vert_perc_by_sentence(mention):
    '''Returns the vertical percentile of a mention by sentence'''
    sentence = mention.context.sentence
    sentences = mention.context.sentence.document.sentences
    return sentences.index(sentence) / len(sentences) 

@labeling_function()
def name_short_outside_half_percentile_sentence_wise(c):
    '''Checks if name short is in the lower half of the documents sentences'''
    name_short, name_full = c
    try:
        short_vert_percentile = get_page_vert_perc_by_sentence(name_short)
    except:
        print(c)
        return ABSTAIN
    if short_vert_percentile >= 0.5:
        return TRUE
    else:
        return ABSTAIN
    

@labeling_function()
def name_full_in_top_percentile_sentence_wise(c):
    '''Checks if name long is in the top percentile of the document'''
    name_short, name_full = c
    full_vert_percentile = get_page_vert_perc_by_sentence(name_full)
    if full_vert_percentile <= 0.25:
        return TRUE
    else:
        return ABSTAIN


@labeling_function()
def word_count(c):
    '''Checks if name short has less than or equal to 8 letters'''
    name_short, name_full = c
    short_string = name_short.context.get_span()
   
    if len(short_string) <= 8:
        return TRUE
    else:
        return ABSTAIN
    

@labeling_function()
def small_letter_count(c):
    '''Checks if name short has less than or equal to 2 small letters'''
    name_short, name_full = c
    name_short_string = name_short.context.get_span()
    lowercase_count = sum(1 for w in name_short_string if w.islower())

    if lowercase_count <= 2:
        return TRUE
    else:
        return ABSTAIN


@labeling_function()
def check_all_uppercase_letters(c):
    '''Checks if all name short uppercase letters are in name long'''
    name_short, name_full = c
    
    short_string = name_short.context.get_span()
    long_string = name_full.context.get_span() 
    
    uppercase_set = set(char for char in long_string if char.isupper())

    letters = ''.join(char for char in short_string if char.isalpha() and char.isupper())


    for letter in letters:
        if letter not in uppercase_set:
            return ABSTAIN
    
    return TRUE



short_long_lfs = [
    # name_short_outside_half_percentile,
    name_short_outside_half_percentile_sentence_wise,
    # name_full_in_top_percentile,
    name_full_in_top_percentile_sentence_wise,
    word_count,
    small_letter_count,
    check_all_uppercase_letters
]