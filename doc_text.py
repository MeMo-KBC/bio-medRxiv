import re
import json
from bs4 import BeautifulSoup
from pprint import pprint

# # First Test Run
phone_matcher_oldold = re.compile(r"[A-Z][\'.-]?[\s]?[A-Z][\'.-]?[aA-zZ]?[\'.-]?[aA-zZ]?[\'.-]?[aA-zZ]?")
# phone_matcher_old = re.compile(r"[A-Z][a-z][\'.-][A-Z][\'.-]?[aA-zZ]*")

# Second Test Run
phone_matcher_new = re.compile(r"[\s]?[A-Z][\'.-]?[\s]?[A-Z][\'.-]?[aA-zZ]?[\'.-]?[aA-zZ]?[\'.-]?[aA-zZ]*[\'.-]?[\s]?")
phone_matcher_old = re.compile(r"[A-Z][a-z][\'.-]?[a-z]?[A-Z][\'.-]?[aA-zZ]*")

def n_lower_chars(string):
    return sum(1 for c in string if c.islower())

export = json.load(open("project-30.json"))
phone_numbers = []
maxi = 0

for document in export:
    data = document["data"]
    doc_id = document['file_upload']

    for match in document["annotations"][0]["result"]:
        if "value" not in match.keys():
            continue
        if any("Author short" == label for label in match["value"]["hypertextlabels"]):
            try:
                abbrev = match["value"]["text"]
                if len(abbrev) > maxi:
                    print(maxi)
                    print(abbrev)
                    user_input = input('zählt?')
                    if user_input == 'y':
                        maxi = len(abbrev)
                    else:
                        continue
                phone_numbers.append(abbrev)
            except:
                continue
