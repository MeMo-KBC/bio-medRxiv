from LabelstudioToFonduer.to_label_studio import ToLabelStudio
import logging
import json
from fonduer.candidates import CandidateExtractor
from fonduer.parser.models import Document
from pipeline.utils import split_documents, get_session, PARALELL
from definitions.candidates import NameFullAbbr, NameFullTask
from pipeline.throttler.random_throttler import throt_rand

session = get_session(db_name="testrun")
candidate_extractor = CandidateExtractor(
                                    session,
                                    [NameFullAbbr, NameFullTask],
                                    throttlers=None,
                                )
    
    # for split, docs in enumerate(split_documents(session)):
for split, docs in enumerate(session.query(Document).all()): 
    docs = [docs]
    print(f"\nSplit {split}: {len(docs)} documents")
    candidate_extractor.apply(docs, split=split, parallelism=PARALELL)
    print(f"Split {split}: Number of NameFull + NameAbbrv candidates:", session.query(NameFullAbbr).filter(NameFullAbbr.split==split).count())
    print(f"Split {split}: Number of NameFull + Task candidates:", session.query(NameFullTask).filter(NameFullTask.split==split).count())

train_cands = candidate_extractor.get_candidates()

converter = ToLabelStudio()

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)

export = converter.create_export(candidates=train_cands)

#print(json.dumps(export[0]["annotations"], indent=4))

output_data = export[0]["annotations"]

output_file = "output.json"

with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=4)

print(f"JSON data saved to {output_file}")