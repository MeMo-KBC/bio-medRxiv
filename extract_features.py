from fonduer.features import Featurizer
from fonduer.parser.models import Document

from pipeline.utils import get_session
from definitions.candidates import NameFullAbbr, NameFullTask

def main():
    session = get_session("test_collection")
    featurizer = Featurizer(session, [NameFullTask, NameFullAbbr], parallelism=6)
    featurizer.apply(split=0, train=True)
    featurizer.apply(split=1)
    featurizer.apply(split=2)


if __name__ == '__main__':
    main()