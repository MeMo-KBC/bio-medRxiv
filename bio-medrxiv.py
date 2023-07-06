import plac
from MeMoKBC.pipeline.utils import create_db, get_session
from MeMoKBC.scripts.doc_parser import doc_parser
from MeMoKBC.scripts.extract_mentions import extract_mentions
from MeMoKBC.scripts.extract_candidates import extract_candidates
from MeMoKBC.scripts.extract_features import extract_features
from MeMoKBC.scripts.apply_lf import apply_lf
from pathlib import Path


@plac.annotations(
    # arg=(helptext, kind, abbrev, type, choices, metavar)
    db_name=("What db to use", "positional", None, str, None, "db_name"),
    create_db_arg=("Create db", "flag", "c", None, None, None),
    parse_documents_folder=("Parse documents in following folder", "option", "f", Path, None, "folder"),
    extract_mentions_arg=("Extract mentions", "flag", "M", None, None, None),
    extract_candidates_arg=("Extract candidates", "flag", "C", None, None, None),
    extract_features_arg=("Extract features", "flag", "F", None, None, None),
    apply_lfs_arg=("Apply label functions", "flag", "L", None, None, None),
    debug=("Enable debug mode", "flag", "d", None, None, None)
)
def main(db_name, create_db_arg, parse_documents_folder, extract_mentions_arg, extract_candidates_arg, extract_features_arg, apply_lfs_arg, debug):
    '''Main script for calling all functions'''
   
    if debug:
        print("No debug mode implemented yet")
        exit()

    if create_db_arg:
        create_db(db_name)
        print("Created db:", db_name)

    session = get_session(db_name)

    # TODO add check if any documents are in db
    if parse_documents_folder:    
        doc_parser(session, parse_documents_folder)
        print("Parsed documents")
    
    if extract_mentions_arg:
        extract_mentions(session, 25)
        print("Extracted mentions")

    if extract_candidates_arg:
        extract_candidates(session, 25)
        print("Extracted candidates")
    
    if extract_features_arg:
        extract_features(session, 25)
        print("Extracted features")

    if apply_lfs_arg:
        apply_lf(session, 25)
        print("Applied label functions")



"""
@plac.annotations(arg=("What db to use", str, None, 'db_name'))
@plac.flg("create_db", "Create db", abbrev="b")
@plac.opt("parse_documents_folder", "Parse documents in following folder", type=str)
@plac.flg('extract_mentions', "Extract mentions", abbrev="m")
@plac.flg('extract_candidates', "Extract candidates", abbrev="c")
@plac.flg('extract_features', "Extract features", abbrev="f")
@plac.flg('apply_lfs', "Apply label functions", abbrev="l")
@plac.flg("debug", "Enable debug mode", abbrev="d")
def main(db_name, create_db, parse_documents_folder, extract_mentions, extract_candidates, extract_features, apply_lfs, debug):
    '''Main script for calling all functions'''
    if debug:
        print("No debug mode implemented yet")
        exit()

    if create_db:
        scripts.create_db.create_db(db_name)
        print("Created db:", db_name)

    session = get_session(db_name)


    if parse_documents_folder:
        scripts.doc_parser.doc_parser(session, parse_documents_folder)
        print("Parsed documents")
    
    if extract_mentions:
        scripts.extract_mentions.extract_mentions(session)
        print("Extracted mentions")

    if extract_candidates:
        scripts.extract_candidates.extract_candidates(session)
        print("Extracted candidates")
    
    if extract_features:
        scripts.extract_features.extract_features(session)
        print("Extracted features")

    if apply_lfs:
        scripts.apply_lf.apply_lf(session)
        print("Applied label functions")

"""

if __name__ == "__main__":
    plac.call(main)