from fonduer.candidates.matchers import LambdaFunctionMatcher, Union
import re

# 1
def matcher_just_capital(mention):
    '''Matches a span if 2 to 4 letters are written in capital - von marc''' 

    mention_string = mention.get_span()
    match_found = re.findall('[A-Z]{2,4}', mention_string)
    return match_found

# 2
def matcher_capital_minus(mention):
    '''Matches a span if 3 letters are written in capital and have a - within''' 

    mention_string = mention.get_span()
    match_found = re.findall('[A-Z](-[A-Z]|[A-Z]-){1,2}[A-Z]', mention_string)
    return match_found

# 3
def matcher_capital_point(mention):
    '''Matches a span if a capital letter and a point match 2-4 times'''

    mention_string = mention.get_span()
    match_found = re.findall('([A-Z]\.){2,4}', mention_string)
    return match_found

# 4
def matcher_capital_point_minus(mention):
    '''Matches a span if a capital letter and a point match 3 times and have a - within'''

    mention_string = mention.get_span()
    match_found = re.findall('[A-Z]\.-[A-Z]\.[A-Z]', mention_string)
    return match_found

# 5
def matcher_capital_lower_point(mention):
    '''Matches a span if a capital, a possible lower and a point are 2-3 times found'''

    mention_string = mention.get_span()
    match_found = re.findall('([A-Z][a-z]?\.){2,3}', mention_string)
    return match_found

name_matcher_1 = LambdaFunctionMatcher(func=matcher_just_capital)
name_matcher_2 = LambdaFunctionMatcher(func=matcher_capital_minus)
name_matcher_3 = LambdaFunctionMatcher(func=matcher_capital_point)
name_matcher_4 = LambdaFunctionMatcher(func=matcher_capital_point_minus)
name_matcher_5 = LambdaFunctionMatcher(func=matcher_capital_lower_point)

matcher_abb_name = Union( #fügt die Ergebnisse aller Matcher zusammen # Gegenteil ist Intersect()? aus presidenten-bsp?
    name_matcher_1,
    name_matcher_2,
    name_matcher_3,
    name_matcher_4,
    name_matcher_5
)



# in einem bestimmten p, table, page? für Throttler oder LF



# in abschnitt authors contributions, acknowledgements
# nicht immer fett, nicht immer ein titel, nicht immer mit :, manchmal alles groß geschrieben
# distanz von "author contributions" zu matcher, je kleiner, desto relevanter?

# 2-3 Großbuchstaben
# Großbuchstabe punkt (2-3 mal)
    # mit - vor Großbuchstabe bei dem mittleren buchstabe

# mögliche falsch positiv -> noch unklar wie groß die menge der falsch positiven matcher ist

# NY -> New York
# 



# 10.1101.2019.12.28.886655 # Namen sind ausgeschrieben, keine kürzel und in Absatz 'Contributions'
# 10.1101.2019.12.28.890046 # M.Tu., M.Ts. zweiter buchstabe um beide auseinander halten zu können?
# 10.1101.2019.12.30.891457 # abb. 4 cap letters
# 10.1101.2020.01.01.891432 # no contributions -> not abbreviations
# 10.1101.2020.01.05.895268 # no contributions, aknowledgments -> not abbreviations
# 10.1101.2020.01.02.893081 # auth contrib. title all cap