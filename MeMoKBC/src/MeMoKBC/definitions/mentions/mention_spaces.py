from fonduer.candidates import MentionNgrams
from fonduer.candidates.mentions import MentionSentences

nameFull_ngrams = MentionNgrams(n_min=1, n_max=3)
nameAbbrv_ngrams = MentionNgrams(n_min=1, n_max=3)
AllAuthors_ngrams = MentionNgrams(n_min=1, n_max=3)
task_sentences = MentionSentences()