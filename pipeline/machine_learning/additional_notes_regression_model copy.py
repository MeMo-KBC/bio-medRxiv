# This is only a draft and a description of the necessary steps to take
# DEVELOPEMENT STATUS


# Use the noisy training labels to train the end extraction model. For now a simple logistic regression model is used.
# We use the training marginals to train a discriminative model that classifies each Candidate as a true or false mention.
# Machine learning framework https://github.com/SenWu/emmental is used.

import emmental

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
            "checkpoint_metric": {f"{ATTRIBUTE}/{ATTRIBUTE}/train/loss": "min"},
            "checkpoint_freq": 1,
            "checkpoint_runway": 2,
            "clear_intermediate_checkpoints": True,
            "clear_all_checkpoints": True,
        },
    },
}

emmental.init(Meta.log_path)
emmental.Meta.update_config(config=config_cheese) # Correct that we update the current config with our new training config? (MP)


# Collect word counter from training data
from fonduer.learning.utils import collect_word_counter

word_counter = collect_word_counter(train_cands) # assumption: gives each word a number starting with 0


# Generate word embedding module for LSTM model
# (in Logistic Regression, we generate it since Fonduer dataset requires word2id dict)
from emmental.modules.embedding_module import EmbeddingModule

arity = 2

# Geneate special tokens
specials = []
for i in range(arity):
    specials += [f"~~[[{i}", f"{i}]]~~"] # for arity = 2 --> ["~~[[0", "0]]~~","~~[[1", "1]]~~"] # maybe they get excluded?

emb_layer = EmbeddingModule(
    word_counter=word_counter, word_dim=300, specials=specials
)


# Needs to be done somehwhere before along with extracting the candidates maybe?:
from fonduer.features import Featurizer

featurizer = Featurizer(session, [PresidentnamePlaceofbirth])
%time featurizer.apply(split=0, train=True, parallelism=PARALLEL)
%time F_train = featurizer.get_feature_matrices(train_cands)

print(F_train[0].shape)
%time featurizer.apply(split=1, parallelism=PARALLEL)
%time F_dev = featurizer.get_feature_matrices(dev_cands)
print(F_dev[0].shape)

%time featurizer.apply(split=2, parallelism=PARALLEL)
%time F_test = featurizer.get_feature_matrices(test_cands)
print(F_test[0].shape)


# Generate dataloader for training set
from emmental.data import EmmentalDataLoader
from fonduer.learning.dataset import FonduerDataset
import numpy as np

# Filter out noise samples
diffs = train_marginals.max(axis=1) - train_marginals.min(axis=1) # train_marginals = generative model we applied to the training candidates (From the simple_model.py)(MP)
train_idxs = np.where(diffs > 1e-6)[0]

train_dataloader = EmmentalDataLoader(
    task_to_label_dict={ATTRIBUTE: "labels"},
    dataset=FonduerDataset(
        ATTRIBUTE,
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
from emmental.model import EmmentalModel
from fonduer.learning.task import create_task
from emmental.learner import EmmentalLearner

tasks = create_task(
    ATTRIBUTE, 2, F_train[0].shape[1], 2, emb_layer, model="LogisticRegression"
)

model = EmmentalModel(name=f"{ATTRIBUTE}_task")

for task in tasks:
    model.add_task(task)

emmental_learner = EmmentalLearner()
emmental_learner.learn(model, [train_dataloader])
