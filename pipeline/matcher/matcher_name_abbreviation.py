from fonduer.candidates.matchers import LambdaFunctionMatcher, Union
import re


# First Regex Function
def first_matcher_capital_letter(mention):
    '''Matches a span if 2 to 4 letters are written in capital'''

    mention_string = mention.get_span()
    capital_words_letter = re.findall('[A-Z]{2,4}', mention_string)
    return capital_words_letter


# Second Regex Function
def second_matcher_capital_letter(mention):
    '''Matches a span if 2 letters are written in capital seperated by any single character'''

    mention_string = mention.get_span()
    capital_words_sep_one = re.findall('[A-Z].[A-Z]', mention_string)
    return capital_words_sep_one

# Third Regex Function
def third_matcher_abbreviations(mention):
    '''Matches a span if it resembles one of the abbreviation styles which where identified by macmacpri'''
    
    mention_string = mention.get_span()
    abbreviation = re.findall('(^\(?\w{1}[\.-]{0,2}\w{1}[\.\-:]{0,2}\w?[\.\-:]{0,2}\w?\)?$)', mention_string)
    return abbreviation

name_matcher_letter = LambdaFunctionMatcher(func=first_matcher_capital_letter)
name_matcher_sep_one = LambdaFunctionMatcher(func=second_matcher_capital_letter)
name_matcher_abbreviation = LambdaFunctionMatcher(func=third_matcher_abbreviations)

# combine all functions to one
matcher_abb_name = Union(
    name_matcher_letter,
    name_matcher_sep_one,
    name_matcher_abbreviation
)