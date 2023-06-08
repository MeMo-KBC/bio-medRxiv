def count_small_letter_throttler(c):
    '''Checks if the Mention NameShort has more than two small letters'''
    # Extract the first Mention (NameShort)
    name_short = c[1]
    # Get the string representation of the first Mention
    name_short_string = name_short.context.get_span()
    # Count the number of lowercase letters in the string
    lowercase_count = sum(1 for w in name_short_string if w.islower())

    if lowercase_count <= 5:
        return True
    else:
        return False



def same_first_character_throttler(c):
    '''Checks if both Mentions start with the same letter'''
    # Extract both Mentions
    name_short = c[1]
    name_long = c[0]
    
    # Get the string representation
    short_string = name_short.context.get_span()
    long_string = name_long.context.get_span()
    
    # Convert the strings to lowercase
    short_string = short_string.lower()
    long_string = long_string.lower()
    
    # Check if the first characters of the strings are the same
    if short_string[0] == long_string[0]:
        return True
    else:
        return False
    
# def all_short_in_long_throttler(c):
#    '''Checks if all words of the short name are contained in the long name'''
#    # Extract both Mentions
#    name_short = c[1]
#    name_long = c[0]
#
#    # Get the string representation
#    short_string = name_short.context.get_span()
#    long_string = name_long.context.get_span()
#
#    # Convert the strings to lowercase
#    short_string = short_string.lower()
#    long_string = long_string.lower()
#
#    # Split the strings into words
#    short_words = short_string.split()
#    long_words = long_string.split()
# ...


def name_shortlong_throttler(c):
    if count_small_letter_throttler(c) and same_first_character_throttler(c):
        return True
    else:
        return False