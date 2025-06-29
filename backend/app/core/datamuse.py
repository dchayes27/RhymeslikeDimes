from datamuse import Datamuse
from typing import List, Dict, Optional
import logging
import pronouncing

logger = logging.getLogger(__name__)


class DatamuseClient:
    def __init__(self):
        self.api = Datamuse()
    
    def _is_perfect_rhyme(self, word1: str, word2: str) -> bool:
        """
        Check if two words are perfect rhymes (all syllables match phonetically).
        """
        try:
            phones1 = pronouncing.phones_for_word(word1.lower())
            phones2 = pronouncing.phones_for_word(word2.lower())
            
            if not phones1 or not phones2:
                return False
            
            # Get the primary pronunciation for each word
            phone1 = phones1[0]
            phone2 = phones2[0]
            
            # For perfect rhyme, the rhyming parts should be nearly identical
            # and cover most/all of the shorter word
            rhyme1 = pronouncing.rhyming_part(phone1)
            rhyme2 = pronouncing.rhyming_part(phone2)
            
            if not rhyme1 or not rhyme2 or rhyme1 != rhyme2:
                return False
            
            # Calculate what percentage of each word the rhyming part covers
            syllables1 = pronouncing.syllable_count(phone1)
            syllables2 = pronouncing.syllable_count(phone2)
            rhyme_syllables = pronouncing.syllable_count(rhyme1)
            
            # For perfect rhyme, the rhyming part should cover most of both words
            # (at least 70% for shorter words, and they should be close in syllable count)
            min_syllables = min(syllables1, syllables2)
            max_syllables = max(syllables1, syllables2)
            
            # Perfect rhymes should:
            # 1. Have the same rhyming part
            # 2. Cover most of the shorter word (80%+ for 1-2 syllables, 60%+ for longer)
            # 3. Not differ by more than 1 syllable
            if max_syllables - min_syllables > 1:
                return False
            
            coverage_threshold = 0.8 if min_syllables <= 2 else 0.6
            coverage = rhyme_syllables / min_syllables
            
            return coverage >= coverage_threshold
            
        except Exception as e:
            logger.debug(f"Error checking perfect rhyme for '{word1}' and '{word2}': {e}")
            return False
    
    def _classify_rhymes(self, original: str, candidates: List[str]) -> Dict[str, List[str]]:
        """
        Classify rhymes into perfect, near, and slant based on phonetic analysis.
        """
        perfect = []
        near = []
        slant = []
        
        for candidate in candidates:
            if candidate.lower() == original.lower():
                continue
                
            # For multi-word phrases, check the last word
            orig_words = original.strip().split()
            cand_words = candidate.strip().split()
            
            if len(orig_words) > 1 and len(cand_words) > 1:
                # Both are multi-word - check if last words are perfect rhymes
                if self._is_perfect_rhyme(orig_words[-1], cand_words[-1]):
                    perfect.append(candidate)
                else:
                    near.append(candidate)
            elif len(orig_words) > 1:
                # Original is multi-word, candidate is single - check against last word
                if self._is_perfect_rhyme(orig_words[-1], candidate):
                    perfect.append(candidate)
                else:
                    near.append(candidate)
            elif len(cand_words) > 1:
                # Candidate is multi-word, original is single - check against last word
                if self._is_perfect_rhyme(original, cand_words[-1]):
                    perfect.append(candidate)
                else:
                    near.append(candidate)
            else:
                # Both are single words
                if self._is_perfect_rhyme(original, candidate):
                    perfect.append(candidate)
                else:
                    near.append(candidate)
        
        return {
            "perfect": perfect,
            "near": near,
            "slant": slant
        }
    
    def get_rhymes(self, phrase: str, rhyme_type: str, max_results: int = 50) -> List[str]:
        """
        Get rhymes from Datamuse API.
        
        Args:
            phrase: Word or phrase to find rhymes for
            rhyme_type: Type of rhyme - 'perfect', 'near', or 'slant'
            max_results: Maximum number of results to return
        
        Returns:
            List of rhyming words/phrases
        """
        try:
            params = {"max": max_results}
            
            if rhyme_type == "perfect":
                params["rel_rhy"] = phrase
            elif rhyme_type == "near":
                params["rel_nry"] = phrase
            elif rhyme_type == "slant":
                params["sl"] = phrase
            else:
                logger.warning(f"Unknown rhyme type: {rhyme_type}")
                return []
            
            results = self.api.words(**params)
            return [item["word"] for item in results]
            
        except Exception as e:
            logger.error(f"Datamuse API error for '{phrase}': {str(e)}")
            return []
    
    def get_multi_word_rhymes(self, phrase: str, max_results: int = 10) -> List[str]:
        """
        Get multi-word rhymes by finding phrases ending with words that rhyme with the last word.
        """
        words = phrase.strip().split()
        if len(words) < 2:
            return []
        
        last_word = words[-1]
        rhyming_words = self.get_rhymes(last_word, "perfect", 15)  # Get more candidates
        
        multi_word_rhymes = []
        
        # Common word prefixes that often appear in multi-word phrases
        common_prefixes = [
            "made", "take", "came", "late", "hate", "gate", "date", "rate", "wait", "state",
            "stayed", "played", "delayed", "displayed", "betrayed", "conveyed", "surveyed",
            "blue", "new", "true", "threw", "grew", "knew", "flew", "drew", "few", "view",
            "break", "make", "take", "fake", "wake", "shake", "cake", "lake", "snake",
            "said", "red", "bed", "head", "dead", "led", "fed", "thread", "spread", "bread"
        ]
        
        for rhyme_word in rhyming_words:
            if rhyme_word.lower() == last_word.lower():
                continue
                
            # Try combining common prefixes with the rhyming word
            for prefix in common_prefixes:
                candidate = f"{prefix} {rhyme_word}"
                if candidate.lower() != phrase.lower():
                    multi_word_rhymes.append(candidate)
                    if len(multi_word_rhymes) >= max_results:
                        break
            
            if len(multi_word_rhymes) >= max_results:
                break
        
        # Also try to find real phrases from Datamuse that end with rhyming words
        for rhyme_word in rhyming_words[:5]:  # Limit to top 5 to avoid too many API calls
            try:
                # Search for phrases ending with the rhyming word
                params = {"max": 10, "sp": f"* {rhyme_word}"}
                phrases = self.api.words(**params)
                for item in phrases:
                    word = item["word"]
                    if " " in word and word.lower() != phrase.lower():
                        multi_word_rhymes.append(word)
                        if len(multi_word_rhymes) >= max_results:
                            break
                if len(multi_word_rhymes) >= max_results:
                    break
            except Exception as e:
                logger.warning(f"Error searching for phrases ending with '{rhyme_word}': {e}")
                continue
        
        return multi_word_rhymes[:max_results]
    
    def get_all_rhyme_types(self, phrase: str, max_per_type: int = 7) -> Dict[str, List[str]]:
        """
        Get all types of rhymes for a phrase, properly classified by phonetic accuracy.
        
        Args:
            phrase: Word or phrase to find rhymes for
            max_per_type: Maximum results per rhyme type
        
        Returns:
            Dictionary with 'perfect', 'near', and 'slant' rhyme lists
        """
        all_candidates = []
        
        # Get candidates from Datamuse API (all types)
        datamuse_perfect = self.get_rhymes(phrase, "perfect", max_per_type * 2)
        datamuse_near = self.get_rhymes(phrase, "near", max_per_type * 2)
        datamuse_slant = self.get_rhymes(phrase, "slant", max_per_type)
        
        all_candidates.extend(datamuse_perfect)
        all_candidates.extend(datamuse_near)
        
        # For multi-word phrases, also get rhymes for the last word
        if " " in phrase:
            words = phrase.strip().split()
            if words:
                last_word = words[-1]
                last_word_rhymes = self.get_rhymes(last_word, "perfect", max_per_type * 2)
                all_candidates.extend(last_word_rhymes)
                
                # Add some multi-word combinations
                multi_word_rhymes = self.get_multi_word_rhymes(phrase, max_per_type)
                all_candidates.extend(multi_word_rhymes)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_candidates = []
        for candidate in all_candidates:
            if candidate.lower() not in seen:
                seen.add(candidate.lower())
                unique_candidates.append(candidate)
        
        # Classify all candidates using phonetic analysis
        classified = self._classify_rhymes(phrase, unique_candidates)
        
        # Add slant rhymes from Datamuse (these are usually good)
        classified["slant"].extend([s for s in datamuse_slant if s.lower() != phrase.lower()])
        
        return {
            "perfect": classified["perfect"][:max_per_type],
            "near": classified["near"][:max_per_type], 
            "slant": classified["slant"][:max_per_type]
        }