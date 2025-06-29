from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest, AnalyzeResponse, SuggestionRequest
from app.core.rhyme_engine import RhymeEngine
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize rhyme engine
rhyme_engine = RhymeEngine()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_bar(request: AnalyzeRequest):
    """
    Analyze a bar of text for rhyme suggestions.
    """
    try:
        if not request.bar.strip():
            raise HTTPException(status_code=400, detail="Bar cannot be empty")
        
        fragments = rhyme_engine.analyze_bar(
            request.bar,
            max_results=request.max_results,
            ngram_max=request.ngram_max
        )
        
        return AnalyzeResponse(
            fragments=fragments,
            original_bar=request.bar
        )
    except Exception as e:
        logger.error(f"Error analyzing bar: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/suggestions/{word}")
async def get_word_suggestions(word: str, request: SuggestionRequest):
    """
    Get rhyme suggestions for a specific word.
    """
    try:
        suggestions = rhyme_engine.get_suggestions_for_word(
            word,
            rhyme_type=request.rhyme_type,
            max_results=10
        )
        
        return {
            "word": word,
            "suggestions": suggestions
        }
    except Exception as e:
        logger.error(f"Error getting suggestions for '{word}': {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "rhymeslikedimes-api"}