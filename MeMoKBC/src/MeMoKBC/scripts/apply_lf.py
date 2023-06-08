from fonduer.supervision import Labeler
from fonduer.parser.models import Document

from MeMoKBC.definitions.candidates import NameFullAbbr, NameAbbrTask
from MeMoKBC.pipeline.lfs.name_short_task_lfs import name_abbr_task_lfs
from MeMoKBC.pipeline.lfs.name_full_abbr_lfs import name_full_abbr_lfs

def apply_lf(session, parallel: int=12):
    labeler = Labeler(session, [NameFullAbbr, NameAbbrTask])

    labeler.apply(split=0, lfs=[name_full_abbr_lfs, name_abbr_task_lfs], train=True, parallelism=parallel)
    labeler.apply(split=1, lfs=[name_full_abbr_lfs, name_abbr_task_lfs], parallelism=parallel)
    labeler.apply(split=2, lfs=[name_full_abbr_lfs, name_abbr_task_lfs], parallelism=parallel)
