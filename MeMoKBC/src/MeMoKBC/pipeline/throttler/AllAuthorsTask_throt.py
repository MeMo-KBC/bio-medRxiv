def all_authors_task_throttler(c):
    """
    Custom throttler function to filter candidates of the AllAuthorsTask class where "all authors" and a mention of a task occur in the same sentence.
    """
    if isinstance(c):
        sentence_index_1 = c.all_authors.sentence.index
        sentence_index_2 = c.task.sentence.index

        if sentence_index_1 == sentence_index_2:
            return True

    return False
