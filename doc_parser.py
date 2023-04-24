from pipeline.utils import get_session
from fonduer.meta import Meta
from fonduer.parser.preprocessors import HTMLDocPreprocessor
from fonduer.parser import Parser


def main(db_name):
    PARALLEL = 12
    session = get_session(db_name)

    docs_path = "/data/test_collection"
    doc_preprocessor = HTMLDocPreprocessor(docs_path)
    corpus_parser = Parser(session, structural=True, lingual=True)
    corpus_parser.apply(doc_preprocessor, parallelism=PARALLEL)


if __name__ == '__main__':
    main("test_collection")