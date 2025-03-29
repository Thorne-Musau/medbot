import re
from typing import List

def tokenize_text(text: str) -> List[str]:
    """Tokenize text into words, handling medical terms"""
    # Convert to lowercase
    text = text.lower()
    
    # Split on whitespace and punctuation
    tokens = re.findall(r'\w+', text)
    
    # Handle medical terms with hyphens
    expanded_tokens = []
    for token in tokens:
        if '-' in token:
            expanded_tokens.extend(token.split('-'))
        expanded_tokens.append(token)
    
    return expanded_tokens 