from typing import List, Dict, Tuple
import logging
from .datamuse import DatamuseClient
from .phonemes import PhonemesManager

logger = logging.getLogger(__name__)

try:
    from Phyme import Phyme
    phyme_available = True
except ImportError:
    phyme_available = False
    logger.warning("Phyme library not available, using basic rhyming only")


class RhymeEngine:
    def __init__(self):
        self.datamuse = DatamuseClient()
        self.phonemes = PhonemesManager()
        if phyme_available:
            self.phyme = Phyme()
    
    def sliding_ngrams(self, words: List[str], n_max: int = 3) -> List[Tuple[int, int, str]]:
        """
        Generate all n-grams up to n_max from a list of words.
        
        Args:
            words: List of words to generate n-grams from
            n_max: Maximum n-gram size
        
        Returns:
            List of tuples (start_idx, end_idx, phrase)
        """
        ngrams = []
        for n in range(1, min(n_max + 1, len(words) + 1)):
            for i in range(len(words) - n + 1):
                phrase = " ".join(words[i:i + n])
                ngrams.append((i, i + n, phrase))
        return ngrams
    
    def analyze_bar(self, bar: str, max_results: int = 7, ngram_max: int = 3) -> Dict[str, Dict]:
        """
        Analyze a bar of text for all rhyme possibilities.
        
        Args:
            bar: Line of text to analyze
            max_results: Maximum results per rhyme type
            ngram_max: Maximum n-gram size
        
        Returns:
            Dictionary mapping phrases to their rhyme information
        """
        # Tokenize the bar
        words = bar.split()
        if not words:
            return {}
        
        results = {}
        
        # Generate all n-grams
        for start, end, phrase in self.sliding_ngrams(words, ngram_max):
            # Get rhymes from Datamuse
            rhymes = self.datamuse.get_all_rhyme_types(phrase, max_results)
            
            # Filter out the original phrase from results (case-insensitive)
            phrase_lower = phrase.lower()
            for rhyme_type in rhymes:
                rhymes[rhyme_type] = [
                    r for r in rhymes[rhyme_type] 
                    if r.lower() != phrase_lower
                ]
            
            results[phrase] = {
                "perfect": rhymes["perfect"],
                "near": rhymes["near"],
                "slant": rhymes["slant"],
                "span": (start, end)
            }
        
        return results
    
    def get_suggestions_for_word(self, word: str, rhyme_type: str = "all", max_results: int = 10) -> Dict[str, List[str]]:
        """
        Get rhyme suggestions for a single word.
        
        Args:
            word: Word to find rhymes for
            rhyme_type: Type of rhyme or 'all'
            max_results: Maximum results to return
        
        Returns:
            Dictionary of rhyme suggestions by type
        """
        if rhyme_type == "all":
            return self.datamuse.get_all_rhyme_types(word, max_results)
        else:
            rhymes = self.datamuse.get_rhymes(word, rhyme_type, max_results)
            return {rhyme_type: rhymes}