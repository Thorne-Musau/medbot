import spacy
from spacy.matcher import PhraseMatcher
import joblib
from pathlib import Path
from typing import List, Dict

class ComprehensiveSymptomExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.symptom_map = joblib.load(Path('data/processed/symptom_names.joblib'))
        self.patterns = joblib.load(Path('data/processed/symptom_patterns.joblib'))
        self.matcher = self._build_matcher()
        
    def _build_matcher(self):
        """Build matcher with multiple pattern types"""
        matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        
        # Add main symptom patterns
        for symptom, variants in self.patterns.items():
            patterns = [self.nlp(text) for text in variants]
            matcher.add(symptom, patterns)
            
        # Add negation patterns
        negation_phrases = ["no", "not", "without", "don't have"]
        for phrase in negation_phrases:
            matcher.add("NEGATION", [self.nlp(phrase)])
            
        return matcher
    
    def extract(self, text: str) -> Dict[str, List]:
        """Extract symptoms with context awareness"""
        doc = self.nlp(text.lower())
        matches = self.matcher(doc)
        
        results = {
            "exact_matches": set(),
            "related_symptoms": set(),
            "negated_symptoms": set()
        }
        
        # Process matches
        for match_id, start, end in matches:
            match_text = self.nlp.vocab.strings[match_id]
            
            if match_text == "NEGATION":
                # Handle negations in context
                self._process_negation(doc, start, end, results)
            elif match_text in self.symptom_map:
                # Check for contextual clues
                if not self._is_negated(doc, start, end):
                    results["exact_matches"].add(match_text)
        
        return {
            "exact_matches": list(results["exact_matches"]),
            "related_symptoms": list(results["related_symptoms"]),
            "negated_symptoms": list(results["negated_symptoms"])
        }
    
    def _is_negated(self, doc, start, end):
        """Check if match is in negation context"""
        window_start = max(0, start - 3)
        window_end = min(len(doc), end + 1)
        for token in doc[window_start:window_end]:
            if token.text in {"no", "not", "without"}:
                return True
        return False
    
    def _process_negation(self, doc, neg_start, neg_end, results):
        """Find and mark negated symptoms"""
        search_window = doc[max(0, neg_start-5):min(len(doc), neg_end+5)]
        for token in search_window:
            if token.text in self.patterns:
                results["negated_symptoms"].add(token.text)

# Example usage
if __name__ == "__main__":
    extractor = ComprehensiveSymptomExtractor()
    sample_text = "I have a headache and nausea but no fever"
    print(extractor.extract(sample_text))
    # Output: {'exact_matches': ['headache', 'nausea'], 
    #          'related_symptoms': [], 
    #          'negated_symptoms': ['fever']}