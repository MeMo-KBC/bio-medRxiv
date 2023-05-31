from fonduer.candidates.matchers import LambdaFunctionMatcher, Union, Intersect, RegexMatchSpan
from MeMoKBC.pipeline.utils import get_session
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

list_of_headlines = [
                     #"Acknowledgements", "Acknowledgement", "acknowledgements", "acknowledgement", 
                     "Contributions", "Contribution", "contribution", "contributions",
                     "Author Contributions",
                     #"Credits", "Credit", "credits", "credit",
                     "Überschrift 1"]

def mention_get_verb(mention):
    """
    function checks
    """
    span_string = mention.get_span()
    doc_id = mention.sentence.paragraph.document_id
    para_pos = mention.sentence.paragraph.position
    try:
        p = mention.sentence.paragraph
        p_pos = mention.sentence.document.paragraphs.index(p)
        headline = p.document.paragraphs[p_pos-10:p_pos]
        for h in headline:
            x = h.sentences[0].text
            if any(option.lower() in x.lower() for option in list_of_headlines):
                return True
        else:
            
            return False # case: span not in wanted paragraph
    except:
        
        return False
        

matcher_task = LambdaFunctionMatcher(func = mention_get_verb)

'''
def first_page(mention):
    """Matches a span if it is on the first page."""
    page = get_page(mention)
    if page == 1:
        return True
    else:
        return False
'''