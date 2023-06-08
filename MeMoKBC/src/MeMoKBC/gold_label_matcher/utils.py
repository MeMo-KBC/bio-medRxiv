from fonduer.meta import Meta


from MeMoKBC.gold_label_matcher import Relation, Annotation
from MeMoKBC.definitions.candidates import NameFullAbbr
from MeMoKBC.definitions.mentions.mention_subclasses import NameAbbr
from MeMoKBC.pipeline.utils import get_session
from fonduer.candidates.models import Candidate
from fonduer.meta import Meta
from fonduer.supervision.models import GoldLabel
from typing import Union
import logging

def match_gold_label(db_name: str, project_json_path: str, candidates: "Union[list[Candidate], Candidate]"):
    logging.basicConfig(level=logging.INFO)

    if type(candidates) != list:
        candidates = [candidates]

    session = get_session(db_name)

    relations_per_doc = Relation.generate_from_project_json(project_json_path)    
    
    candidates_list = []
    for cand in candidates:
        candidates_list.extend(session.query(cand).all())
        logging.info("Found " + str(len(candidates_list)) + " candidates for " + str(cand))


    candidates_by_doc_name = {}
    for candidate in candidates_list:
        if candidate.document.name not in candidates_by_doc_name.keys():
            candidates_by_doc_name[candidate.document.name] = []
        candidates_by_doc_name[candidate.document.name].append(candidate)

    def add_whitespace(annotation_text: str):
        """Adds whitespaces before capital letters, only needed for long author names"""
        whitespaces_to_add = []
        for i, char in enumerate(annotation_text):
            if i == 0:
                continue
            if char.isupper() and annotation_text[i-1] != " ":
                whitespaces_to_add.append(i)
            
        for i in reversed(whitespaces_to_add):
            annotation_text = annotation_text[:i] + " " + annotation_text[i:]
        
        return annotation_text

    def cand_contains_relation_text(cand: Candidate, gold_set: set):
        """Checks if the candidate is present in the gold set"""
        cand_1, cand_2 = list(cand)
        cand_1_text = cand_1.context.get_span()
        cand_2_text = cand_2.context.get_span()
        return (cand_1_text, cand_2_text ) in gold_set or (cand_2_text, cand_1_text) in gold_set

    gold_labels = []

    for document_id in list(relations_per_doc.keys())[1:]:
        if document_id not in candidates_by_doc_name.keys():
            logging.warning("Document not found in candidates: " + document_id)
            continue

        cands = candidates_by_doc_name[document_id]
        rels = relations_per_doc[document_id]
        
        gold_set = set()
        for rel in rels:
            from_annotation = rel.from_annotation
            to_annotation = rel.to_annotation
            if from_annotation.label == "Author long":
                from_annotation.text = add_whitespace(from_annotation.text)
            if to_annotation.label == "Author long":
                to_annotation.text = add_whitespace(to_annotation.text)

            gold_set.add((rel.from_annotation.text, rel.to_annotation.text))

        cands_filtered = [cand for cand in cands if cand_contains_relation_text(cand, gold_set)]
        gold_labels.extend(cands_filtered)
        break

    return gold_labels


