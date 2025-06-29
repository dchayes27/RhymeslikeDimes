from typing import List, Dict, Tuple, Optional
import logging
import pronouncing
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
        
        # Enhanced features flag - enabled since multi-syllable detection is core functionality
        self.enhanced_features_enabled = True
    
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
        
        enhanced_results = results.copy()
        
        # Only run enhanced features if enabled and no previous errors
        if self.enhanced_features_enabled:
            try:
                # Add multi-word phrase rhymes for better DOOM-style matching
                enhanced_results = self._add_multi_word_phrase_rhymes(results, words, max_results)
            except Exception as e:
                logger.warning(f"Multi-word phrase rhymes failed, disabling enhanced features: {e}")
                self.enhanced_features_enabled = False
                enhanced_results = results.copy()
            
            if self.enhanced_features_enabled:
                try:
                    # Add internal rhyme detection
                    internal_rhymes = self._find_internal_rhymes(bar, max_results)
                    if internal_rhymes:
                        enhanced_results["_internal_rhymes"] = internal_rhymes
                except Exception as e:
                    logger.warning(f"Internal rhyme detection failed: {e}")
        
        # Sort results for better card ordering - group n-grams by base word
        sorted_results = self._sort_results_by_base_word(enhanced_results)
        return sorted_results
    
    def _sort_results_by_base_word(self, results: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Sort results to group multi-word fragments with their base words.
        E.g., "This" should appear before "This is", then "is" before "is the", etc.
        """
        # Convert to list of (phrase, data) tuples for sorting
        result_items = list(results.items())
        
        def sort_key(item):
            phrase, data = item
            words = phrase.split()
            first_word = words[0].lower() if words else ""
            word_count = len(words)
            # Sort by: first word, then by number of words (1-grams before 2-grams, etc.)
            return (first_word, word_count)
        
        # Sort and convert back to dict
        sorted_items = sorted(result_items, key=sort_key)
        return dict(sorted_items)
    
    def _add_multi_word_phrase_rhymes(self, results: Dict[str, Dict], words: List[str], max_results: int) -> Dict[str, Dict]:
        """
        Add DOOM-style multi-word phrase rhyming to existing results.
        Finds rhymes between phrase endings like 'krills in his hand and' → 'gazillion grand'
        """
        try:
            enhanced_results = results.copy()
            
            # Extract multi-word phrases (2+ words) from results
            multi_word_phrases = [phrase for phrase in results.keys() if len(phrase.split()) >= 2]
            
            # Limit processing to prevent timeouts
            if len(multi_word_phrases) > 20:
                multi_word_phrases = multi_word_phrases[:20]
            
            for phrase in multi_word_phrases:
                try:
                    phrase_words = phrase.split()
                    
                    # For each multi-word phrase, find other multi-word phrases that rhyme
                    phrase_ending_rhymes = self._find_phrase_ending_rhymes(phrase, multi_word_phrases, max_results)
                    
                    # Add these to the results
                    if phrase_ending_rhymes:
                        for rhyme_type, rhyme_list in phrase_ending_rhymes.items():
                            if rhyme_list:  # Only add if there are actual rhymes
                                enhanced_results[phrase][f"phrase_{rhyme_type}"] = rhyme_list
                except Exception as e:
                    logger.debug(f"Error processing phrase '{phrase}': {e}")
                    continue
            
            return enhanced_results
        except Exception as e:
            logger.warning(f"Multi-word phrase enhancement failed: {e}")
            return results.copy()
    
    def _find_phrase_ending_rhymes(self, target_phrase: str, candidate_phrases: List[str], max_results: int) -> Dict[str, List[str]]:
        """
        Find multi-word phrases that rhyme with the target phrase ending.
        Uses DOOM-style logic: compare last 1-3 words of phrases phonetically.
        """
        target_words = target_phrase.split()
        phrase_rhymes = {"perfect": [], "near": [], "slant": []}
        
        for candidate in candidate_phrases:
            if candidate.lower() == target_phrase.lower():
                continue
                
            candidate_words = candidate.split()
            
            # Compare phrase endings of different lengths (1-3 words)
            for ending_length in range(1, min(4, len(target_words) + 1, len(candidate_words) + 1)):
                target_ending = " ".join(target_words[-ending_length:])
                candidate_ending = " ".join(candidate_words[-ending_length:])
                
                if target_ending.lower() == candidate_ending.lower():
                    continue
                
                # Score the phrase ending similarity
                similarity_score = self._score_phrase_similarity(target_ending, candidate_ending)
                
                if similarity_score >= 0.8:  # High similarity = perfect
                    if candidate not in phrase_rhymes["perfect"]:
                        phrase_rhymes["perfect"].append(candidate)
                elif similarity_score >= 0.6:  # Medium similarity = near
                    if candidate not in phrase_rhymes["near"]:
                        phrase_rhymes["near"].append(candidate)
                elif similarity_score >= 0.4:  # Low similarity = slant
                    if candidate not in phrase_rhymes["slant"]:
                        phrase_rhymes["slant"].append(candidate)
        
        # Limit results
        for rhyme_type in phrase_rhymes:
            phrase_rhymes[rhyme_type] = phrase_rhymes[rhyme_type][:max_results]
        
        return phrase_rhymes
    
    def _score_phrase_similarity(self, phrase1: str, phrase2: str) -> float:
        """
        Score similarity between two phrases based on phonetic patterns.
        Returns 0.0-1.0 where 1.0 is perfect similarity.
        """
        words1 = phrase1.split()
        words2 = phrase2.split()
        
        if len(words1) != len(words2):
            # Different word counts - can still rhyme but lower base score
            base_score = 0.3
        else:
            base_score = 0.5
        
        # Compare each word pair
        word_scores = []
        min_len = min(len(words1), len(words2))
        
        for i in range(min_len):
            word1 = words1[-(i+1)]  # Compare from the end
            word2 = words2[-(i+1)]
            
            # Use existing perfect rhyme logic for individual words
            if self.datamuse._is_perfect_rhyme(word1, word2):
                word_scores.append(1.0)
            else:
                # Calculate phonetic similarity manually
                similarity = self._calculate_phonetic_similarity(word1, word2)
                word_scores.append(similarity)
        
        if not word_scores:
            return 0.0
        
        # Weight the last word (most important) more heavily
        if len(word_scores) == 1:
            final_score = word_scores[0]
        else:
            # Last word counts for 60%, other words for 40%
            last_word_score = word_scores[0] * 0.6
            other_words_score = sum(word_scores[1:]) / len(word_scores[1:]) * 0.4
            final_score = last_word_score + other_words_score
        
        return min(1.0, base_score + final_score * 0.5)
    
    def _calculate_phonetic_similarity(self, word1: str, word2: str) -> float:
        """Calculate basic phonetic similarity between two words."""
        try:
            phones1 = pronouncing.phones_for_word(word1.lower())
            phones2 = pronouncing.phones_for_word(word2.lower())
            
            if not phones1 or not phones2:
                return 0.0
            
            # Get rhyming parts
            rhyme1 = pronouncing.rhyming_part(phones1[0])
            rhyme2 = pronouncing.rhyming_part(phones2[0])
            
            if not rhyme1 or not rhyme2:
                return 0.0
            
            # Compare rhyming parts
            if rhyme1 == rhyme2:
                return 1.0
            
            # Calculate phoneme overlap
            phonemes1 = rhyme1.split()
            phonemes2 = rhyme2.split()
            
            # Find common ending phonemes
            common_ending = 0
            min_len = min(len(phonemes1), len(phonemes2))
            
            for i in range(1, min_len + 1):
                if phonemes1[-i] == phonemes2[-i]:
                    common_ending = i
                else:
                    break
            
            if min_len == 0:
                return 0.0
            
            return common_ending / min_len
            
        except Exception:
            return 0.0
    
    def _find_internal_rhymes(self, text: str, max_results: int = 10) -> Dict[str, List[Dict]]:
        """
        Find internal rhymes within a single line of text.
        Example: "hawk men stalkin' hear that we hawkin' often" -> finds multiple internal rhyme pairs
        """
        words = text.split()
        internal_rhymes = {"perfect": [], "near": [], "slant": []}
        
        # Limit to first 15 words to prevent timeout on long texts
        limited_words = words[:15]
        
        # Compare every word with every other word in the line
        for i, word1 in enumerate(limited_words):
            for j, word2 in enumerate(limited_words):
                if i >= j:  # Skip self and already compared pairs
                    continue
                
                # Clean words (remove punctuation)
                clean_word1 = word1.strip(".,!?'\"").lower()
                clean_word2 = word2.strip(".,!?'\"").lower()
                
                if len(clean_word1) < 2 or len(clean_word2) < 2:
                    continue
                
                # Check if they rhyme using our enhanced algorithm
                rhyme_strength = self._classify_internal_rhyme_strength(clean_word1, clean_word2)
                
                if rhyme_strength > 0.3:  # Higher threshold to reduce noise
                    rhyme_info = {
                        "word1": word1,
                        "word2": word2,
                        "position1": i,
                        "position2": j,
                        "strength": rhyme_strength,
                        "pattern": f"{clean_word1} → {clean_word2}"
                    }
                    
                    if rhyme_strength >= 0.8:
                        internal_rhymes["perfect"].append(rhyme_info)
                    elif rhyme_strength >= 0.6:
                        internal_rhymes["near"].append(rhyme_info)
                    else:
                        internal_rhymes["slant"].append(rhyme_info)
        
        # Limit results and sort by strength
        for rhyme_type in internal_rhymes:
            internal_rhymes[rhyme_type] = sorted(
                internal_rhymes[rhyme_type], 
                key=lambda x: x["strength"], 
                reverse=True
            )[:max_results]
        
        return internal_rhymes
    
    def _classify_internal_rhyme_strength(self, word1: str, word2: str) -> float:
        """
        Classify the strength of internal rhyme between two words.
        Returns 0.0-1.0 where 1.0 is perfect rhyme.
        """
        # Use existing perfect rhyme check first
        if self.datamuse._is_perfect_rhyme(word1, word2):
            return 1.0
        
        # Calculate phonetic similarity for partial matches
        phonetic_sim = self._calculate_phonetic_similarity(word1, word2)
        
        # Check for consonant cluster similarity (important for DOOM style)
        consonant_sim = self._calculate_consonant_similarity(word1, word2)
        
        # Check for vowel pattern similarity (assonance)
        vowel_sim = self._calculate_vowel_similarity(word1, word2)
        
        # Combine scores with weights
        # Phonetic similarity is most important, consonant patterns second, vowels third
        combined_score = (phonetic_sim * 0.5) + (consonant_sim * 0.3) + (vowel_sim * 0.2)
        
        return min(1.0, combined_score)
    
    def _calculate_consonant_similarity(self, word1: str, word2: str) -> float:
        """Calculate similarity based on consonant patterns (for DOOM-style cluster matching)."""
        try:
            phones1 = pronouncing.phones_for_word(word1)
            phones2 = pronouncing.phones_for_word(word2)
            
            if not phones1 or not phones2:
                return 0.0
            
            # Extract consonants (phonemes without stress numbers)
            consonants1 = [p for p in phones1[0].split() if not any(char.isdigit() for char in p)]
            consonants2 = [p for p in phones2[0].split() if not any(char.isdigit() for char in p)]
            
            if not consonants1 or not consonants2:
                return 0.0
            
            # Check for ending consonant similarity
            ending_match = consonants1[-1] == consonants2[-1] if consonants1 and consonants2 else False
            
            # Check for consonant cluster overlap
            common_consonants = set(consonants1) & set(consonants2)
            total_consonants = set(consonants1) | set(consonants2)
            
            if not total_consonants:
                return 0.0
            
            overlap_ratio = len(common_consonants) / len(total_consonants)
            
            # Weight ending consonant match more heavily
            if ending_match:
                return min(1.0, overlap_ratio + 0.3)
            else:
                return overlap_ratio
            
        except Exception:
            return 0.0
    
    def _calculate_vowel_similarity(self, word1: str, word2: str) -> float:
        """Calculate similarity based on vowel patterns (assonance)."""
        try:
            phones1 = pronouncing.phones_for_word(word1)
            phones2 = pronouncing.phones_for_word(word2)
            
            if not phones1 or not phones2:
                return 0.0
            
            # Extract vowels (phonemes with stress numbers)
            vowels1 = [p for p in phones1[0].split() if any(char.isdigit() for char in p)]
            vowels2 = [p for p in phones2[0].split() if any(char.isdigit() for char in p)]
            
            if not vowels1 or not vowels2:
                return 0.0
            
            # Compare main vowel sounds (remove stress markers)
            main_vowel1 = vowels1[-1][:-1] if vowels1[-1][-1].isdigit() else vowels1[-1]
            main_vowel2 = vowels2[-1][:-1] if vowels2[-1][-1].isdigit() else vowels2[-1]
            
            if main_vowel1 == main_vowel2:
                return 1.0
            
            # Check for vowel pattern similarity
            vowel_set1 = set(v[:-1] if v[-1].isdigit() else v for v in vowels1)
            vowel_set2 = set(v[:-1] if v[-1].isdigit() else v for v in vowels2)
            
            common_vowels = vowel_set1 & vowel_set2
            total_vowels = vowel_set1 | vowel_set2
            
            if not total_vowels:
                return 0.0
            
            return len(common_vowels) / len(total_vowels)
            
        except Exception:
            return 0.0
    
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