from fonduer.candidates.matchers import LambdaFunctionMatcher, Union, Intersect, RegexMatchSpan
import re
from random import randint
from fonduer.parser.models import Document, Section, Table, Cell, Paragraph, Sentence, Figure, Caption

# Matchers for testing to reduce the number of candidates

def every_hundreth(mention):
    """Matches every hundreth mention."""
    if randint(1, 100) == 1:
        return True
    else:
        return False

def every_tenth(mention):
    """Matches every tenth mention."""
    if randint(1, 10) == 1:
        return True
    else:
        return False


# Matchers for NameFull

match_capital_words = RegexMatchSpan(rgx=r"([A-Z][a-z]+\s?){2,}")

matcher_name_full = Intersect(
    match_capital_words,
    LambdaFunctionMatcher(func=every_hundreth)
    )


# Matchers for NameAbbrv

match_capital_letters = RegexMatchSpan(rgx=r"[A-Z]{2,4}")
match_seperated_capital_letters = RegexMatchSpan(rgx=r"[A-Z].[A-Z]")
# match_abbrv_style = RegexMatchSpan(rgx=r'(^\(?\w{1}[\.-]{0,2}\w{1}[\.\-:]{0,2}\w?[\.\-:]{0,2}\w?\)?$)')

matcher_name_abbrv = Intersect(
    Union(
        match_capital_letters,
        match_seperated_capital_letters
    ),
    LambdaFunctionMatcher(func=every_tenth)
)



##
# !!! Meine Notizen/ Änderungen zum Task-Matcher !!!
##
# Überlegungen
# Müssen in einem Text mit Namenskürzeln sein?
# Müssen in einem Text mit Überschrift xxx sein? (z.B acknowledgements, ... gibt es vielleicht eine Liste aus dem Label Team?)
# auf bestimmte Verben filtern?
# Besteht aus Verb und Objekt
    # verb dann "of" dann Nomen
    # verb dann "and" dann verb ...
    # liste von verben und Nomen durch Komma getrennt: research studies, conducted experiments, analyzed data,...
#
# To Do: ein Beispiel Matcher der nur den Task xxx(bestimmtes verb) findet und 2 wörter danach

# Matchers for Task

# match_small_letters = RegexMatchSpan(rgx=r'[a-z]{8}')
# match_small_words = RegexMatchSpan(rgx=r'[a-z]+\s{3,}')

# matcher_task = Intersect(
#     Union(
#         match_small_letters,
#         match_small_words
#     )
# )

import sys
import subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'nltk'])
# %pip install nltk
from nltk.corpus import wordnet as wn
import nltk
nltk.download('wordnet')


#########################################################

list_of_headlines = ["Acknowledgements", "Acknowledgement", "acknowledgements", "acknowledgement", 
                     #"Contributions", "Contribution", "contribution", "contributions",
                     #"Credits", "Credit", "credits", "credit",
                     #"Überschrift 1"
                     ]


from pipeline.utils import get_session
session = get_session("jkracht") # hier eigenen DB- Namen hinzufügen

def mention_span_in_acknowledments_matches_verb(mention):
    span_string = mention.get_span()
    try:
        # get last paragraphs first sentence (headline of the paragraph)
        headline_of_last_paragraph = session.query(Paragraph).get(mention.sentence.paragraph_id-1).sentences[0].text

        # check if last headline is listed to extract mentions of
        #if headline_of_last_paragraph in list_of_headlines:
        if any(option in headline_of_last_paragraph for option in list_of_headlines):

            #test if span is a verb
            for word in wn.synsets(span_string):
                if word.pos() == "v": # and word.name().split(".")[0] == span_string.lower():
                    return True # case: span is a ver in a wanted paragraph

            return False # case: span is not a verb
        
        else:
            return False # case: span not in wanted paragraph
    except:
        return False # case: no prior paragraph

###############################    

matcher_task = LambdaFunctionMatcher(func = mention_span_in_acknowledments_matches_verb)
'''
def first_page(mention):
    """Matches a span if it is on the first page."""
    page = get_page(mention)
    if page == 1:
        return True
    else:
        return False
'''