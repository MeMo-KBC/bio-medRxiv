from fonduer.candidates.matchers import LambdaFunctionMatcher, Union, Intersect, RegexMatchSpan
import re
from random import randint


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

match_small_letters = RegexMatchSpan(rgx=r'[a-z]{8}')
match_small_words = RegexMatchSpan(rgx=r'[a-z]+\s{3,}')

matcher_task = Intersect(
    Union(
        match_small_letters,
        match_small_words
    )
)

'''
def first_page(mention):
    """Matches a span if it is on the first page."""
    page = get_page(mention)
    if page == 1:
        return True
    else:
        return False
'''