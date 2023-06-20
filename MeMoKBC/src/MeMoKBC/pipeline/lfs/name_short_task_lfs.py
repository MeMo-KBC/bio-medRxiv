from snorkel.labeling import labeling_function

ABSTAIN = -1
FALSE = 0
TRUE = 1

@labeling_function()
def lf_length_more_than_three_words(c):
    name_abbr, task = c
    sentence_span = task.context.get_span()
    sentence_tokenized = sentence_span.split(" ")
    if len(sentence_tokenized) > 3:
        # print("1")
        return ABSTAIN
    else:
        # print("2")
        return FALSE

@labeling_function()
def lf_name_short_in_first_words(c):
    name_abbr, task = c
    name = name_abbr.context.get_span()
    sentence = task.context.get_span().split(" ")
    if name.lower() in " ".join(sentence[:3]).lower():
        return TRUE
    else:
        return ABSTAIN

@labeling_function()
def lf_check_surr_chars(c):
    name_abbr, task = c
    name_span = name_abbr.context.get_span()
    sentence_span = task.context.get_span()
    char_left = sentence_span.index(name_span) - 1
    char_right = char_left + len(name_span) + 2
    chars = []

    if char_left > 0:
        chars.append(sentence_span[char_left])
    if char_right < len(sentence_span):
        chars.append(sentence_span[char_right])

    for char in chars:
        if char not in [" ", ","]:
            return FALSE
        
    return ABSTAIN

name_abbr_task_lfs = [
    lf_length_more_than_three_words,
    lf_name_short_in_first_words,
    # lf_check_surr_chars
]