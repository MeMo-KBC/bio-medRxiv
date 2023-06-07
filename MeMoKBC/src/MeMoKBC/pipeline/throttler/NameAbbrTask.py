def are_neighbors(c):
    '''Checks if the Mentions are neighbors'''
    name_abbr, task = c
    name_abbr_sentence_id = name_abbr.context.sentence.position
    task_span = task.context.get_span()

