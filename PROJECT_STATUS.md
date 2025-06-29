# RhymesLikeDimes Project Status

## Current State (2025-06-29)

### What's Working
- **Multi-syllable rhyme detection** - Core functionality fully operational
- **DOOM-style pattern matching** - Catches complex rhymes like "again/hydrogen", "kinda/grinder"
- **Multi-word phrase rhyming** - Finds phrases that rhyme with input phrases
- **Production deployment** - Live at https://rhymeslikedimes-production.up.railway.app
- **API compatibility** - Fixed Pydantic validation issues that were causing 500 errors

### Recent Changes
1. **Removed internal rhymes section** - It was confusing and not helpful for the main use case
2. **Enhanced rhyme algorithm** - Now catches assonance, consonance, and slant rhymes
3. **Fixed production deployment** - Was failing due to API response format issues

### Key Technical Details
- **Backend**: FastAPI + Datamuse API + CMU Pronouncing Dictionary
- **Frontend**: React/TypeScript with Vite and Tailwind CSS
- **Deployment**: Railway (backend) + Vercel (frontend)
- **Algorithm**: Enhanced `_is_perfect_rhyme()` in `/backend/app/core/datamuse.py` with DOOM-style pattern matching

### Current Issues & Considerations

#### 1. Categorization System
The current perfect/near/slant categories don't align well with creative needs:
- "empty with" returns "myth" as perfect but not "dreamt a fifth" 
- The algorithm's idea of "perfect" doesn't match what's useful for writing
- Multi-word phrases aren't being generated creatively enough

#### 2. Possible Reorganization Ideas
Instead of perfect/near/slant, consider organizing by:
- **Syllable matching** (1-syllable, 2-syllable, 3+ syllable rhymes)
- **Phrase complexity** (single words vs multi-word phrases)
- **Sound pattern** (ending sound, assonance, consonance)
- **Quality score** (single ranked list)
- **Commonality** (common vs creative/unusual)

#### 3. Multi-word Phrase Generation
Currently limited to:
- Common prefix combinations ("made with", "take with", etc.)
- Datamuse API searches for "* [rhyme_word]"
- Doesn't generate creative combinations like "dreamt a fifth"

### Test Commands
```bash
# Test multi-syllable detection
curl -X POST "https://rhymeslikedimes-production.up.railway.app/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"bar": "delivery discovery", "max_results": 3, "ngram_max": 2}'

# Test DOOM-style patterns
curl -X POST "https://rhymeslikedimes-production.up.railway.app/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"bar": "again hydrogen", "max_results": 3, "ngram_max": 2}'
```

### Next Steps to Consider
1. **Rethink categorization** - Move away from perfect/near/slant to something more useful
2. **Improve phrase generation** - Find more creative multi-word combinations
3. **Add ranking/scoring** - Surface the most useful rhymes first
4. **Consider context** - Maybe different modes for different styles (trap, boom bap, etc.)
5. **User feedback integration** - Learn from what rhymes users actually select

### Key Files
- `/backend/app/core/datamuse.py` - Core rhyme classification logic
- `/backend/app/core/rhyme_engine.py` - Main rhyme processing engine
- `/backend/app/api/routes.py` - API endpoints
- `/frontend/src/components/RhymeResults.tsx` - Frontend display logic

### Important Context
The user emphasized that **multi-syllable rhyme detection is THE most important feature**, not a complex add-on. The tool's purpose is to help find rhymes that work well in rap/hip-hop contexts, where traditional "perfect" rhymes might not be as valuable as creative sound matches.