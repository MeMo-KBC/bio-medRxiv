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

match_capital_letters = RegexMatchSpan(rgx=r"[A-Z]{2}", ignore_case=False)
match_seperated_capital_letters = RegexMatchSpan(rgx=r"[A-Z].[A-Z]", ignore_case=False)
# match_abbrv_style = RegexMatchSpan(rgx=r'(^\(?\w{1}[\.-]{0,2}\w{1}[\.\-:]{0,2}\w?[\.\-:]{0,2}\w?\)?$)')


matcher_name_abbrv = Union(
    match_capital_letters,
    match_seperated_capital_letters
)


# Matchers for Task

match_small_letters = RegexMatchSpan(rgx=r'[a-z]{8}')
match_small_words = RegexMatchSpan(rgx=r'[a-z]+\s{3,}')


def match_prewritten_sentences(mention):
    sentences = [
        "LD performed most of the scFRAPs, constructed the strains and some of the plasmids used in the study, performed modeling and data analysis.",
        "AB performed scFRAPs, data analysis, developed the model and the R package for data fitting.",
        "AG performed the measurements of nuclear pore proteins.",
        "AK wrote the R package for data fitting."
        ]
    if mention.get_span() in sentences:
        return True
    else:
        return False

matcher_task = LambdaFunctionMatcher(func=match_prewritten_sentences)

'''
def first_page(mention):
    """Matches a span if it is on the first page."""
    page = get_page(mention)
    if page == 1:
        return True
    else:
        return False
'''