from fonduer.candidates.matchers import LambdaFunctionMatcher
import re

# Define function
def matcher_capital_letter(mention):
    
    # Matches a span if three capital letters follow each other
    mention_string = mention.get_span()
    capital_word = re.findall('([A-Z]{3})', mention_string)
    return capital_word

capital_letter_matcher = LambdaFunctionMatcher(func=matcher_capital_letter)