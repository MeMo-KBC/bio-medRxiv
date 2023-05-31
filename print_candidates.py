from fonduer.candidates import CandidateExtractor
from fonduer.parser.models import Document
from pipeline.utils import split_documents, get_session, PARALLEL
from definitions.candidates import NameFullAbbr, NameFullTask
from pipeline.throttler.random_throttler import throt_rand



def main(db_name: str):
    session = get_session(db_name=db_name)

    
    # for split, docs in enumerate(split_documents(session)):
    for split, docs in enumerate(session.query(Document).all()): 
        docs = [docs]

        full_short = session.query(NameFullAbbr)
        
        full_short_list = []

        for x in full_short:
            full_short_list.append([x[0][0].get_span(), x[1][0].get_span()])
        
        #full_short_set = set(full_short_list)

        print(full_short_list)


if __name__ == "__main__":
    main(db_name="test_collection")