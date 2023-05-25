from pipeline.utils import get_session
from fonduer.meta import Meta
from fonduer.parser.preprocessors import HTMLDocPreprocessor
from fonduer.parser import Parser
from pipeline.utils import PARALELL


def main(db_name: str):
    session = get_session(db_name)

    docs_path = "data"
    doc_preprocessor = HTMLDocPreprocessor(docs_path)
    corpus_parser = Parser(session, structural=True, lingual=True)
    corpus_parser.apply(doc_preprocessor, parallelism=PARALELL)


if __name__ == '__main__':
    main("testrun")