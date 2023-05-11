import os

project_name = "biorxiv"
conn_string = "postgresql://postgres@fonduer-postgres-dev:5432/"

dataset_path = "data/"
export_path = os.path.join(dataset_path, "snapshot1.json")
documents_path = os.path.join(dataset_path, "converted")


from LabelstudioToFonduer.to_fonduer import parse_export
export = parse_export(export_path)

from LabelstudioToFonduer.fonduer_tools import save_create_project
save_create_project(conn_string=conn_string, project_name=project_name)


from fonduer import Meta, init_logging
init_logging(log_dir=os.path.join(dataset_path, "logs"))
session = Meta.init(conn_string + project_name).Session()

from LabelstudioToFonduer.document_processor import My_HTMLDocPreprocessor
from fonduer.parser import Parser
doc_preprocessor = My_HTMLDocPreprocessor(documents_path, max_docs=100)

from LabelstudioToFonduer.lingual_parser import ModifiedSpacyParser
exceptions = [".NET", "Sr.", ".WEB", ".de", "Jr.", "Inc.", "Senior.", "p.", "m."]
my_parser = ModifiedSpacyParser(lang="en", split_exceptions=exceptions)

corpus_parser = Parser(session, 
    lingual_parser=my_parser, 
    structural=True, 
    lingual=True, 
    flatten=[])
    
corpus_parser.apply(doc_preprocessor, parallelism=8)

from fonduer.parser.models import Document, Sentence

print(f"Documents: {session.query(Document).count()}")
print(f"Sentences: {session.query(Sentence).count()}")

docs = session.query(Document).order_by(Document.name).all()

from fonduer.candidates.models import mention_subclass
Title = mention_subclass("Title")
Date = mention_subclass("Date")


from fonduer.candidates import MentionNgrams
title_ngrams = MentionNgrams(n_max=export.ngrams("Author short")[1] + 5, n_min=export.ngrams("Author short")[0])
date_ngrams = MentionNgrams(n_max=export.ngrams("Author long")[1] + 5, n_min=export.ngrams("Author long")[0])


from fonduer.candidates.matchers import LambdaFunctionMatcher
title = export.lable_entitis("Author short")
date = export.lable_entitis("Author long")


def is_title(mention):
    if mention.get_span() in title:
        return True
    else:
        False


def is_date(mention):
    if mention.get_span() in date:
        return True
    else:
        False


title_matcher = LambdaFunctionMatcher(func=is_title)
date_matcher = LambdaFunctionMatcher(func=is_date)


from fonduer.candidates import MentionExtractor
mention_extractor = MentionExtractor(
    session,
    [Title, Date],
    [title_ngrams, date_ngrams],
    [title_matcher, date_matcher],
)


from fonduer.candidates.models import Mention
mention_extractor.apply(docs)
num_title = session.query(Title).count()
num_date = session.query(Date).count()

print(f"Total Mentions: {session.query(Mention).count()} ({num_title} titles, {num_date} dates)")


from fonduer.candidates.models import candidate_subclass
TitleDate = candidate_subclass("TitleDate", [Title, Date])


from fonduer.candidates import CandidateExtractor
candidate_extractor = CandidateExtractor(session, [TitleDate])
candidate_extractor.apply(docs)

from LabelstudioToFonduer.to_fonduer import ToFonduer
converter = ToFonduer(label_studio_export=export, fonduer_session=session)


from fonduer.supervision.models import GoldLabel
from fonduer.supervision import Labeler
labeler = Labeler(session, [TitleDate])

labeler.apply(
    docs=docs,
    lfs=[[converter.is_gold]],
    table=GoldLabel,
    train=True,
    parallelism=8,
)