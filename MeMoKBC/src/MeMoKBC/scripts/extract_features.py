from fonduer.features import Featurizer
from fonduer.parser.models import Document

from MeMoKBC.definitions.candidates import NameFullAbbr, NameFullTask, NameAbbrTask

def extract_features(session, parallel: int=12):
    featurizer = Featurizer(session, [NameAbbrTask], parallelism=parallel)
    featurizer.apply(split=0, train=True)
    featurizer.apply(split=1)
    featurizer.apply(split=2)   