import json
import os
from config import SYMPTOM_DIR, MODELS_DIR

# ── Treatment Database ───────────────────────────────────
TREATMENT_DB = {
    "Tomato___Late_blight": {
        "disease_name"   : "Tomato Late Blight",
        "plant"          : "Tomato",
        "severity"       : "High",
        "description"    : "A devastating disease caused by Phytophthora infestans. Spreads rapidly in cool, wet conditions.",
        "symptoms"       : [
            "Dark brown water-soaked spots on leaves",
            "White mold on underside of leaves",
            "Brown rotting stems",
            "Fruit develops firm brown rot"
        ],
        "organic_remedy" : [
            "Remove and destroy infected plant parts immediately",
            "Apply copper-based fungicide spray",
            "Use neem oil spray every 7 days",
            "Improve air circulation around plants",
            "Avoid overhead watering"
        ],
        "chemical_remedy": [
            "Apply Mancozeb 75% WP at 2.5g/liter",
            "Use Metalaxyl + Mancozeb (Ridomil Gold)",
            "Spray Cymoxanil 8% + Mancozeb 64% WP",
            "Apply Dimethomorph based fungicides"
        ],
        "prevention"     : [
            "Use certified disease-free seeds",
            "Plant resistant varieties like Mountain Magic",
            "Rotate crops every season",
            "Avoid planting near potatoes",
            "Apply preventive copper spray before rainy season"
        ],
        "source"         : "USDA Plant Disease Database"
    },
    "Tomato___Early_blight": {
        "disease_name"   : "Tomato Early Blight",
        "plant"          : "Tomato",
        "severity"       : "Medium",
        "description"    : "Caused by Alternaria solani fungus. Common in warm humid conditions.",
        "symptoms"       : [
            "Dark brown spots with concentric rings",
            "Yellow halo around spots",
            "Lower leaves affected first",
            "Defoliation in severe cases"
        ],
        "organic_remedy" : [
            "Remove infected lower leaves",
            "Apply compost tea spray",
            "Use copper fungicide spray",
            "Mulch around base of plant",
            "Spray diluted neem oil weekly"
        ],
        "chemical_remedy": [
            "Apply Chlorothalonil 75% WP",
            "Use Azoxystrobin based fungicide",
            "Spray Mancozeb 75% WP at 2g/liter",
            "Apply Tebuconazole 25.9% EC"
        ],
        "prevention"     : [
            "Use resistant tomato varieties",
            "Avoid working with wet plants",
            "Water at soil level not on leaves",
            "Space plants for good air circulation",
            "Apply balanced fertilizer to strengthen plants"
        ],
        "source"         : "CABI Crop Protection Compendium"
    },
    "Apple___Apple_scab": {
        "disease_name"   : "Apple Scab",
        "plant"          : "Apple",
        "severity"       : "Medium",
        "description"    : "Caused by Venturia inaequalis fungus. Most common apple disease worldwide.",
        "symptoms"       : [
            "Olive green to black velvety spots on leaves",
            "Scabby corky lesions on fruit",
            "Premature leaf drop",
            "Deformed and cracked fruit"
        ],
        "organic_remedy" : [
            "Remove fallen leaves to reduce spore source",
            "Apply sulfur-based fungicide spray",
            "Use copper hydroxide spray",
            "Prune trees for better air circulation",
            "Apply neem oil during early season"
        ],
        "chemical_remedy": [
            "Apply Captan 50% WP at 2.5g/liter",
            "Use Myclobutanil 10% WP",
            "Spray Trifloxystrobin + Tebuconazole",
            "Apply Dodine 65% WP"
        ],
        "prevention"     : [
            "Plant scab resistant varieties like Liberty",
            "Rake and destroy fallen leaves every autumn",
            "Apply dormant oil spray before bud break",
            "Avoid dense planting",
            "Monitor weather for infection periods"
        ],
        "source"         : "Cornell University Plant Disease Diagnostic Clinic"
    },
    "Apple___Black_rot": {
        "disease_name"   : "Apple Black Rot",
        "plant"          : "Apple",
        "severity"       : "High",
        "description"    : "Caused by Botryosphaeria obtusa. Affects fruit, leaves and bark.",
        "symptoms"       : [
            "Purple bordered spots on leaves",
            "Frog-eye leaf spot pattern",
            "Black rotting fruit",
            "Cankers on branches"
        ],
        "organic_remedy" : [
            "Prune out all dead and diseased wood",
            "Remove mummified fruit from tree",
            "Apply copper sulfate spray",
            "Disinfect pruning tools with bleach",
            "Improve tree vigor with proper nutrition"
        ],
        "chemical_remedy": [
            "Apply Captan 50% WP fungicide",
            "Use Thiophanate-methyl 70% WP",
            "Spray Ziram 76% WG",
            "Apply Myclobutanil during pink stage"
        ],
        "prevention"     : [
            "Remove all mummified fruit and dead wood",
            "Maintain tree health with proper fertilization",
            "Avoid wounding trees during pruning",
            "Apply protective fungicide from pink stage",
            "Inspect trees regularly for cankers"
        ],
        "source"         : "Penn State Extension Plant Disease"
    },
    "Corn___Common_rust": {
        "disease_name"   : "Corn Common Rust",
        "plant"          : "Corn / Maize",
        "severity"       : "Medium",
        "description"    : "Caused by Puccinia sorghi fungus. Favored by cool temperatures and high humidity.",
        "symptoms"       : [
            "Brick red oval pustules on both leaf surfaces",
            "Pustules turn dark brown later",
            "Leaves turn yellow and die",
            "Severe infection reduces yield"
        ],
        "organic_remedy" : [
            "Plant early to avoid peak rust season",
            "Remove heavily infected leaves",
            "Apply neem oil spray",
            "Use potassium bicarbonate spray",
            "Ensure proper plant spacing"
        ],
        "chemical_remedy": [
            "Apply Propiconazole 25% EC",
            "Use Azoxystrobin + Propiconazole",
            "Spray Mancozeb 75% WP",
            "Apply Trifloxystrobin based fungicide"
        ],
        "prevention"     : [
            "Plant rust resistant hybrid varieties",
            "Monitor crops regularly from silking stage",
            "Avoid late planting",
            "Rotate crops with non-host plants",
            "Apply foliar fungicide at first sign"
        ],
        "source"         : "University of Illinois Extension"
    },
    "Potato___Late_blight": {
        "disease_name"   : "Potato Late Blight",
        "plant"          : "Potato",
        "severity"       : "High",
        "description"    : "Caused by Phytophthora infestans. Same pathogen that caused Irish Potato Famine.",
        "symptoms"       : [
            "Water-soaked dark spots on leaves",
            "White cottony growth under leaves",
            "Stems turn black and collapse",
            "Tubers show brown dry rot"
        ],
        "organic_remedy" : [
            "Destroy infected plant material immediately",
            "Apply copper-based Bordeaux mixture",
            "Avoid overhead irrigation",
            "Hill up soil around stems",
            "Use biocontrol agent Bacillus subtilis"
        ],
        "chemical_remedy": [
            "Apply Metalaxyl + Mancozeb (Ridomil)",
            "Use Cymoxanil 8% + Mancozeb 64%",
            "Spray Dimethomorph 50% WP",
            "Apply Fluopicolide based fungicide"
        ],
        "prevention"     : [
            "Use certified disease-free seed tubers",
            "Plant resistant varieties like Sarpo Mira",
            "Avoid planting in poorly drained areas",
            "Destroy volunteer potato plants",
            "Apply preventive fungicide before wet season"
        ],
        "source"         : "International Potato Center (CIP)"
    },
    "Grape___Black_rot": {
        "disease_name"   : "Grape Black Rot",
        "plant"          : "Grape",
        "severity"       : "High",
        "description"    : "Caused by Guignardia bidwellii fungus. Can destroy entire grape crop.",
        "symptoms"       : [
            "Tan circular spots with dark borders on leaves",
            "Black shriveled mummified berries",
            "Brown lesions on shoots and tendrils",
            "Infected berries fall or remain on vine"
        ],
        "organic_remedy" : [
            "Remove all mummified berries from vine",
            "Apply copper sulfate spray early season",
            "Prune for open canopy and air flow",
            "Remove infected shoot tips",
            "Use sulfur dust during dry weather"
        ],
        "chemical_remedy": [
            "Apply Myclobutanil 10% WP",
            "Use Mancozeb 75% WP spray",
            "Spray Captan 50% WP",
            "Apply Tebuconazole 25.9% EC"
        ],
        "prevention"     : [
            "Remove mummies and infected debris in winter",
            "Train vines for good air circulation",
            "Apply first spray at bud break",
            "Continue spray program through fruit set",
            "Plant in well-drained sunny locations"
        ],
        "source"         : "Virginia Cooperative Extension"
    },
    "Healthy": {
        "disease_name"   : "No Disease Detected",
        "plant"          : "General",
        "severity"       : "None",
        "description"    : "Your plant appears healthy! No disease symptoms detected.",
        "symptoms"       : [],
        "organic_remedy" : [
            "Continue regular watering schedule",
            "Apply balanced organic fertilizer monthly",
            "Monitor regularly for early signs of disease"
        ],
        "chemical_remedy": [],
        "prevention"     : [
            "Maintain proper spacing between plants",
            "Water at soil level to keep leaves dry",
            "Rotate crops each season",
            "Use disease resistant varieties",
            "Inspect plants weekly for early detection"
        ],
        "source"         : "General Agricultural Guidelines"
    }
}

def get_treatment(disease_label: str) -> dict:
    """
    Get treatment for a detected disease.
    Returns treatment dict or unknown disease response.
    """
    # Direct match
    if disease_label in TREATMENT_DB:
        return {
            "status" : "found",
            "data"   : TREATMENT_DB[disease_label]
        }

    # Partial match (in case label has slight variation)
    for key in TREATMENT_DB:
        if key.lower() in disease_label.lower() or disease_label.lower() in key.lower():
            return {
                "status" : "found",
                "data"   : TREATMENT_DB[key]
            }

    # Not found
    return {
        "status"  : "not_found",
        "message" : "Disease not recognized. Please consult a local agricultural expert.",
        "data"    : None
    }

def get_all_diseases() -> list:
    """Return list of all diseases in the database."""
    return [
        {
            "id"          : idx,
            "label"       : key,
            "disease_name": val["disease_name"],
            "plant"       : val["plant"],
            "severity"    : val["severity"]
        }
        for idx, (key, val) in enumerate(TREATMENT_DB.items())
    ]

def save_treatment_db():
    """Save treatment DB as JSON for frontend use."""
    os.makedirs(SYMPTOM_DIR, exist_ok=True)
    save_path = os.path.join(SYMPTOM_DIR, "treatment_db.json")
    with open(save_path, "w") as f:
        json.dump(TREATMENT_DB, f, indent=2)
    print(f" Treatment DB saved to: {save_path}")

if __name__ == "__main__":
    print("=" * 50)
    print("  PlantDocBot — Treatment Mapper")
    print("=" * 50)

    # Test it
    test_disease = "Tomato___Late_blight"
    result = get_treatment(test_disease)
    print(f"\n Test lookup: {test_disease}")
    print(f"  Disease   : {result['data']['disease_name']}")
    print(f"  Severity  : {result['data']['severity']}")
    print(f"  Organic   : {result['data']['organic_remedy'][0]}")
    print(f"  Chemical  : {result['data']['chemical_remedy'][0]}")

    # Save DB
    save_treatment_db()

    print(f"\n Total diseases in DB: {len(TREATMENT_DB)}")
    print("Treatment Mapper Ready!")