from fonduer.supervision import Labeler
from fonduer.parser.models import Document

from pipeline.utils import get_session
from definitions.candidates import NameFullAbbr, NameFullTask
from pipeline.lfs.dummy_lfs import dummy_lf_rand

from fonduer.candidates.models import Candidate
# maybe not needed
from fonduer.candidates.matchers import LambdaFunctionMatcher, Union
import re
from snorkel.labeling import LFAnalysis # LFAnalysis creates statistic on Coverage, Overlap, Conflict
from snorkel.labeling.model import LabelModel


def main(db_name):
    PARALLEL = 12
    session = get_session(db_name)
    labeler = Labeler(session, [NameFullAbbr, NameFullTask])

    labeler.apply(split=0, lfs=[dummy_lf_rand, dummy_lf_rand], train=True, parallelism=PARALLEL)
    labeler.apply(split=1, lfs=[dummy_lf_rand, dummy_lf_rand], parallelism=PARALLEL)
    labeler.apply(split=2, lfs=[dummy_lf_rand, dummy_lf_rand], parallelism=PARALLEL)

    train_cands = session.query(Candidate).filter(Candidate.split==0).all()
    dev_cands = session.query(Candidate).filter(Candidate.split==1).all()

    L_train = labeler.get_label_matrices(train_cands) # rows = candidates, columns = labelfuncs with -1, 0, 1
    # ^-- these are needed for receiving the empirical accuracy as well as training the model

    # (gold) labels must be loaded to calculate the empirical accuracy of our labeling functions with helpf of snorkel
    # L_gold_train = labeler.get_gold_labels(train_cands, annotator="gold")

    
    LFAnalysis(
        L_train[0],
        lfs=sorted(dummy_lf_rand, key=lambda lf: lf.name)
    ).lf_summary() #Y=L_gold_train[0].reshape(-1)) #adds empirical accuracy to statistics


    # Training a simple model based on the Labelfunctions to estimate their accuracies
    gen_model = LabelModel(cardinality=2) # <-- cardinality = number of classes
    gen_model.fit(L_train[0], n_epochs=500, log_freq=100)


    # We now apply the generative model to the training candidates to get the noise-aware training label set. We'll refer to these as the training marginals:
    train_marginals = gen_model.predict_proba(L_train[0]) # <-- TH: do not understand why L_train instead of train_cands, but backed up by two notebooks of Fonduer

    # Apply the generative model to the development data set
    labeler.apply(split=1, lfs=[dummy_lf_rand], parallelism=PARALLEL)
    L_dev = labeler.get_label_matrices(dev_cands)
    L_dev[0].shape

    # We now could check the F1 score, but most likely our model is overfitted to the data and therefore it will likely be too good





if __name__ == '__main__':
    main("test_collection")