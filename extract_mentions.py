from fonduer.candidates import MentionExtractor
from definitions.mentions.mention_subclasses import NameAbbr, NameFull, Task
from definitions.mentions.mention_spaces import nameAbbrv_ngrams, nameFull_ngrams, task_sentences
from pipeline.matcher.matcher_name_abbreviation import matcher_abb_name
from pipeline.matcher.matcher_dummy import dummy_matcher_capital
from pipeline.matcher.matcher_sixteen_small_letter import small_letter_matcher
from pipeline.session import get_session
from fonduer.parser.models import Document


def extract_mentions(db_name: str):

    assert db_name, "db_name is necessary"  
    session = get_session(db_name=db_name)

    docs = session.query(Document).all()

    mention_extractor = MentionExtractor(
        session,
        [NameAbbr, NameFull, Task]
        [nameAbbrv_ngrams, nameFull_ngrams, task_sentences]
        [matcher_abb_name, dummy_matcher_capital, small_letter_matcher]
    )

    mention_extractor.apply(docs, parallelism=4)


if __name__ == '__main__':
    extract_mentions("dummy_db")