from fonduer.candidates.matchers import LambdaFunctionMatcher, Union, Intersect, RegexMatchSpan
from fonduer.utils.data_model_utils.structural import get_attributes, get_prev_sibling_tags
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
'''
match_capital_words = RegexMatchSpan(rgx=r"([A-Z][a-z]+\s?){2,}")

matcher_name_full = Intersect(
    match_capital_words,
    LambdaFunctionMatcher(func=every_hundreth)
    )
'''

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

#match_capital_letters = RegexMatchSpan(rgx=r"[A-Z]{2,4}")
#match_seperated_capital_letters = RegexMatchSpan(rgx=r"[A-Z].[A-Z]")
#match_abbrv_style = RegexMatchSpan(rgx=r'(^\(?\w{1}[\.-]{0,2}\w{1}[\.\-:]{0,2}\w?[\.\-:]{0,2}\w?\)?$)')

'''
matcher_name_abbrv = Intersect(
    Union(
        match_capital_letters,
        match_seperated_capital_letters
    ),
    LambdaFunctionMatcher(func=every_tenth)
)
'''
match_all = RegexMatchSpan(rgx=r"^[A-Z][\'.-]?[\s]?[A-Z][\'.-]?[aA-zZ]?[\'.-]?[aA-zZ]?[\'.-]?[aA-zZ]?", ignore_case = False)
match_capital_dot_small = RegexMatchSpan(rgx=r"^[A-Z][a-z][\'.-][A-Z][\'.-]?[aA-zZ]*", ignore_case = False)

matcher_name_abbrv = Union(
        match_all,
        match_capital_dot_small
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