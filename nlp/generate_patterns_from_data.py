import pandas as pd
import joblib
from pathlib import Path
from collections import defaultdict
import spacy
from spacy.tokens import DocBin

# Initialize NLP processor
nlp = spacy.load("en_core_web_sm")

def generate_comprehensive_patterns():
    """Create symptom patterns from raw dataset"""
    # Load your binary encoded dataset
    df = pd.read_csv(Path('data/raw/symptoms.csv'))
    
    # Get all symptom column names (excluding prognosis)
    symptom_columns = [col for col in df.columns if col != "prognosis"]
    
    # Create symptom clusters by co-occurrence
    symptom_clusters = defaultdict(list)
    for _, row in df.iterrows():
        active_symptoms = [col for col in symptom_columns if row[col] == 1]
        for symptom in active_symptoms:
            symptom_clusters[symptom].extend(active_symptoms)
    
    # Generate patterns for each symptom
    patterns = {}
    for symptom in symptom_columns:
        # Standard pattern
        readable = symptom.replace('_', ' ')
        patterns[symptom] = [readable]
        
        # Add common co-occurring symptoms as context patterns
        frequent_co_occurrences = [
            s for s in symptom_clusters[symptom] 
            if symptom_clusters[symptom].count(s) > 5
        ][:3]  # Top 3 most frequent
        
        # Create phrase patterns
        for co_symptom in frequent_co_occurrences:
            phrase = f"{readable} and {co_symptom.replace('_', ' ')}"
            patterns[symptom].append(phrase)
    
    # Add common linguistic variations
    variations = {
        'headache': ['migraine', 'head pain', 'cephalgia', 'cephalalgia'],
        'nausea': ['queasiness', 'sick feeling'],
        'vomiting': ['emesis', 'throwing up', 'puking'],
        'fatigue': ['tiredness', 'exhaustion'],
        'fever': ['pyrexia', 'hyperthermia'],
        'cough': ['tussis', 'hacking'],
        'chest_pain': ['thoracic pain', 'chest discomfort'],
        'dizziness': ['vertigo', 'lightheadedness']
    }
    for symptom, vars in variations.items():
        if symptom in patterns:
            patterns[symptom].extend(vars)
    
    # ===== ADD YOUR MANUAL PATTERNS HERE =====
    patterns["headache"].extend(["migraine", "migraines", "head pain"])
    patterns["vomiting"].extend(["throwing up", "puking"])
    # ===== END OF ADDITIONS =====
    
    # Save comprehensive patterns
    joblib.dump(patterns, Path('data/processed/symptom_patterns.joblib'))
    print(f"Generated {len(patterns)} symptom patterns with contextual variations")

if __name__ == "__main__":
    generate_comprehensive_patterns()