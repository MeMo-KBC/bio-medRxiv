from fonduer.meta import Meta
from fonduer.parser.models import Document

PARALLEL = 6

def get_session(db_name: str):
    conn_str = 'postgresql://postgres@fonduer-postgres-dev:5432/' + db_name
    return Meta.init(conn_string=conn_str).Session()


def split_documents(session):
    docs = session.query(Document).all()
    ld = len(docs)

    train_docs = set()
    dev_docs = set()
    test_docs = set()
    splits = (0.7, 0.85)
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