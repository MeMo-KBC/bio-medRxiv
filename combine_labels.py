import json
from pathlib import Path

def combine(iterpaths, save_path):

    # get all jsons from directories
    all_jsons = []
    for path in iterpaths:
        path = Path(path)
        jsons = [f for f in path.iterdir() if f.is_file() and f.suffix == ".json"]
        all_jsons.extend(jsons)
    

    # combine jsons
    json_combined = []
    raw_jsons = [json.load(open(f, "r")) for f in all_jsons]
    for raw_json in raw_jsons:
        json_combined.extend(raw_json)

    with open(save_path, "w") as f:
        json.dump(json_combined, f, indent=4)
    

if __name__ == "__main__":
    iterpaths = [
        "/data/Goldlabel_biomedRxiv/zgoldlabel_complete/all_candidates",
        "/data/Goldlabel_biomedRxiv/zgoldlabel_complete/short_task",
    ]
    combine(iterpaths, save_path="/data/Goldlabel_biomedRxiv/zgoldlabel_complete/combined/GoldLabels.json")