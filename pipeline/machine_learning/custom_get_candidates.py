from fonduer.candidates.models import Candidate

def custom_get_candidates(session, split, candidate_list):

    result = []

    for candidate_class in candidate_list:
        # Filter by candidate_ids in a particular split
        sub_query = (session.query(Candidate.id).filter(Candidate.split == split).subquery())
        cands = (session.query(candidate_class).filter(candidate_class.id.in_(sub_query)).order_by(candidate_class.id).all())
        
        result.append(cands)

    return result