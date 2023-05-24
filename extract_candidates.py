from fonduer.candidates import CandidateExtractor
from fonduer.parser.models import Document
from pipeline.utils import split_documents, get_session, PARALLEL
from definitions.candidates import NameFullAbbr, NameFullTask
from pipeline.throttler.NameFullTask import NameFullTask_throttlers



def main(db_name: str):
    session = get_session(db_name=db_name)
    candidate_extractor = CandidateExtractor(
                                    session,
                                    [NameFullAbbr,NameFullTask], #NameFullAbbr,
                                    throttlers=NameFullTask_throttlers,
                                )
    
    # for split, docs in enumerate(split_documents(session)):
    for split, docs in enumerate(session.query(Document).all()): 
        docs = [docs]
        print(f"\nSplit {split}: {len(docs)} documents")
        candidate_extractor.apply(docs, split=split, parallelism=PARALLEL)
        print(f"Split {split}: Number of NameFull + NameAbbrv candidates:", session.query(NameFullAbbr).filter(NameFullAbbr.split==split).count())
        print(f"Split {split}: Number of NameFull + Task candidates:", session.query(NameFullTask).filter(NameFullTask.split==split).count())


if __name__ == "__main__":
    main(db_name="jkracht")