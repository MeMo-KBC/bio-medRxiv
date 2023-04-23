from fonduer.supervision import Labeler
from fonduer.parser.models import Document

from pipeline.utils import get_session
from definitions.candidates import NameFullAbbr, NameFullTask
from pipeline.lfs.dummy_lfs import dummy_lf_rand


def main(db_name):
    PARALLEL = 12
    session = get_session(db_name)
    labeler = Labeler(session, [NameFullAbbr, NameFullTask])

    labeler.apply(split=0, lfs=[dummy_lf_rand, dummy_lf_rand], train=True, parallelism=PARALLEL)
    labeler.apply(split=1, lfs=[dummy_lf_rand, dummy_lf_rand], parallelism=PARALLEL)
    labeler.apply(split=2, lfs=[dummy_lf_rand, dummy_lf_rand], parallelism=PARALLEL)
    


if __name__ == '__main__':
    main("test_collection")