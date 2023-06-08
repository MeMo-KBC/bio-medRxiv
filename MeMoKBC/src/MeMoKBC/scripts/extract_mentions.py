from fonduer.candidates import MentionExtractor
from fonduer.parser.models import Document

from MeMoKBC.definitions.mentions.mention_subclasses import NameAbbr, NameFull, Task, AllAuthors
from MeMoKBC.definitions.mentions.mention_spaces import nameAbbrv_ngrams, nameFull_ngrams, task_sentences, AllAuthors_ngrams
from MeMoKBC.pipeline.matchers import matcher_name_abbrv, matcher_task, matcher_name_full, matcher_all_authors


def extract_mentions(session, parallel: int=12):

    docs = session.query(Document).all()

    mention_extractor = MentionExtractor(
        session,
        [NameAbbr, NameFull, Task, AllAuthors],
        [nameAbbrv_ngrams, nameFull_ngrams, task_sentences, AllAuthors_ngrams],
        [matcher_name_abbrv, matcher_name_full, matcher_task, matcher_all_authors],
    )

    mention_extractor.apply(docs, clear=True)
    print(
        f"Number of NameAbbrs: {session.query(NameAbbr).count()}",
        f"Number of NameFulls: {session.query(NameFull).count()}",
        f"Number of Tasks: {session.query(Task).count()}",
        f"Number of AllAuthors: {session.query(AllAuthors).count()}"
    )
