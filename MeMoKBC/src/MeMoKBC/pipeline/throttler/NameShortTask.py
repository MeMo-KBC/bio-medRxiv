from fonduer.utils.data_model_utils.textual import same_sentence

def throttler_same_sentence(c):
    '''checks if mentions of the candidate are in the same sentence'''
    if same_sentence(c):
        return True
    else:
        return False