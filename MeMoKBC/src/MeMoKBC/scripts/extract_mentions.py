from fonduer.candidates import MentionExtractor
from fonduer.parser.models import Document

from MeMoKBC.definitions.mentions.mention_subclasses import NameAbbr, NameFull, Task
from MeMoKBC.definitions.mentions.mention_spaces import nameAbbrv_ngrams, nameFull_ngrams, task_sentences
from MeMoKBC.pipeline.matchers import matcher_name_full, matcher_name_abbrv, matcher_task


def extract_mentions(session, parallel: int=12):

    docs = session.query(Document).all()

    mention_extractor = MentionExtractor(
        session,
        [NameAbbr, Task],
        [nameAbbrv_ngrams, task_sentences],
        [matcher_name_abbrv, matcher_task],
        parallelism=parallel,
    )

    mention_extractor.apply(docs, parallelism=parallel, clear=True)
    print(
        f"Number of NameAbbrs: {session.query(NameAbbr).count()}",
        # f"Number of NameFulls: {session.query(NameFull).count()}",
        f"Number of Tasks: {session.query(Task).count()}",
    )
