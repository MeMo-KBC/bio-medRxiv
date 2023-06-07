from snorkel.labeling import labeling_function


ABSTAIN = -1
FALSE = 0
TRUE = 1

@labeling_function()
def lf_length_more_than_three_words(c):
    sentence = c[1].context.get_span().split(" ")
    if len(sentence) > 3:
        # print("1")
        return ABSTAIN
    else:
        # print("2")
        return FALSE

@labeling_function()
def lf_name_short_in_first_words(c):
    name = c[0].context.get_span()
    sentence = c[1].context.get_span().split(" ")
    i = 1
    for word in sentence:
        if name.lower() == word.lower(): # was ist mit sonderzeichen? word stemmen und vergleichen?
            if i <= 3:
                # print("3")
                return TRUE
            else:
                # print("4")
                return ABSTAIN
        i+=1   
    return ABSTAIN



short_task_lfs = [
    lf_length_more_than_three_words,
    lf_name_short_in_first_words,
]