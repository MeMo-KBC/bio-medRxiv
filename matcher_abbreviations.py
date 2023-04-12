from fonduer.candidates.matchers import LambdaFunctionMatcher, Union
import re

# First Regex Function
def matcher_just_capital(mention):
    '''Matches a span if 2 to 4 letters are written in capital - von marc''' 

    mention_string = mention.get_span()
    match_found = re.findall('[A-Z]{2,4}', mention_string)
    return match_found

def matcher_capital_point(mention):
    '''Matches a span if a capital letter and a point match 2-3 times'''

    mention_string = mention.get_span()
    match_found = re.findall('([A-Z]\.){2,3}', mention_string)
    return match_found

def matcher_capital_point_minus(mention):
    '''Matches a span if a capital letter and a point match 3 times and have a - within'''

    mention_string = mention.get_span()
    match_found = re.findall('[A-Z]\.-[A-Z]\.[A-Z]', mention_string)
    return match_found

name_matcher_1 = LambdaFunctionMatcher(func=matcher_just_capital)
name_matcher_2 = LambdaFunctionMatcher(func=matcher_capital_point)
name_matcher_3 = LambdaFunctionMatcher(func=matcher_capital_point_minus)

matcher_abb_name = Union( #fügt die Ergebnisse aller Matcher zusammen # Gegenteil ist Intersect()? aus presidenten-bsp?
    name_matcher_1,
    name_matcher_2,
    name_matcher_3

)

# in einem bestimmten p, table, page?

# in abschnitt authors contributions, acknowledgements
# 2-3 Großbuchstaben
# Großbuchstabe punkt (2-3 mal)
    # mit - vor Großbuchstabe bei dem mittleren buchstabe

# testen an doc 10.1101.2019.12.20.882787