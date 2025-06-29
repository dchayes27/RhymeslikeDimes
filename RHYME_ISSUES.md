# Rhyming Logic Issues to Fix

## Issue 1: Card Ordering Problem
**Problem**: Multi-word cards appear in wrong order
**Current**: "This", "is", "the", "time", "This is", "is the", etc. (random order)
**Expected**: "This", "This is", "is", "is the", "the", "the time", "time" (grouped by starting word)

**Fix Needed**: Sort fragments so n-word phrases appear next to their base words
- "This" should be followed by "This is"
- "is" should be followed by "is the" 
- etc.

## Issue 2: Perfect Rhyme Classification Too Loose
**Problem**: Words classified as "perfect rhymes" when they only match ending syllables
**Example**: "times of" and "love" showing as perfect rhymes
- "times of" = [TAHYMZ AHV] 
- "love" = [LAHV]
- Only shares final [AHV] sound, not all syllables

**Expected**: Perfect rhymes should match ALL syllables, not just endings
**Current Perfect**: Should be Near/Slant rhymes instead

## Robust Test Cases Needed:

### Perfect Rhyme Tests:
- "cat" → "bat", "hat", "mat" (TRUE perfect)
- "spaghetti" → "confetti", "Serengeti" (TRUE perfect - all 3 syllables)
- "love" → "dove", "above" (TRUE perfect)

### Should NOT be Perfect:
- "times of" + "love" (different syllable counts)
- "running" + "gun" (syllable count mismatch)
- "beautiful" + "full" (only partial match)

### Multi-word Perfect:
- "ate spaghetti" → "confetti" (last word perfect match)
- "break the chain" → "take the pain" (last word perfect match)

## Priority:
1. **HIGH**: Fix perfect rhyme classification (syllable count + coverage)
2. **HIGH**: Fix card ordering (group n-grams by base word)
3. **MED**: Add comprehensive test cases

## Test Framework:
Create automated tests that verify:
- Syllable count matching for perfect rhymes
- Phonetic coverage percentage
- Proper card sorting order
- Multi-word rhyme accuracy