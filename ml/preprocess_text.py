import os
import re
import json
from config import SYMPTOM_DIR, DATA_DIR

DISEASE_SYMPTOM_MAP = {
    "Tomato___Late_blight": [
        "dark brown spots on tomato leaves",
        "water soaked lesions on leaves",
        "white mold on underside of tomato leaf",
        "tomato leaves turning brown and dying",
        "irregular brown patches on tomato plant",
        "tomato plant wilting with brown lesions",
        "grayish white growth on tomato leaves",
        "tomato stems turning black and rotting",
        "brown patches spreading fast on tomato",
        "tomato leaves look burned and wet",
        "mushy brown spots on tomato fruit",
        "tomato plant collapsing from base",
        "dark water soaked areas on tomato stem",
        "tomato foliage dying from tips inward",
        "fuzzy white coating under tomato leaf"
    ],
    "Tomato___Early_blight": [
        "dark spots with yellow rings on tomato",
        "concentric ring pattern on tomato leaf",
        "lower tomato leaves turning yellow and brown",
        "brown lesions with target pattern on tomato",
        "tomato leaves have bullseye shaped spots",
        "older tomato leaves dropping off early",
        "dark brown circular spots on tomato",
        "yellow halo around brown spots on tomato",
        "tomato leaf edges turning brown and dry",
        "small dark spots growing larger on tomato",
        "tomato plant losing leaves from bottom up",
        "irregular dark lesions on tomato foliage",
        "tomato leaves show angular brown patches",
        "dry brown spots with rings on tomato leaf",
        "tomato plant defoliating due to brown spots"
    ],
    "Apple___Apple_scab": [
        "dark olive green spots on apple leaves",
        "scabby lesions on apple fruit",
        "apple leaves curling and falling early",
        "velvety spots on apple leaf surface",
        "black crusty patches on apple skin",
        "apple fruit cracking with dark spots",
        "apple leaves have smoky gray patches",
        "rough corky spots on apple fruit",
        "apple tree dropping leaves in summer",
        "dark feathery spots on young apple leaves",
        "apple fruit deformed with scab patches",
        "olive brown velvety coating on apple leaf",
        "apple leaves puckering and twisting",
        "small circular dark spots on apple leaves",
        "apple fruit surface rough and discolored"
    ],
    "Apple___Black_rot": [
        "brown circular lesions on apple leaves",
        "black rotting spots on apple fruit",
        "purple bordered spots on apple leaf",
        "frog eye pattern on apple leaves",
        "apple fruit shriveling and turning black",
        "apple bark cracking with orange discoloration",
        "reddish purple spots on apple foliage",
        "apple fruit mummifying on tree",
        "circular tan spots with purple border on apple",
        "apple leaves yellowing with brown spots",
        "black sunken lesions on apple fruit",
        "apple cankers on branches and twigs",
        "apple fruit rotting from core outward",
        "dark brown rings on apple fruit surface",
        "apple leaves dropping with purple spots"
    ],
    "Corn___Common_rust": [
        "orange rust pustules on corn leaves",
        "reddish brown powder on corn leaf surface",
        "corn leaves turning yellow with rust spots",
        "small oval brown spots on maize leaves",
        "brick red pustules scattered on corn",
        "corn leaf surface rough with rust bumps",
        "maize leaves covered in orange powder",
        "corn plant showing rust colored streaks",
        "both sides of corn leaf have rust spots",
        "corn leaves turning pale with orange dots",
        "rust pustules breaking open on corn leaf",
        "maize plant stunted with rust infection",
        "corn leaves have elongated rust pustules",
        "orange to brown powdery spots on corn",
        "corn field showing widespread rust symptoms"
    ],
    "Potato___Late_blight": [
        "dark water soaked spots on potato leaves",
        "white fuzzy growth under potato leaves",
        "potato plant collapsing and turning brown",
        "brown lesions spreading quickly on potato",
        "potato tubers showing dark rot inside",
        "potato stems turning black at base",
        "potato leaves wilting despite watering",
        "gray green water soaked patches on potato",
        "potato plant dying rapidly from top down",
        "white cottony growth on underside of potato leaf",
        "potato leaves turning black and mushy",
        "entire potato plant browning within days",
        "potato foliage smells bad and rots",
        "dark sunken patches on potato tuber skin",
        "potato field showing rapid disease spread"
    ],
    "Grape___Black_rot": [
        "brown circular spots on grape leaves",
        "black shriveled grape berries",
        "tan lesions with dark borders on grape leaf",
        "grape leaves with reddish brown spots",
        "grape berries turning black and hard",
        "small black dots visible inside grape lesions",
        "grape vine leaves showing irregular brown patches",
        "grape clusters with mummified black berries",
        "reddish brown spots on young grape shoots",
        "grape leaves yellowing around brown spots",
        "black rotted grapes remaining on vine",
        "grape leaf edges browning and curling",
        "circular lesions with dark margins on grape",
        "grape fruit shriveling before ripening",
        "brown spots on grape tendrils and shoots"
    ],
    "Healthy": [
        "plant looks healthy and green",
        "no spots or lesions on leaves",
        "leaves are fresh and normal colored",
        "plant is growing well with no disease signs",
        "vibrant green leaves with no discoloration",
        "plant has lush foliage and strong stems",
        "no wilting or yellowing observed on plant",
        "leaves are smooth with no spots or patches",
        "plant growing normally with no symptoms",
        "healthy green plant with no visible issues",
        "no abnormal growth or discoloration seen",
        "plant leaves are firm and fully green",
        "crop looks normal and disease free",
        "no rust spots mold or rot on plant",
        "plant appears vigorous and fully healthy"
    ]
}



def clean_text(text):
    """Basic text cleaning."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)   # remove special chars
    text = re.sub(r"\s+", " ", text)            # collapse whitespace
    return text

def build_corpus():
    """
    Convert disease-symptom map into a labeled corpus
    ready for BERT fine-tuning.
    Format: list of {"text": ..., "label": ..., "label_id": ...}
    """
    os.makedirs(SYMPTOM_DIR, exist_ok=True)

    labels     = sorted(DISEASE_SYMPTOM_MAP.keys())
    label2id   = {label: idx for idx, label in enumerate(labels)}
    corpus     = []

    for disease, symptoms in DISEASE_SYMPTOM_MAP.items():
        for symptom in symptoms:
            corpus.append({
                "text"     : clean_text(symptom),
                "label"    : disease,
                "label_id" : label2id[disease]
            })

    # Save corpus as JSON
    corpus_path = os.path.join(SYMPTOM_DIR, "symptom_corpus.json")
    with open(corpus_path, "w") as f:
        json.dump(corpus, f, indent=2)

    # Save label mapping
    label_map_path = os.path.join(SYMPTOM_DIR, "label_map.json")
    with open(label_map_path, "w") as f:
        json.dump(label2id, f, indent=2)

    print(f" Corpus built: {len(corpus)} entries across {len(labels)} diseases")
    print(f" Saved to: {corpus_path}")
    print(f" Label map saved to: {label_map_path}")
    return corpus, label2id

if __name__ == "__main__":
    print("=" * 50)
    print("  PlantDocBot — Text Corpus Preparation")
    print("=" * 50)
    build_corpus()