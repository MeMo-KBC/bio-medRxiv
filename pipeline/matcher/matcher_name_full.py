from fonduer.candidates.matchers import LambdaFunctionMatcher
from fonduer.utils.data_model_utils.structural import get_attributes, get_prev_sibling_tags
import re


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