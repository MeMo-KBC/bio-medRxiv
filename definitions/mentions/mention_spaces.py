from fonduer.candidates import MentionNgrams
from fonduer.candidates.mentions import MentionSentences

nameFull_ngrams = MentionNgrams(n_min=1, n_max=2)
nameAbbrv_ngrams = MentionNgrams(n_min=1, n_max=1)
task_sentences = MentionSentences()