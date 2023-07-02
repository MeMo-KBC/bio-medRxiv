from fonduer.supervision import Labeler
from fonduer.parser.models import Document

from MeMoKBC.definitions.candidates import NameFullAbbr, NameAbbrTask
from MeMoKBC.pipeline.lfs.name_short_task_lfs import name_abbr_task_lfs
from MeMoKBC.pipeline.lfs.name_short_long_lfs import short_long_lfs

def apply_lf(session, parallel: int=12):
    labeler = Labeler(session, [NameAbbrTask, NameFullAbbr])
    labeler.drop_keys(labeler.get_keys())
    labeler.clear_all()
    labeler.upsert_keys(name_abbr_task_lfs, NameAbbrTask)
    labeler.upsert_keys(short_long_lfs, NameFullAbbr)
    labeler.apply(split=0, lfs=[name_abbr_task_lfs, short_long_lfs], parallelism=parallel)
    labeler.apply(split=1, lfs=[name_abbr_task_lfs, short_long_lfs], parallelism=parallel)
    labeler.apply(split=2, lfs=[name_abbr_task_lfs, short_long_lfs], parallelism=parallel)