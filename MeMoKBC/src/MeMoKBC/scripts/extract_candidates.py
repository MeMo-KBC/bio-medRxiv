from fonduer.candidates import CandidateExtractor
from fonduer.parser.models import Document

from MeMoKBC.definitions.candidates import NameFullAbbr, NameAbbrTask, AllAuthorsTask
from MeMoKBC.pipeline.utils import split_documents
from MeMoKBC.pipeline.throttler.name_shortlong_throttler import name_shortlong_throttler
#from MeMoKBC.pipeline.throttler.NameAbbrTask import are_neighbors
from MeMoKBC.pipeline.throttler.AllAuthorsTask_throt import all_authors_task_throttler
from MeMoKBC.pipeline.throttler.NameAbbrTask import name_mention_in_task_mention_throttler



def extract_candidates(session, split: "tuple[float, float]"=(0.33, 0.66), parallel: int=12):
    candidate_extractor = CandidateExtractor(
                                    session,
                                    [NameAbbrTask, NameFullAbbr, AllAuthorsTask],
                                    throttlers=[name_mention_in_task_mention_throttler, name_shortlong_throttler, all_authors_task_throttler]
                                )
    
    # doc_split = split_documents(session, split)
    doc_split = [session.query(Document).all()]

    for idx, docs in enumerate(doc_split): 
        if type(docs) != list:
            docs = list(docs)
        print(f"\nSplit {idx}: {len(docs)} documents")
        candidate_extractor.apply(docs, split=idx, parallelism=parallel)
        print(f"Split {idx}: Number of NameFull + NameAbbrv candidates:", session.query(NameFullAbbr).filter(NameFullAbbr.split==idx).count())
        print(f"Split {idx}: Number of NameAbbr + Task candidates:", session.query(NameAbbrTask).filter(NameAbbrTask.split==idx).count())
        print(f"Split {idx}: Number of AllAuthors + Task candidates:", session.query(AllAuthorsTask).filter(AllAuthorsTask.split==idx).count())


 # Print AllAuthorsTask candidates
        all_authors_candidates = session.query(AllAuthorsTask).filter(AllAuthorsTask.split == idx).all()
        print(f"\nAllAuthorsTask Candidates:")
        for candidate in all_authors_candidates:
            print(candidate)