from nlp.symptom_extraction import ComprehensiveSymptomExtractor

extractor = ComprehensiveSymptomExtractor()
test_cases = [
    "I have headache and nausea but no fever",
    "Severe migraines with vomiting",
    "Mild stomach pain after eating"
]

for text in test_cases:
    print(f"Input: {text}")
    print("Output:", extractor.extract(text))
    print("-" * 50)