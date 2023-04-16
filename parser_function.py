
# imports
import os, shutil

## Wichtig: bei mir funktioniert der Dev-Container nicht, deshalb konnte nicht bisher getestet werden
# vorher muss rxiv_publications.zip entpackt werden
# je nachdem wo der Ordner ist, müssen die Pfade unten angepasst werden


def extract_html_files(dir_to_extract: str, dir_of_files_bio: str, dir_of_files_med: str):
    """
    Extracts html-files from folder rxiv_publications
    """

    # create directory
    if not os.path.exists(dir_to_extract):
        os.mkdir(dir_to_extract)

    ### extract bio html-files
    # list of folder names
    folderlist_bio = [ f for f in os.listdir(dir_of_files_bio)]
    # loop array with folder names
    for f in folderlist_bio:
        # create path to folder
        file_dir = os.path.join(folderlist_bio, f)
        # html-file is hase the same name as the folder
        file_name = f+".html"
        # create path to html-file
        html_file_bio = os.path.join(file_dir, file_name)
        
        # copy file into directory for extracted files
        if os.path.exists(html_file_bio):
            shutil.copyfile(html_file_bio, dir_to_extract)


    ### extract med html-files
    # list of folders
    folderlist_med = [ f for f in os.listdir(dir_of_files_med)]
    # loop array with folder names
    for f in folderlist_med:
        # create path to folder
        file_dir = os.path.join(folderlist_med, f)
        # html-file is hase the same name as the folder
        file_name = f+".html"
        # create path to html-file
        html_file_med = os.path.join(file_dir, file_name)

        # copy file into directory for extracted files
        if os.path.exists(html_file_med):
            shutil.copyfile(html_file_med, dir_to_extract)



# path strings // path strings may need to be changed depending on the rxiv_publications-folder location
dir_to_extract = "./data"
dir_of_files_bio = "./rxiv_publications/bio"
dir_of_files_med = "./rxiv_publications/med"


def main():
    session = Meta.init(conn_string).Session()
    extract_html_files(dir_to_extract, dir_of_files_bio, dir_of_files_med)

    docs_path = dir_to_extract
    doc_preprocessor = HTMLDocPreprocessor(docs_path)
    corpus_parser = Parser(session, structural=True, lingual=True)
    corpus_parser.apply(doc_preprocessor, parallelism=4)


if __name__ == '__main__':
    main()