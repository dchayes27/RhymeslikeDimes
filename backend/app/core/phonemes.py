import pronouncing
import json
import os
from functools import lru_cache
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PhonemesManager:
    def __init__(self, overrides_path: Optional[str] = None):
        self.overrides_path = overrides_path or os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "overrides.json"
        )
        self.overrides = self._load_overrides()
    
    def _load_overrides(self) -> Dict[str, List[str]]:
        """Load custom pronunciation overrides from JSON file."""
        if os.path.exists(self.overrides_path):
            try:
                with open(self.overrides_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load pronunciation overrides: {e}")
        return {}
    
    @lru_cache(maxsize=1000)
    def get_phones(self, word: str) -> List[str]:
        """
        Get phonetic pronunciations for a word.
        
        Args:
            word: Word to get pronunciations for
        
        Returns:
            List of pronunciation strings
        """
        # Normalize word (lowercase, strip punctuation)
        normalized = word.lower().strip()
        
        # Check overrides first
        if normalized in self.overrides:
            return self.overrides[normalized]
        
        # Fall back to CMU dictionary
        return pronouncing.phones_for_word(normalized)
    
    def get_rhyming_part(self, word: str) -> Optional[str]:
        """Get the rhyming part of a word's pronunciation."""
        phones = self.get_phones(word)
        if phones:
            return pronouncing.rhyming_part(phones[0])
        return None
    
    def syllable_count(self, word: str) -> int:
        """Get the syllable count for a word."""
        phones = self.get_phones(word)
        if phones:
            return pronouncing.syllable_count(phones[0])
        return 0