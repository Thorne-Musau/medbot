# 🏥 MedBot - Medical Diagnosis Assistant

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-unittest-blue.svg)](tests/)

A sophisticated medical diagnosis assistant powered by machine learning and natural language processing. MedBot helps identify potential diseases based on patient symptoms, providing explainable predictions using SHAP (SHapley Additive exPlanations) for transparency and trust.

## 🌟 Key Features

- **🤖 Natural Language Processing**
  - Understands symptom descriptions in natural language
  - Handles complex medical terminology
  - Supports multiple languages (English)

- **🔍 Comprehensive Symptom Extraction**
  - Identifies multiple symptoms from text descriptions
  - Handles medical and common terminology
  - Supports symptom severity and duration

- **🏥 Disease Prediction**
  - Accurate disease prediction based on symptoms
  - Confidence scoring for predictions
  - Support for multiple disease categories

- **📊 Explainable AI**
  - Detailed SHAP-based explanations
  - Visual interpretation of predictions
  - Feature importance analysis

- **📈 Visualization**
  - SHAP summary plots
  - Waterfall plots for individual predictions
  - Interactive feature importance charts

## 📁 Project Structure

```
medbot/
├── data/
│   ├── raw/              # Original dataset
│   └── processed/        # Processed data files
├── models/
│   └── saved_models/     # Trained model files
├── nlp/                  # Natural Language Processing modules
├── explainable_ai/       # Explainable AI components
├── tests/               # Test files
└── docs/                # Documentation and visualizations
```

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Thorne-Musau/medbot.git
cd medbot
```

2. **Create and activate a virtual environment:**
```bash
python -m venv medbot_env
# On Windows
medbot_env\Scripts\activate
# On Unix or MacOS
source medbot_env/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Basic Usage

```python
from nlp import IntentClassifier, ComprehensiveSymptomExtractor
from explainable_ai import XAIPipeline

# Initialize components
classifier = IntentClassifier()
extractor = ComprehensiveSymptomExtractor()
xai_pipeline = XAIPipeline()

# Process user input
user_input = "I have a severe headache and fever"
intent = classifier.classify_intent(user_input)

if intent == "symptom_report":
    # Extract symptoms
    symptoms = extractor.extract_symptoms(user_input)
    
    # Get prediction and explanation
    prediction, explanation, visualization = xai_pipeline.explain_prediction(symptoms)
    
    print(f"Predicted Condition: {prediction}")
    print("\nExplanation:")
    print(explanation)
```

### Running Tests

```bash
python -m unittest discover tests
```

## 🧠 Model Architecture

### Components Overview

- **Intent Classification**
  - Pre-trained model for symptom reporting intent
  - Natural language understanding
  - Context-aware classification

- **Symptom Extraction**
  - Pattern matching algorithms
  - Medical term mapping
  - Context analysis

- **Disease Prediction**
  - Random Forest classifier
  - Multi-class classification
  - Probability scoring

- **Explanation Generation**
  - SHAP value calculation
  - Feature importance analysis
  - Visual explanation generation

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write clear, descriptive commit messages
- Include tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dataset Source**: [Source Name]
- **SHAP Library**: For explainable AI capabilities
- **Medical Resources**: For terminology and symptom mappings
- **Contributors**: All who have helped improve this project

## 📞 Contact

- **GitHub Issues**: [Open an issue](https://github.com/Thorne-Musau/medbot/issues)
- **Email**: [Your Email]
- **Project Link**: [https://github.com/Thorne-Musau/medbot](https://github.com/Thorne-Musau/medbot)

---

<p align="center">Made with ❤️ by Thorne Musau</p>

# MedBot API

A FastAPI-based backend for the MedBot system, providing endpoints for user authentication, chat interactions, and disease diagnosis.

## Features

- User authentication and management
- Chat conversation handling
- Disease diagnosis using ML model
- Conversation history tracking
- Diagnosis history tracking

## Prerequisites

- Python 3.8+
- PostgreSQL (optional, SQLite by default)
- Trained ML model and associated files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/medbot.git
cd medbot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with:
```
DATABASE_URL=sqlite:///./medbot.db  # Or your PostgreSQL URL
SECRET_KEY=your-secret-key-here
```

5. Initialize the database:
```bash
alembic upgrade head
```

## Project Structure

```
medbot/
├── api/
│   ├── app.py              # FastAPI application
│   ├── database.py         # Database configuration
│   ├── models/             # Pydantic and SQLAlchemy models
│   ├── routes/             # API endpoints
│   ├── auth/              # Authentication utilities
│   └── ml/                # ML model integration
├── models/
│   └── saved_models/      # Trained ML models
├── data/
│   └── processed/         # Processed data files
├── alembic/               # Database migrations
├── tests/                 # Test files
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## Running the API

1. Start the server:
```bash
uvicorn api.app:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- POST `/auth/register` - Register a new user
- POST `/auth/token` - Login and get access token

### Chat
- POST `/conversations` - Create a new conversation
- GET `/conversations` - List user's conversations
- GET `/conversations/{id}` - Get conversation details
- POST `/chat` - Send a message and get response

### Diagnosis
- POST `/diagnose` - Get diagnosis for symptoms
- GET `/diagnoses` - List user's diagnosis history
- GET `/diagnoses/{id}` - Get diagnosis details

## Testing

Run the test suite:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 