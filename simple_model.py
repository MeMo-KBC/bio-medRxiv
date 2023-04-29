from fonduer.supervision import Labeler
from fonduer.parser.models import Document

from pipeline.utils import get_session
from definitions.candidates import NameFullAbbr, NameFullTask
from pipeline.lfs.dummy_lfs import dummy_lfs

from fonduer.candidates.models import Candidate
from fonduer.candidates.matchers import LambdaFunctionMatcher, Union
import re
from snorkel.labeling import LFAnalysis # LFAnalysis creates statistic on Coverage, Overlap, Conflict
from snorkel.labeling.model import LabelModel
from pipeline.machine_learning.custom_get_candidates import custom_get_candidates

import emmental
from emmental.modules.embedding_module import EmbeddingModule
from fonduer.meta import Meta
from fonduer.features import Featurizer
from emmental.data import EmmentalDataLoader
from fonduer.learning.dataset import FonduerDataset
import numpy as np
from emmental.model import EmmentalModel
from fonduer.learning.task import create_task
from emmental.learner import EmmentalLearner


def main(db_name):
    PARALLEL = 12
    session = get_session(db_name)
    labeler = Labeler(session, [NameFullAbbr, NameFullTask])

    #labeler.apply(split=0, lfs=[dummy_lfs, dummy_lfs], train=True, parallelism=PARALLEL)
    #labeler.apply(split=1, lfs=[dummy_lfs, dummy_lfs], parallelism=PARALLEL)
    #labeler.apply(split=2, lfs=[dummy_lfs, dummy_lfs], parallelism=PARALLEL)

    train_cands = custom_get_candidates(session, 0, [NameFullAbbr, NameFullTask])
    dev_cands = custom_get_candidates(session, 1, [NameFullAbbr, NameFullTask])
    test_cands = custom_get_candidates(session, 2, [NameFullAbbr, NameFullTask])

    L_train = labeler.get_label_matrices(train_cands) # rows = candidates, columns = labelfuncs with -1, 0, 1
    # ^-- these are needed for receiving the empirical accuracy as well as training the model

    # (gold) labels must be loaded to calculate the empirical accuracy of our labeling functions with helpf of snorkel
    # L_gold_train = labeler.get_gold_labels(train_cands, annotator="gold")

    
    LFAnalysis(
        L_train[0],
        lfs=sorted(dummy_lfs, key=lambda lf: lf.name)
    ).lf_summary() #Y=L_gold_train[0].reshape(-1)) #adds empirical accuracy to statistics


    # Training a simple model based on the Labelfunctions to estimate their accuracies
    gen_model = LabelModel(cardinality=2) # <-- cardinality = number of classes
    gen_model.fit(L_train[0], n_epochs=500, log_freq=100)


    # We now apply the generative model to the training candidates to get the noise-aware training label set. We'll refer to these as the training marginals:
    train_marginals = gen_model.predict_proba(L_train[0]) # <-- TH: do not understand why L_train instead of train_cands, but backed up by two notebooks of Fonduer

    # Apply the generative model to the development data set
    labeler.apply(split=1, lfs=[dummy_lfs, dummy_lfs], parallelism=PARALLEL)
    L_dev = labeler.get_label_matrices(dev_cands)
    print(L_dev[0].shape)

    # We now could check the F1 score, but most likely our model is overfitted to the data and therefore it will likely be too good

    

    # Setup training config
    config_cheese = {
        "meta_config": {"verbose": True},
        "model_config": {"model_path": None, "device": 0, "dataparallel": False},
        "learner_config": {
            "n_epochs": 30,
            "optimizer_config": {"lr": 0.001, "l2": 0.0},
            "task_scheduler": "round_robin",
        },
        "logging_config": {
            "evaluation_freq": 1,
            "counter_unit": "epoch",
            "checkpointing": False,
            "checkpointer_config": {
                "checkpoint_metric": {f"{db_name}/{db_name}/train/loss": "min"},
                "checkpoint_freq": 1,
                "checkpoint_runway": 2,
                "clear_intermediate_checkpoints": True,
                "clear_all_checkpoints": True,
            },
        },
    }

    emmental.init(Meta.log_path)
    emmental.Meta.update_config(config=config_cheese)


    # Collect word counter from training data
    from fonduer.learning.utils import collect_word_counter

    word_counter = collect_word_counter(train_cands) # assumption: gives each word a number starting with 0


    # Generate word embedding module for LSTM model
    # (in Logistic Regression, we generate it since Fonduer dataset requires word2id dict)

    arity = 2

    # Geneate special tokens
    specials = []
    for i in range(arity):
        specials += [f"~~[[{i}", f"{i}]]~~"] # for arity = 2 --> ["~~[[0", "0]]~~","~~[[1", "1]]~~"] # maybe they get excluded?

    emb_layer = EmbeddingModule(
        word_counter=word_counter, word_dim=300, specials=specials
    )

    # Needs to be done somehwhere before along with extracting the candidates maybe?:

    featurizer = Featurizer(session, [NameFullAbbr, NameFullTask])
    # featurizer.apply(split=0, train=True, parallelism=PARALLEL)
    F_train = featurizer.get_feature_matrices(train_cands)

    print(F_train[0].shape)
    
    # featurizer.apply(split=1, parallelism=PARALLEL)
    F_dev = featurizer.get_feature_matrices(dev_cands)
    print(F_dev[0].shape)

    #featurizer.apply(split=2, parallelism=PARALLEL)
    F_test = featurizer.get_feature_matrices(test_cands)
    print(F_test[0].shape)


    # Generate dataloader for training set
   
    # Filter out noise samples
    diffs = train_marginals.max(axis=1) - train_marginals.min(axis=1)
    train_idxs = np.where(diffs > 1e-6)[0]

    train_dataloader = EmmentalDataLoader(
        task_to_label_dict={db_name: "labels"},
        dataset=FonduerDataset(
            db_name,
            train_cands[0],
            F_train[0],
            emb_layer.word2id,
            train_marginals,
            train_idxs,
        ),
        split="train",
        batch_size=100,
        shuffle=True,
    )


    # Create task and model, and perform training
    tasks = create_task(
        db_name, 2, F_train[0].shape[1], 2, emb_layer, model="LogisticRegression"
    )

    model = EmmentalModel(name=f"{db_name}_task")

    for task in tasks:
        model.add_task(task)

    emmental_learner = EmmentalLearner()
    emmental_learner.learn(model, [train_dataloader])






if __name__ == '__main__':
    main("test_collection")