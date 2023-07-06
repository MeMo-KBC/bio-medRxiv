from snorkel.labeling import labeling_function
from random import randint
from pathlib import Path
import csv
import re

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
'''
@labeling_function()
def lf_name_short_in_first_words(c):
    name_abbr, task = c
    name = name_abbr.context.get_span()
    sentence = task.context.get_span().split(" ")
    if name.lower() in " ".join(sentence[:3]).lower():
        return TRUE
    else:
        return ABSTAIN
'''
@labeling_function()
def lf_name_short_in_first_words(c):
    name_abbr, task = c
    name = name_abbr.context.get_span()
    sentence = re.sub(r'[^\w\s]', '', task.context.get_span())
    first_words = re.findall(r'\b\w+\b', sentence)[:3]

    for word in first_words:
        if word.isupper() and word == name:
            return TRUE
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

@labeling_function()
def is_medical_abbreviation(c):
    name_abbr, task = c
    name_span = name_abbr.context.get_span()

    with open(f'{str(Path(__file__).parent)}/CSVs/all_abbs.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        medical_abbreviations = [row[0].lower() for row in reader]
    
    with open(f'{str(Path(__file__).parent)}/CSVs/Orga_abb.csv', 'r') as csvfile:
        reader_orga = csv.reader(csvfile)
        orga_abbreviations = [row[0].lower() for row in reader_orga]

    
    if name_span.lower() in medical_abbreviations or orga_abbreviations:
        return FALSE
        #print("FALSE")

    return ABSTAIN
    #print("ABSTAIN")


@labeling_function()
def name_in_task(c):
    name_abbr, task = c
    sentence = task.context.get_span()
    if name_abbr.context.get_span() in sentence:
        return TRUE
    else:
        return FALSE


@labeling_function()
def sentence_beginning(c):
    name_abbr, task = c
    sentence = task.context.get_span()
    if sentence.startswith(name_abbr.context.get_span()):
        return TRUE
    else:
        return ABSTAIN
    

@labeling_function()
def common_verbs_following_abbr(c):
    common_verbs = [
        "did",
        "conducted",
        "prepared",
        "performed",
        "developed",
        "designed",
        "created",
        "wrote",
        "edited",
        "reviewed",
        "analyzed",
        "evaluated",
        "interpreted",
    ]
    name_abbr, task = c
    sentence = task.context.get_span()
    sentence_tokenized = sentence.split(" ")
    if name_abbr.context.get_span() in sentence_tokenized:
        index = sentence_tokenized.index(name_abbr.context.get_span())
        if index + 1 < len(sentence_tokenized):
            if sentence_tokenized[index + 1] in common_verbs:
                return TRUE
        
    return ABSTAIN


@labeling_function()
def verbs_ending_with_past(c):
    name_abbr, task = c
    sentence = task.context.get_span()
    sentence_tokenized = sentence.split(" ")
    if name_abbr.context.get_span() in sentence_tokenized:
        index = sentence_tokenized.index(name_abbr.context.get_span())
        if index + 1 < len(sentence_tokenized):
            if sentence_tokenized[index + 1].endswith("ed"):
                return TRUE
        
    return ABSTAIN


@labeling_function()
def word_before_abbr(c):
    words_before = [
        "the",
        "a",
        "an",
        "this",
        "that",
        "these",
        "those",
    ]

    name_abbr, task = c
    sentence = task.context.get_span()
    sentence_tokenized = sentence.split(" ")
    if name_abbr.context.get_span() in sentence_tokenized:
        index = sentence_tokenized.index(name_abbr.context.get_span())
        if index - 1 >= 0:
            if sentence_tokenized[index - 1] in words_before:
                return FALSE
    return ABSTAIN


@labeling_function()
def abbr_is_complete(c):
    name_abbr, task = c
    name = name_abbr.context.get_span()
    sentence = task.context.get_span()

    if name in sentence:
        idx = sentence.index(name)
        if idx + len(name) < len(sentence):
            if sentence[idx + len(name)] not in [" ", ",", ";", "."]:
                return FALSE
    
        if idx >= 1:
            if sentence[idx - 1] not in [" ", ",", ";", "."]:
                return FALSE
    return ABSTAIN


name_abbr_task_lfs = [
    # name_in_task,
    lf_length_more_than_three_words,
    lf_name_short_in_first_words,
    is_medical_abbreviation,
    sentence_beginning,
    common_verbs_following_abbr,
    verbs_ending_with_past,
    word_before_abbr,
    abbr_is_complete,
    # lf_check_surr_chars
]