from fonduer.utils.data_model_utils.tabular import same_table

def throt_same_table(c):
    '''checks if Mentions of the Candidate appear within same table'''
    if same_table(c):
        return False
    else:
        return True


    
def task_is_written_in_capital(c):
    '''checks if Task-Mentions of the Candidate is written in capital letters'''
    
    task_string = c[1].context.text

    if task_string.isupper():
        return False
    else:
        return True

