from fonduer.supervision import Labeler
from fonduer.parser.models import Document

from MeMoKBC.definitions.candidates import NameFullAbbr, NameAbbrTask
from MeMoKBC.pipeline.lfs.name_short_task_lfs import short_task_lfs
from MeMoKBC.pipeline.lfs.name_short_long_lfs import short_long_lfs

def apply_lf(session, parallel: int=12):
    labeler = Labeler(session, [NameFullAbbr, NameAbbrTask])

    labeler.apply(split=0, lfs=[short_long_lfs, short_task_lfs], train=True, parallelism=parallel)
    labeler.apply(split=1, lfs=[short_long_lfs, short_task_lfs], parallelism=parallel)
    labeler.apply(split=2, lfs=[short_long_lfs, short_task_lfs], parallelism=parallel)
