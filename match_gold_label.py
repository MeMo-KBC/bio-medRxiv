from MeMoKBC.gold_label_matcher import Relation, Annotation
from MeMoKBC.definitions.candidates import NameAbbrTask
from MeMoKBC.definitions.mentions.mention_subclasses import NameAbbr
from fonduer.meta import Meta
from fonduer.supervision.models import GoldLabel


db_name = "match_goldlabel"
conn_str = 'postgresql://postgres@fonduer-postgres-dev:5432/' + db_name
session = Meta.init(conn_string=conn_str).Session()


relations_per_doc = Relation.generate_from_project_json("/data/label_studio_export.json")    
# print(relations)


candidates = session.query(NameAbbrTask).all()


candidates_by_doc_name = {}
for candidate in candidates:
    if candidate.document.name not in candidates_by_doc_name.keys():
        candidates_by_doc_name[candidate.document.name] = []
    candidates_by_doc_name[candidate.document.name].append(candidate)


document_id = "10.1101.001768"
name_abbr = session.query(NameAbbr).all()


# print(relations[document_id])


# prefilter out all candidates without relations text

def cand_contains_relation_text(cand, gold_set):
    cand_1, cand_2 = list(cand)
    cand_1_text = cand_1.context.get_span()
    cand_2_text = cand_2.context.get_span()
    return (cand_1_text, cand_2_text ) in gold_set #  or (cand_2_text, cand_1_text) in gold_set

gold_labels = []

for document_id in relations_per_doc.keys():
    cands = candidates_by_doc_name[document_id]
    rels = relations_per_doc[document_id]
    gold_set = set()
    for rel in rels:
        gold_set.add((rel.from_annotation.text, rel.to_annotation.text))
    cands_filtered = [cand for cand in cands if cand_contains_relation_text(cand, gold_set)]
    gold_labels.extend(cands_filtered)
    

print(gold_labels)