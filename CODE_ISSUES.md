# Code Quality & Bug Backlog

The following issues were identified during code review. They are grouped by priority (High → Medium → Low) to aid planning.

## High Priority

1. **Multi-word rhyme data is silently dropped before it reaches clients**  
   *Location:* `backend/app/core/rhyme_engine.py`, `backend/app/models/schemas.py`  
   *Problem:* `_add_multi_word_phrase_rhymes` augments each fragment dictionary with `phrase_perfect`, `phrase_near`, and `phrase_slant` keys so that DOOM-style phrase endings can be surfaced. However, the `AnalyzeResponse`/`RhymeInfo` schema only allows `perfect`, `near`, `slant`, and `span`. Pydantic therefore discards the new keys during response serialization, so the enhanced data never leaves the API.  
   *Impact:* Users cannot see any of the multi-word rhyme work that the backend performs.  
   *Recommendation:* Extend `RhymeInfo` (and the frontend `RhymeInfo` type) to represent phrase-level results explicitly, or restructure the response shape so the added keys are preserved.

2. **Frontend hides phrase-level rhymes even if the backend sends them**  
   *Location:* `frontend/src/components/SuggestionPanel.tsx`  
   *Problem:* The component only considers `perfect`, `near`, and `slant` arrays when deciding whether to render a card. Any future keys such as `phrase_perfect` are ignored, so phrase rhymes would still be invisible after fixing the schema.  
   *Impact:* Blocks UI support for the multi-word rhyme feature.  
   *Recommendation:* Teach the component to render phrase rhyme sections (or a generic renderer that handles dynamic keys) so new categories appear automatically.

3. **Fragment title renders with literal quotation marks**  
   *Location:* `frontend/src/components/SuggestionPanel.tsx`  
   *Problem:* The JSX uses `"{fragment}"`, which prints the braces and quotes instead of interpolating the fragment text.  
   *Impact:* Produces confusing card titles like `"my phrase"`.  
   *Recommendation:* Replace the string literal with `{fragment}` so the fragment is rendered cleanly.

## Medium Priority

4. **Inserted rhyme suggestions always add a leading space**  
   *Location:* `frontend/src/components/BarInput.tsx`  
   *Problem:* `insertAtCursor` prefixes every insertion with a space (`' ' + text`). At the start of the textarea this creates a leading space, and when replacing selections it can leave double spaces.  
   *Impact:* Results in untidy text and forces users to clean up whitespace manually.  
   *Recommendation:* Detect whether a space is actually needed (e.g., only prefix when the cursor is not at index 0 and the preceding character is not whitespace).

5. **Local development defaults to hitting production API**  
   *Location:* `frontend/src/hooks/useRhymes.ts`  
   *Problem:* When `VITE_API_URL` is unset the hook falls back to the deployed Railway instance. This makes offline development brittle and risks spamming production while coding.  
   *Impact:* Harder to work locally and potentially noisy in production logs.  
   *Recommendation:* Default to `http://localhost:8001` (or read from Vite proxy) and require explicit opt-in for production URLs.

