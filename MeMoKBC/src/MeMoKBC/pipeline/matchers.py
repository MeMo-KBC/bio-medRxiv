from fonduer.candidates.matchers import LambdaFunctionMatcher, Union, Intersect, RegexMatchSpan
import re
from random import randint


# Matchers for NameFull

match_name_full = RegexMatchSpan(rgx=r"([A-Z][a-z]+\s?){2,}")



# Matchers for NameAbbrv

match_all = RegexMatchSpan(rgx=r"[\s]?[A-Z][\'.-]?[\s]?[A-Z][\'.-]?[aA-zZ]?[\'.-]?[aA-zZ]?[\'.-]?[aA-zZ]*[\'.-]?[\s]?", ignore_case = False)
match_capital_dot_small = RegexMatchSpan(rgx=r"[A-Z][a-z][\'.-]?[a-z]?[A-Z][\'.-]?[aA-zZ]*", ignore_case = False)

matcher_name_abbrv = Intersect(
    Union(
        match_all,
        match_capital_dot_small
    )
)


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