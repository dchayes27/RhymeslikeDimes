#!/usr/bin/env python3
"""
Comprehensive test cases for rhyme classification system.
Tests both perfect rhyme detection and card ordering logic.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.datamuse import DatamuseClient
import pronouncing

class TestRhymeClassification:
    """Test cases for rhyme classification accuracy"""
    
    def setup_method(self):
        self.client = DatamuseClient()
    
    def test_perfect_rhymes_single_syllable(self):
        """Perfect rhymes - single syllable words"""
        perfect_pairs = [
            ("cat", "bat"),
            ("cat", "hat"), 
            ("cat", "mat"),
            ("love", "dove"),
            ("love", "above"),
            ("run", "gun"),
            ("run", "sun"),
            ("time", "rhyme"),
            ("time", "lime")
        ]
        
        for word1, word2 in perfect_pairs:
            is_perfect = self.client._is_perfect_rhyme(word1, word2)
            print(f"Testing '{word1}' vs '{word2}': {is_perfect}")
            assert is_perfect, f"'{word1}' and '{word2}' should be perfect rhymes"
    
    def test_perfect_rhymes_multi_syllable(self):
        """Perfect rhymes - multi-syllable words"""
        perfect_pairs = [
            ("spaghetti", "confetti"),
            ("nation", "station"),
            ("creation", "vacation")
        ]
        
        for word1, word2 in perfect_pairs:
            is_perfect = self.client._is_perfect_rhyme(word1, word2)
            print(f"Testing '{word1}' vs '{word2}': {is_perfect}")
            assert is_perfect, f"'{word1}' and '{word2}' should be perfect rhymes"
    
    def test_NOT_perfect_rhymes(self):
        """Words that should NOT be classified as perfect rhymes"""
        not_perfect_pairs = [
            ("times of", "love"),  # Different syllable counts
            ("running", "gun"),    # Syllable count mismatch  
            ("beautiful", "full"), # Only partial match
            ("chocolate", "late"), # Only ending match
            ("education", "nation"), # Only ending match
            ("telephone", "phone"),  # Only ending match
        ]
        
        for word1, word2 in not_perfect_pairs:
            is_perfect = self.client._is_perfect_rhyme(word1, word2)
            print(f"Testing '{word1}' vs '{word2}': {is_perfect}")
            assert not is_perfect, f"'{word1}' and '{word2}' should NOT be perfect rhymes"
    
    def test_multi_word_perfect_rhymes(self):
        """Multi-word phrases with perfect rhyme matches"""
        test_cases = [
            ("ate spaghetti", "confetti"),     # Last word perfect match
            ("break the chain", "pain"),       # Last word perfect match (simplified)
            ("running fast", "last"),          # Last word perfect match
            ("having fun", "sun")              # Last word perfect match
        ]
        
        for phrase, word in test_cases:
            # Extract last word from phrase
            last_word = phrase.split()[-1]
            is_perfect = self.client._is_perfect_rhyme(last_word, word)
            print(f"Testing '{phrase}' (last: '{last_word}') vs '{word}': {is_perfect}")
            assert is_perfect, f"'{phrase}' should perfect rhyme with '{word}' via last word '{last_word}'"
    
    def test_syllable_coverage_algorithm(self):
        """Test the syllable coverage calculation"""
        test_cases = [
            # (word1, word2, expected_coverage_ratio)
            ("cat", "bat", 1.0),           # Full coverage
            ("love", "dove", 1.0),         # Full coverage  
            ("times of", "love", 0.5),     # Only half coverage
            ("beautiful", "full", 0.33),   # Only 1/3 coverage
            ("chocolate", "late", 0.5),    # Only half coverage
        ]
        
        for word1, word2, expected_ratio in test_cases:
            # Get phonemes for both words
            phones1 = pronouncing.phones_for_word(word1.replace(' ', ''))
            phones2 = pronouncing.phones_for_word(word2.replace(' ', ''))
            
            if phones1 and phones2:
                # Count syllables (vowel sounds)
                syllables1 = len([p for p in phones1[0].split() if any(char.isdigit() for char in p)])
                syllables2 = len([p for p in phones2[0].split() if any(char.isdigit() for char in p)])
                
                min_syllables = min(syllables1, syllables2)
                max_syllables = max(syllables1, syllables2)
                
                # Calculate expected coverage
                actual_ratio = min_syllables / max_syllables if max_syllables > 0 else 0
                
                print(f"'{word1}' ({syllables1} syll) vs '{word2}' ({syllables2} syll): "
                      f"coverage = {actual_ratio:.2f}, expected ≈ {expected_ratio:.2f}")
                
                # Allow some tolerance in coverage calculation
                assert abs(actual_ratio - expected_ratio) < 0.2, \
                    f"Coverage ratio mismatch for '{word1}' vs '{word2}'"

class TestCardOrdering:
    """Test cases for proper card ordering/grouping"""
    
    def test_word_fragment_grouping(self):
        """Test that multi-word fragments group with their base words"""
        # Simulate rhyme results for phrase "This is the time"
        sample_rhymes = [
            {"word": "This", "rhyme_type": "slant"},
            {"word": "is", "rhyme_type": "near"}, 
            {"word": "the", "rhyme_type": "slant"},
            {"word": "time", "rhyme_type": "perfect"},
            {"word": "This is", "rhyme_type": "slant"},
            {"word": "is the", "rhyme_type": "near"},
            {"word": "the time", "rhyme_type": "perfect"},
        ]
        
        # Expected order: group n-grams with their base words (alphabetical by first word)
        expected_order = [
            "is",         # 1-gram (alphabetically first)
            "is the",     # 2-gram starting with "is"
            "the",        # 1-gram  
            "the time",   # 2-gram starting with "the"
            "This",       # 1-gram (capitalized "this")
            "This is",    # 2-gram starting with "This"
            "time"        # 1-gram
        ]
        
        # Sort using proposed algorithm
        def sort_key(rhyme):
            word = rhyme["word"]
            word_count = len(word.split())
            first_word = word.split()[0].lower()
            return (first_word, word_count)
        
        sorted_rhymes = sorted(sample_rhymes, key=sort_key)
        actual_order = [r["word"] for r in sorted_rhymes]
        
        print("Expected order:", expected_order)
        print("Actual order:  ", actual_order)
        
        assert actual_order == expected_order, \
            f"Card ordering mismatch. Expected: {expected_order}, Got: {actual_order}"
    
    def test_rhyme_type_priority(self):
        """Test that perfect rhymes appear before near/slant within groups"""
        sample_rhymes = [
            {"word": "time", "rhyme_type": "slant"},
            {"word": "time", "rhyme_type": "perfect"}, 
            {"word": "time", "rhyme_type": "near"},
        ]
        
        # Sort by rhyme type priority: perfect > near > slant
        rhyme_priority = {"perfect": 0, "near": 1, "slant": 2}
        
        def sort_key(rhyme):
            return rhyme_priority.get(rhyme["rhyme_type"], 3)
        
        sorted_rhymes = sorted(sample_rhymes, key=sort_key)
        actual_types = [r["rhyme_type"] for r in sorted_rhymes]
        expected_types = ["perfect", "near", "slant"]
        
        print("Expected types:", expected_types)
        print("Actual types:  ", actual_types)
        
        assert actual_types == expected_types, \
            f"Rhyme type ordering mismatch. Expected: {expected_types}, Got: {actual_types}"

def run_debug_tests():
    """Run specific tests to debug current issues"""
    print("=== DEBUGGING CURRENT RHYME ISSUES ===\n")
    
    client = DatamuseClient()
    
    # Test the specific problematic case: "times of" vs "love"
    print("1. Testing problematic case: 'times of' vs 'love'")
    is_perfect = client._is_perfect_rhyme("times of", "love")
    print(f"   Result: {is_perfect} (should be False)\n")
    
    # Test phonetic breakdown
    print("2. Phonetic analysis:")
    phones_times_of = pronouncing.phones_for_word("timesof")  # Combined for testing
    phones_love = pronouncing.phones_for_word("love")
    
    print(f"   'times of' phones: {phones_times_of}")
    print(f"   'love' phones: {phones_love}")
    
    if phones_times_of and phones_love:
        # Count syllables
        syll_times = len([p for p in phones_times_of[0].split() if any(char.isdigit() for char in p)])
        syll_love = len([p for p in phones_love[0].split() if any(char.isdigit() for char in p)])
        print(f"   Syllable counts: 'times of'={syll_times}, 'love'={syll_love}\n")
    
    # Test some known perfect rhymes
    print("3. Testing known perfect rhymes:")
    perfect_tests = [("cat", "bat"), ("love", "dove"), ("time", "rhyme")]
    for w1, w2 in perfect_tests:
        result = client._is_perfect_rhyme(w1, w2)
        print(f"   '{w1}' vs '{w2}': {result} (should be True)")

if __name__ == "__main__":
    # Run debug tests first
    run_debug_tests()
    
    print("\n" + "="*50)
    print("Running comprehensive test suite...")
    print("="*50)
    
    # Run manual tests since pytest isn't available
    test_suite = TestRhymeClassification()
    test_suite.setup_method()
    
    print("\n=== RUNNING MANUAL TEST SUITE ===")
    
    try:
        print("\n1. Testing single syllable perfect rhymes...")
        test_suite.test_perfect_rhymes_single_syllable()
        print("   ✓ PASSED")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
    
    try:
        print("\n2. Testing multi-syllable perfect rhymes...")
        test_suite.test_perfect_rhymes_multi_syllable()
        print("   ✓ PASSED")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
    
    try:
        print("\n3. Testing words that should NOT be perfect rhymes...")
        test_suite.test_NOT_perfect_rhymes()
        print("   ✓ PASSED")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
    
    try:
        print("\n4. Testing multi-word perfect rhymes...")
        test_suite.test_multi_word_perfect_rhymes()
        print("   ✓ PASSED")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
    
    try:
        print("\n5. Testing syllable coverage algorithm...")
        test_suite.test_syllable_coverage_algorithm()
        print("   ✓ PASSED")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
    
    # Test card ordering
    card_test = TestCardOrdering()
    
    try:
        print("\n6. Testing card ordering/grouping...")
        card_test.test_word_fragment_grouping()
        print("   ✓ PASSED")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
    
    try:
        print("\n7. Testing rhyme type priority...")
        card_test.test_rhyme_type_priority()
        print("   ✓ PASSED")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")