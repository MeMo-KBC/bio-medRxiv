from fonduer.candidates.matchers import LambdaFunctionMatcher, Union, Intersect, Inverse, RegexMatchSpan
from fonduer.utils.data_model_utils.structural import get_attributes, get_prev_sibling_tags
import re
from random import randint


# Matchers for NameFull
def matcher_name_full_func(mention):
    """ Matches only the name of Authors in the section below the title."""


    mention_class = 'class=highwire-cite-authors' in get_attributes(mention)
    prev_sibling_tag = 'h1' in get_prev_sibling_tags(mention)
    name = re.match("(^\w+\s(\w\.\s)?\w+)", mention.get_span(), re.IGNORECASE) # Might needs to be adjusted in regards the findings of labeling group.

    if mention_class and prev_sibling_tag and name:
        return True
    else:
        return False


matcher_name_full = LambdaFunctionMatcher(func=matcher_name_full_func)


# Matchers for NameAbbrv

match_all = RegexMatchSpan(rgx=r"[\s]?[A-Z][\'.-]?[\s]?[A-Z][\'.-]?[aA-zZ]?[\'.-]?[aA-zZ]?[\'.-]?[aA-zZ]*[\'.-]?[\s]?", ignore_case = False)
match_capital_dot_small = RegexMatchSpan(rgx=r"[A-Z][a-z][\'.-]?[a-z]?[A-Z][\'.-]?[aA-zZ]*", ignore_case = False)
match_maxlength = RegexMatchSpan(rgx=r".{1,11}", ignore_case = True)
match_group_smallletters = RegexMatchSpan(rgx = r"[a-z]{5,}", ignore_case = False, search = True)
match_group_bigletters = RegexMatchSpan(rgx = r"[A-Z]{5,}", ignore_case = False, search = True)


matcher_name_abbrv = Intersect(
    Union(
        match_all,
        match_capital_dot_small,
    ),
    match_maxlength,
    Inverse(match_group_smallletters),
    Inverse(match_group_bigletters)
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