from fonduer.candidates.matchers import LambdaFunctionMatcher
import re

# Define function
def matcher_small_letter(mention):
    
    # Matches a span if 16 small letters follow each other
    mention_string = mention.get_span()
    small_word = re.findall('([a-z]{16})', mention_string)
    return small_word

small_letter_matcher = LambdaFunctionMatcher(func=matcher_small_letter)