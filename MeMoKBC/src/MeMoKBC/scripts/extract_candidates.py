from fonduer.candidates import CandidateExtractor
from fonduer.parser.models import Document

from MeMoKBC.definitions.candidates import NameFullAbbr, NameAbbrTask
from MeMoKBC.pipeline.utils import split_documents
from MeMoKBC.pipeline.throttler.name_shortlong_throttler import name_shortlong_throttler



def extract_candidates(session, split: "tuple[float, float]"=(0.33, 0.66), parallel: int=12):
    candidate_extractor = CandidateExtractor(
                                    session,
                                    [NameAbbrTask, NameFullAbbr],
                                    throttlers=[None, name_shortlong_throttler],
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
