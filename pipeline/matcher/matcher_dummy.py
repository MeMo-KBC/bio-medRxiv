from fonduer.candidates.matchers import LambdaFunctionMatcher
import re

def match_capital_letters(mention):
    pattern = r"[A-Z][a-z]+"
    if all(re.match(pattern, gram) for gram in mention):
        return True
    else:
        return False


dummy_matcher_capital = LambdaFunctionMatcher(match_capital_letters)