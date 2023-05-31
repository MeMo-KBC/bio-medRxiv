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

export = json.load(open("project-30.json"))

numbers_per_document = []

for document in export:
    data = document["data"]
    phone_numbers = []
    doc_id = document['file_upload']

    for match in document["annotations"][0]["result"]:
        if "value" not in match.keys():
            continue
        if any("Author short" == label for label in match["value"]["hypertextlabels"]):
            try:
                phone_number = match["value"]["text"]
                phone_numbers.append(phone_number)
            except:
                # print(match)
                continue
        else:
            continue
    numbers_per_document.append(
        (data, phone_numbers, doc_id)
    )


all_precisions = []
all_recalls = []

for document, phone_numbers, doc_id in numbers_per_document:
    soup = BeautifulSoup(str(document), features="html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)


    # pprint(text)
    matches = phone_matcher_new.findall(text)

    matches_unique = set(matches)
    phone_numbers_unique = set(phone_numbers)

    correct_found = phone_numbers_unique.intersection(matches_unique)
    false_found = matches_unique - phone_numbers_unique

    try:
        recall = len(correct_found) / len(phone_numbers_unique)
        precision = len(phone_numbers_unique) / len(matches_unique) 

        all_precisions.append(precision)
        all_recalls.append(recall)

        if recall != 1:
            print("Name_Shorts not found in doc:", doc_id, phone_numbers_unique - correct_found)
    except ZeroDivisionError:  
        continue

try:
    print("\nAverage prec.", sum(all_precisions) / len(all_precisions))
except ZeroDivisionError:
    print("\nAverage prec.", sum(all_precisions) / 1)

try:
    print("Average rec.", sum(all_recalls) / len(all_recalls))
except ZeroDivisionError:
    print("Average rec.", sum(all_recalls) / 1)
