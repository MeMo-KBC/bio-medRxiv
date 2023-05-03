from fonduer.features import Featurizer
from fonduer.parser.models import Document

from pipeline.utils import get_session
from definitions.candidates import NameFullAbbr, NameFullTask

def main(db_name: str):
    session = get_session(db_name)
    featurizer = Featurizer(session, [NameFullTask, NameFullAbbr], parallelism=6)
    featurizer.apply(split=0, train=True)
    featurizer.apply(split=1)
    featurizer.apply(split=2)


if __name__ == '__main__':
    main("test_collection")