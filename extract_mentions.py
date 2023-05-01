from fonduer.candidates import MentionExtractor
from definitions.mentions.mention_subclasses import NameAbbr, NameFull, Task
from definitions.mentions.mention_spaces import nameAbbrv_ngrams, nameFull_ngrams, task_sentences
from pipeline.matchers import matcher_name_abbrv, matcher_task
from pipeline.matcher.matcher_name_full import matcher_name_full
from pipeline.utils import get_session, PARALLEL
from fonduer.parser.models import Document

def extract_mentions(db_name: str):

    assert db_name, "db_name is necessary"  
    session = get_session(db_name=db_name)

    docs = session.query(Document).all()

    mention_extractor = MentionExtractor(
        session,
        [NameAbbr, NameFull, Task],
        [nameAbbrv_ngrams, nameFull_ngrams, task_sentences],
        [matcher_name_abbrv, matcher_name_full, matcher_task],
        parallelism=PARALLEL,
    )

    mention_extractor.apply(docs, parallelism=PARALLEL, clear=True)
    print(
        f"Number of NameAbbrs: {session.query(NameAbbr).count()}",
        f"Number of NameFulls: {session.query(NameFull).count()}",
        f"Number of Tasks: {session.query(Task).count()}",
    )

if __name__ == '__main__':
    extract_mentions("test_collection")    