from fonduer.utils.data_model_utils.tabular import same_table

def throt_same_table(c):
    '''checks if Mentions of the Candidate appear within same table'''
    if same_table(c):
        return False
    else:
        return True