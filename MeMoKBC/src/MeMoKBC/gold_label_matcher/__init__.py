from dataclasses import dataclass
import json


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
    



