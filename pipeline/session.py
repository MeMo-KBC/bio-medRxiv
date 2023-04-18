from fonduer.meta import Meta


def get_session(db_name: str):
    conn_str = 'postgresql://localhost:5432/' + db_name
    return Meta.init(conn_string=conn_str).Session()