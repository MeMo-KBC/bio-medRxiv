from fonduer.meta import Meta
from fonduer.parser.preprocessors import HTMLDocPreprocessor
from fonduer.parser import Parser


def doc_parser(session, docs_path: str, parallel: int=12):
    
    doc_preprocessor = HTMLDocPreprocessor(docs_path)
    corpus_parser = Parser(session, structural=True, lingual=True)
    corpus_parser.apply(doc_preprocessor, parallelism=parallel)