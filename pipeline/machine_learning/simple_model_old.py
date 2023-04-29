# This is only a draft and a description of the necessary steps to take
# DEVELOPEMENT STATUS

from fonduer.candidates.matchers import LambdaFunctionMatcher, Union
import re

# Probably part of the execution script:
#
%time labeler.apply(split=0, lfs=[president_name_pob_lfs], train=True, parallelism=PARALLEL)
%time L_train = labeler.get_label_matrices(train_cands) # rows = candidates, columns = labelfuncs with -1, 0, 1
# ^-- these are needed for receiving the empirical accuracy as well as training the model



# Unclear if this is already part of machine learning or still belongs to previous part:
#
# (gold) labels must be loaded to calculate the empirical accuracy of our labeling functions with helpf of snorkel
L_gold_train = labeler.get_gold_labels(train_cands, annotator="gold")

from snorkel.labeling import LFAnalysis # LFAnalysis creates statistic on Coverage, Overlap, Conflict
LFAnalysis(
    L_train[0],
    lfs=sorted(president_name_pob_lfs, key=lambda lf: lf.name)
).lf_summary(Y=L_gold_train[0].reshape(-1)) # adds empirical accuracy to statistics


# Training a simple model based on the Labelfunctions to estimate their accuracies
from snorkel.labeling.model import LabelModel

gen_model = LabelModel(cardinality=2) # <-- cardinality = number of classes
%time gen_model.fit(L_train[0], n_epochs=500, log_freq=100)


# We now apply the generative model to the training candidates to get the noise-aware training label set. We'll refer to these as the training marginals:
train_marginals = gen_model.predict_proba(L_train[0]) # <-- TH: do not understand why L_train instead of train_cands, but backed up by two notebooks of Fonduer

# Apply the generative model to the development data set
labeler.apply(split=1, lfs=[president_name_pob_lfs], parallelism=PARALLEL)
%time L_dev = labeler.get_label_matrices(dev_cands)
L_dev[0].shape

# We now could check the F1 score, but most likely our model is overfitted to the data and therefore it will likely be too good



