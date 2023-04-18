
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
        file_dir = os.path.join(dir_of_files_bio, f)
        # html-file is hase the same name as the folder
        file_name = f+".html"
        # create path to html-file
        html_file_bio = os.path.join(file_dir, file_name)
        
        # copy file into directory for extracted files
        if os.path.exists(html_file_bio):
            shutil.copy(html_file_bio, dir_to_extract)


    ### extract med html-files
    # list of folders
    folderlist_med = [ f for f in os.listdir(dir_of_files_med)]
    # loop array with folder names
    for f in folderlist_med:
        # create path to folder
        file_dir = os.path.join(dir_of_files_med, f)
        # html-file is hase the same name as the folder
        file_name = f+".html"
        # create path to html-file
        html_file_med = os.path.join(file_dir, file_name)

        # copy file into directory for extracted files
        if os.path.exists(html_file_med):
            shutil.copy(html_file_med, dir_to_extract)

if "__main__" == __name__:
    extract_html_files("/data/rxiv_publications_extracted", "/data/rxiv_publications/bio", "/data/rxiv_publications/med")