# def are_neighbors(c):
#     '''Checks if the Mentions are neighbors'''
#     name_abbr, task = c
#     name_abbr_sentence_id = name_abbr.context.sentence.position
#     task_span = task.context.get_span()



def name_mention_in_task_mention_throttler(c):
    '''
    checks if NameAbb in Task
    '''
    #print(c[0].context.get_span())
    if c[0].context.get_span() in c[1].context.get_span():
        return True
    else:
        return False


