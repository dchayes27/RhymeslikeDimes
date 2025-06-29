#!/usr/bin/env python3
"""
Test MF DOOM-style complex rhyme patterns from the user's example.
These should ALL pass as perfect rhymes with our rap-optimized algorithm.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.datamuse import DatamuseClient
import pronouncing

def test_doom_rhyme(phrase1, phrase2, context):
    """Test a specific DOOM-style rhyme pattern"""
    client = DatamuseClient()
    
    # Extract last words for multi-word phrases
    word1 = phrase1.split()[-1].lower().strip('.,!?')
    word2 = phrase2.split()[-1].lower().strip('.,!?')
    
    result = client._is_perfect_rhyme(word1, word2)
    
    # Get phonetic analysis
    phones1 = pronouncing.phones_for_word(word1)
    phones2 = pronouncing.phones_for_word(word2)
    
    status = "✅ PASS" if result else "❌ FAIL"
    
    print(f"\n{status} {context}")
    print(f"   '{phrase1}' → '{word1}'")
    print(f"   '{phrase2}' → '{word2}'")
    print(f"   Algorithm result: {result}")
    
    if phones1 and phones2:
        rhyme1 = pronouncing.rhyming_part(phones1[0])
        rhyme2 = pronouncing.rhyming_part(phones2[0])
        print(f"   Phonetics: {phones1[0]} | {phones2[0]}")
        print(f"   Rhyme parts: '{rhyme1}' | '{rhyme2}' (match: {rhyme1 == rhyme2})")
    
    return result if result is not None else False

print("🎤 MF DOOM RHYME PATTERN ANALYSIS")
print("Testing complex multi-syllable rhymes from the provided bars")
print("="*60)

# Test all the rhyme patterns from the DOOM bars
doom_rhymes = [
    # "beat kinda" / "meat grinder" 
    ("beat kinda", "meat grinder", "Internal rhyme: 'kinda' vs 'grinder'"),
    
    # "no brain" / "no chain"
    ("no brain", "no chain", "Perfect rhyme: 'brain' vs 'chain'"),
    
    # "nerd" / "heard"
    ("clever nerd", "ever heard", "Perfect rhyme: 'nerd' vs 'heard'"),
    
    # "cookie tear" / "rookie year"
    ("cookie tear", "rookie year", "Multi-syllable: 'cookie tear' vs 'rookie year'"),
    
    # "his hand" / "gazillion grand"
    ("his hand", "gazillion grand", "End rhyme: 'hand' vs 'grand'"),
    
    # "price again" / "hydrogen" 
    ("price again", "hydrogen", "Complex ending: 'again' vs 'hydrogen'"),
    
    # "blessed be the Lord" / "message board"
    ("blessed be the Lord", "message board", "End rhyme: 'Lord' vs 'board'"),
]

# Additional complex patterns to test
additional_patterns = [
    # Test the "kinda"/"grinder" pattern more directly
    ("kinda", "grinder", "Direct test: 'kinda' vs 'grinder'"),
    
    # Test syllable-heavy patterns
    ("again", "hydrogen", "Direct test: 'again' vs 'hydrogen'"),
    
    # Test DOOM-style internal complexity
    ("villain man", "krills in", "DOOM internal: 'man' vs 'in'"),
    ("rockin til", "clocked in", "DOOM flow: 'til' vs 'in'"),
]

all_tests = doom_rhymes + additional_patterns

results = []
for phrase1, phrase2, context in all_tests:
    result = test_doom_rhyme(phrase1, phrase2, context)
    results.append(result)

# Summary
passed = sum(results)
total = len(results)
pass_rate = (passed / total * 100) if total > 0 else 0

print(f"\n{'='*60}")
print(f"MF DOOM RHYME TEST RESULTS: {passed}/{total} passed ({pass_rate:.1f}%)")
print(f"{'='*60}")

if passed == total:
    print("🔥 ALL DOOM RHYMES PASS! Algorithm ready for complex rap patterns!")
else:
    failed_count = total - passed
    print(f"⚠️  {failed_count} rhyme(s) failed - need algorithm adjustments")
    
    # Show which ones failed
    print(f"\nFailed rhymes:")
    for i, (phrase1, phrase2, context) in enumerate(all_tests):
        if not results[i]:
            word1 = phrase1.split()[-1].lower().strip('.,!?')
            word2 = phrase2.split()[-1].lower().strip('.,!?')
            print(f"   '{word1}' vs '{word2}' ({context})")

print(f"\n🎯 For MF DOOM-style rap, we need these complex patterns to work!")
print(f"The algorithm should recognize sophisticated multi-syllable endings,")
print(f"internal rhymes, and slant rhymes that sound perfect in flow context.")