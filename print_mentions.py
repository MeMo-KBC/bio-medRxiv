from fonduer.candidates import CandidateExtractor
from fonduer.parser.models import Document
from pipeline.utils import split_documents, get_session, PARALLEL
from definitions.mentions.mention_subclasses import NameAbbr, NameFull
from pipeline.throttler.random_throttler import throt_rand



def main(db_name: str):
    session = get_session(db_name=db_name)

    
    # for split, docs in enumerate(split_documents(session)):
    for split, docs in enumerate(session.query(Document).all()): 
        docs = [docs]

        name_short = session.query(NameAbbr)
        name_long = session.query(NameFull)
        
        name_short_list = []

        for x in name_short:
            for y in x:
                name_short_list.append(y.get_span())
        
        name_short_set = set(name_short_list)

        name_long_list = []

        for x in name_long:
            for y in x:
                name_long_list.append(y.get_span())
                                      
        name_long_set = set(name_long_list)

        print(name_short_set)
        print(name_long_set)


if __name__ == "__main__":
    main(db_name="test_collection")