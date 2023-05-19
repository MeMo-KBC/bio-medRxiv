# This is only a draft and a description of the necessary steps to take
# DEVELOPEMENT STATUS


# PREVIOUS STEPS START (MP)

# 1. Loading Gold Data (on dev and test set) - Use later for error analysis and evaluation of the model


# 2. Write Labeling Functions that:
# -> Accepts a Candidate as an input argument and returns 2 (Canditate marked as true) / 1 (Canditate marked as false) / 0 (Abstains)


# 3. Collect all labeling functions in one list -> List acts as an input to the Labler
#
# president_name_pob_lfs = [
#     LF_place_of_birth_has_link,
#     LF_place_of_birth_is_longest_ordered_span_before_comma,
#     LF_place_not_a_US_state,
#     LF_place_in_first_sentence_of_cell,
#     LF_place_is_full_sentence,
# ]

# PREVIOUS STEPS END (MP)


# Import necessary at this point? (MP)
#
from fonduer.candidates.matchers import LambdaFunctionMatcher, Union
import re


# Applying labeling functions -> Using the list (president_name_pob_lfs) containing all previously defined functions (MP)
#
# Probably part of the execution script:
#
%time labeler.apply(split=0, lfs=[president_name_pob_lfs], train=True, parallelism=PARALLEL) # lfs=[president_name_pob_lfs], list containing all labeling functions (MP)
%time L_train = labeler.get_label_matrices(train_cands) # rows = candidates, columns = labelfuncs with -1, 0, 1
# ^-- these are needed for receiving the empirical accuracy as well as training the model


# Unclear if this is already part of machine learning or still belongs to previous part:
#
# (gold) labels must be loaded to calculate the empirical accuracy of our labeling functions with help of snorkel
#
L_gold_train = labeler.get_gold_labels(train_cands, annotator="gold")


# Creates a summary table with statistics on the comparison of the results of the labeling functions and the gold standard (MP)
#
from snorkel.labeling import LFAnalysis # LFAnalysis creates statistic on Coverage, Overlap, Conflict

LFAnalysis(
    L_train[0],
    lfs=sorted(president_name_pob_lfs, key=lambda lf: lf.name)
).lf_summary(Y=L_gold_train[0].reshape(-1)) # adds empirical accuracy to statistics


# Fitting the Generative Model (MP)

# Training a simple model based on the Labelfunctions to estimate their accuracies
#
from snorkel.labeling.model import LabelModel

gen_model = LabelModel(cardinality=2) # <-- cardinality = number of classes (Number of classes, by default 2 (MP))
%time gen_model.fit(L_train[0], n_epochs=500, log_freq=100)


# We now apply the generative model to the training candidates to get the noise-aware training label set. We'll refer to these as the training marginals:
#
train_marginals = gen_model.predict_proba(L_train[0]) # <-- TH: do not understand why L_train instead of train_cands, but backed up by two notebooks of Fonduer <- L_train contains all labeling functions (president_name_pob_lfs) and the train_cands (MP)

# Apply the generative model to the development data set
#
labeler.apply(split=1, lfs=[president_name_pob_lfs], parallelism=PARALLEL)
%time L_dev = labeler.get_label_matrices(dev_cands)
L_dev[0].shape

# We now could check the F1 score, but most likely our model is overfitted to the data and therefore it will likely be too good



