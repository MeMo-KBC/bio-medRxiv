from fonduer.meta import Meta
from fonduer.parser.models import Document
from fonduer.candidates.models import Candidate
from fonduer.supervision.models import LabelKey
from fonduer.supervision.labeler import Labeler
import psycopg2
import numpy as np


def create_db(db_name: str):
    conn=psycopg2.connect(
        host="fonduer-postgres-dev",
        user="postgres",
        port="5432",
    )
    conn.autocommit = True
    cur = conn.cursor()
    sql = f"""CREATE DATABASE {db_name};"""
    cur.execute(sql)
    conn.close()

PARALLEL = 1

def get_session(db_name: str):
    conn_str = 'postgresql://postgres@fonduer-postgres-dev:5432/' + db_name
    return Meta.init(conn_string=conn_str).Session()


def split_documents(session, splits: "tuple[float, float]"):
    docs = session.query(Document).all()
    ld = len(docs)

    train_docs = set()
    dev_docs = set()
    test_docs = set()

    data = [(doc.name, doc) for doc in docs]
    data.sort(key=lambda x: x[0])
    for i, (_, doc) in enumerate(data):
        if i < splits[0] * ld:
            train_docs.add(doc)
        elif i < splits[1] * ld:
            dev_docs.add(doc)
        else:
            test_docs.add(doc)
    return train_docs, dev_docs, test_docs

def load_candidates(session, split: int, candidate_list):

    result = []

    for candidate_class in candidate_list:
        result.append(session.query(candidate_class).filter(candidate_class.split == split).all())
    return result


def match_label_matrix(session: Meta, candidates: "list[Candidate]", split: int) -> "list[np.ndarray]":
    """Get the label matrix for a set of candidates. And reduce the label matrix to the columns corresponding to the candidate classes."""
    labeler = Labeler(session, candidates)
    train_cands = load_candidates(session, split, candidates)
    L_train = labeler.get_label_matrices(train_cands)
    lfs = session.query(LabelKey).all()
    lfs_classes = np.array([lf.candidate_classes[0] for lf in lfs])
    matricies = []
    for candidate, L_train_cand in zip(candidates, L_train):
        cand_name = candidate.__tablename__
        mask = np.where(lfs_classes == cand_name)[0].tolist()
        matricies.append(L_train_cand[:, mask])
    return matricies