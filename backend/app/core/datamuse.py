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
        Check if two words are perfect rhymes optimized for rap/poetry.
        Includes DOOM-style slant rhymes and assonance patterns.
        """
        try:
            phones1 = pronouncing.phones_for_word(word1.lower())
            phones2 = pronouncing.phones_for_word(word2.lower())
            
            if not phones1 or not phones2:
                return False
            
            # Get the primary pronunciation for each word
            phone1 = phones1[0]
            phone2 = phones2[0]
            phonemes1 = phone1.split()
            phonemes2 = phone2.split()
            
            # Get rhyming parts (from stressed vowel to end)
            rhyme1 = pronouncing.rhyming_part(phone1)
            rhyme2 = pronouncing.rhyming_part(phone2)
            
            if not rhyme1 or not rhyme2:
                return False
            
            # Calculate syllable and phoneme counts
            syllables1 = pronouncing.syllable_count(phone1)
            syllables2 = pronouncing.syllable_count(phone2)
            rhyme_syllables = pronouncing.syllable_count(rhyme1)
            
            # Count phonemes in rhyming parts for ending strength analysis
            rhyme1_phonemes = rhyme1.split()
            rhyme2_phonemes = rhyme2.split()
            
            # Find common suffix (ending phonemes that match)
            common_suffix_length = 0
            min_phoneme_len = min(len(rhyme1_phonemes), len(rhyme2_phonemes))
            
            for i in range(1, min_phoneme_len + 1):
                if rhyme1_phonemes[-i] == rhyme2_phonemes[-i]:
                    common_suffix_length = i
                else:
                    break
            
            # DOOM-STYLE SLANT RHYME PATTERNS
            # Check for assonance (vowel similarity) and consonance (consonant similarity)
            vowels1 = [p for p in phonemes1 if any(char.isdigit() for char in p)]
            vowels2 = [p for p in phonemes2 if any(char.isdigit() for char in p)]
            consonants1 = [p for p in phonemes1 if not any(char.isdigit() for char in p)]
            consonants2 = [p for p in phonemes2 if not any(char.isdigit() for char in p)]
            
            # Check for ending consonant similarity (very important in rap)
            ending_consonant_match = False
            if consonants1 and consonants2:
                ending_consonant_match = consonants1[-1] == consonants2[-1]
            
            # Check for vowel assonance (main vowel sounds)
            vowel_assonance = False
            if vowels1 and vowels2:
                # Compare main vowel sound (remove stress markers)
                main_vowel1 = vowels1[-1][:-1] if vowels1[-1][-1].isdigit() else vowels1[-1]
                main_vowel2 = vowels2[-1][:-1] if vowels2[-1][-1].isdigit() else vowels2[-1]
                vowel_assonance = main_vowel1 == main_vowel2
            
            # MULTI-SYLLABLE RAP RHYME LOGIC (most important use case)
            if syllables1 >= 2 and syllables2 >= 2:
                # Case 1: Perfect rhyming parts match (revolutionary/evolutionary)
                if rhyme1 == rhyme2:
                    if rhyme_syllables >= 2:
                        return True  # Perfect multi-syllable ending
                    elif rhyme_syllables == 1 and common_suffix_length >= 2:
                        return True  # Strong single-syllable ending with multiple phonemes
                
                # Case 2: Strong ending match with good phoneme overlap
                if common_suffix_length >= 3:  # 3+ phonemes = strong rap rhyme
                    return True
                
                # Case 3: Good ending match for longer words
                if common_suffix_length >= 2 and min(syllables1, syllables2) >= 3:
                    return True  # Multi-syllable words with decent ending
                
                # Case 4: DOOM-style slant rhyme for multi-syllable
                if ending_consonant_match and abs(syllables1 - syllables2) <= 1:
                    return True  # "again/hydrogen" type patterns
                
                # Case 5: Traditional coverage check (more lenient for multi-syllable)
                coverage1 = rhyme_syllables / syllables1 if syllables1 > 0 else 0
                coverage2 = rhyme_syllables / syllables2 if syllables2 > 0 else 0
                min_coverage = min(coverage1, coverage2)
                
                # Lower threshold for multi-syllable (50% instead of 65%)
                return min_coverage >= 0.5
            
            # SINGLE SYLLABLE LOGIC (enhanced for DOOM patterns)
            elif syllables1 == 1 and syllables2 == 1:
                # Perfect match
                if rhyme1 == rhyme2 and len(rhyme1_phonemes) >= 2:
                    return True
                
                # DOOM-style single syllable slant rhymes
                if ending_consonant_match:  # "man/in", "tear/year"
                    return True
                
                if vowel_assonance:  # "til/in" - same vowel sound is enough for DOOM
                    return True
                
                # Strong phoneme overlap
                if common_suffix_length >= 2:
                    return True
            
            # MIXED SYLLABLE LOGIC (single + multi)
            else:
                max_syllables = max(syllables1, syllables2)
                
                # For mixed single/multi-syllable (like "love"/"above")
                if max_syllables <= 4:  # Increased for "again/hydrogen"
                    if rhyme1 == rhyme2:
                        return True
                    elif common_suffix_length >= 2:
                        return True
                    elif ending_consonant_match:  # DOOM-style mixed like "again/hydrogen"
                        return True
                
                # For larger differences, require good coverage
                coverage1 = rhyme_syllables / syllables1 if syllables1 > 0 else 0
                coverage2 = rhyme_syllables / syllables2 if syllables2 > 0 else 0
                min_coverage = min(coverage1, coverage2)
                
                return min_coverage >= 0.6
            
            # Fallback - should not reach here
            return False
            
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