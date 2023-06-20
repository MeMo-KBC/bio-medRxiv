from dataclasses import dataclass
import json
from MeMoKBC.definitions.candidates import NameFullAbbr, NameAbbrTask
from MeMoKBC.definitions.mentions.mention_subclasses import NameAbbr
from MeMoKBC.pipeline.utils import get_session
from fonduer.candidates.models import Candidate
from fonduer.meta import Meta
from fonduer.supervision.models import GoldLabel
from typing import Union
import logging


@dataclass
class Annotation:
    id: str
    label: str
    start: str
    end: str
    startOffset: int
    endOffset: int
    globalOffsetStart: int
    globalOffsetEnd: int
    text: str


    @staticmethod
    def from_dict(d):
        return Annotation(
            id=d["id"],
            label=d["value"]["hypertextlabels"][0],
            start=d["value"]["start"],
            end=d["value"]["end"],
            startOffset=d["value"]["startOffset"],
            endOffset=d["value"]["endOffset"],
            globalOffsetStart=d["value"]["globalOffsets"]["start"],
            globalOffsetEnd=d["value"]["globalOffsets"]["end"],
            text=d["value"]["text"]
        )

    @staticmethod
    def from_doc_dict(doc_dict):
        annotations = []
        for annotation in doc_dict["annotations"][0]["result"]:
            if annotation["type"] == "hypertextlabels":
                annotations.append(Annotation.from_dict(annotation))
        return annotations

@dataclass
class Relation:
    from_annotation: Annotation
    to_annotation: Annotation
    direction: str


    def _generate_annotation_dict(annotations: "list[Annotation]"):
        return {annotation.id: annotation for annotation in annotations}
    
    @staticmethod
    def generate_from_project_json(fn):
        json_data = json.load(open(fn))
        documents_relations = {}
        for doc_dict in json_data:
            document_relations = []
            file_name = doc_dict["file_upload"].split("-")[-1].rstrip(".html")
            annotations = Annotation.from_doc_dict(doc_dict)
            annotations_dict = Relation._generate_annotation_dict(annotations)
            relations_list = [relation_dict for relation_dict in doc_dict["annotations"][0]["result"] if relation_dict["type"] == "relation"]
            for relation_dict in relations_list:
                document_relations.append(Relation(
                    from_annotation=annotations_dict[relation_dict["from_id"]],
                    to_annotation=annotations_dict[relation_dict["to_id"]],
                    direction=relation_dict["direction"]
                ))
            documents_relations[file_name] = document_relations
        return documents_relations
    


def match_gold_label(db_name: str, project_json_path: str, candidates: "Union[list[Candidate], Candidate]"):
    logging.basicConfig(level=logging.INFO)

    if type(candidates) != list:
        candidates = [candidates]

    session = get_session(db_name)

    relations_per_doc = Relation.generate_from_project_json(project_json_path)    
    logging.info(f"Found relations for {len(relations_per_doc.keys())} documents")

    candidates_list = []
    for cand in candidates:
        candidates_list.extend(session.query(cand).all())
        logging.info("Found " + str(len(candidates_list)) + " candidates for " + str(cand))


    candidates_by_doc_name = {}
    for candidate in candidates_list:
        if candidate.document.name not in candidates_by_doc_name.keys():
            candidates_by_doc_name[candidate.document.name] = []
        candidates_by_doc_name[candidate.document.name].append(candidate)

    logging.info(f"Found candidates for {len(candidates_by_doc_name.keys())} documents")

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

    for document_id in list(relations_per_doc.keys()):
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

    return gold_labels
