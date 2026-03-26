
# PlantDocBot

## Overview

PlantDocBot is an AI-powered tool designed to help farmers and gardeners diagnose plant diseases through image uploads or symptom descriptions. The system integrates computer vision and natural language processing to provide accurate disease identification and treatment recommendations in real time.

## Features

* Image-based plant disease detection using a CNN model (EfficientNet/MobileNet).
* Symptom-based text diagnosis via a fine-tuned BERT model.
* Recommendation engine mapping diseases to treatment and prevention strategies.
* Interactive web interface with chat and image upload support.
* Deployment-ready via Docker and compatible with web or mobile frontends.

## Datasets

* **PlantVillage Dataset**: Over 50,000 annotated plant leaf images for disease classification.
* **PlantDoc Dataset**: Real-world noisy images sourced from Kaggle.
* **Text Corpus**: Symptom descriptions collected from agricultural forums, blogs, and open-access research.



## Training

* **Vision model**: `src/vision/train_vision.py` (CNN with transfer learning).
* **NLP model**: `src/nlp/train_nlp.py` (BERT-based classifier for symptoms).


## Contributing

Contributions are welcome. Please submit issues or pull requests with descriptive details.

## License

This project is open-source and available under the MIT License.



If you want, I can also generate a **slimmed version optimized for GitHub** with badges for Python version, license, and Streamlit/CI links, so it looks professional and immediately readable to others. Do you want me to do that?
