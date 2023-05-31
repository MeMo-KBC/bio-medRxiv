from fonduer.meta import Meta


def get_fonduer_candidates(session, candidate_class):
    return session.query(candidate_class).all()