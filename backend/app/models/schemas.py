from pydantic import BaseModel, Field
from typing import List, Dict, Tuple, Optional


class AnalyzeRequest(BaseModel):
    bar: str = Field(..., description="The line of text to analyze for rhymes")
    max_results: int = Field(7, description="Maximum number of results per category")
    ngram_max: int = Field(3, description="Maximum n-gram size for multi-word phrases")


class RhymeInfo(BaseModel):
    perfect: List[str] = Field(default_factory=list)
    near: List[str] = Field(default_factory=list)
    slant: List[str] = Field(default_factory=list)
    phrase_perfect: List[str] = Field(
        default_factory=list,
        description="Multi-word perfect rhymes",
    )
    phrase_near: List[str] = Field(
        default_factory=list,
        description="Multi-word near rhymes",
    )
    phrase_slant: List[str] = Field(
        default_factory=list,
        description="Multi-word slant rhymes",
    )
    span: Tuple[int, int] = Field(..., description="Word span indices in original bar")


class AnalyzeResponse(BaseModel):
    fragments: Dict[str, RhymeInfo] = Field(..., description="Rhyme suggestions for each fragment")
    original_bar: str = Field(..., description="The original input bar")


class SuggestionRequest(BaseModel):
    word: str = Field(..., description="Single word to get suggestions for")
    rhyme_type: Optional[str] = Field("all", description="Type of rhyme: perfect, near, slant, or all")


class WebSocketMessage(BaseModel):
    type: str = Field(..., description="Message type: analyze, suggestion, error")
    data: Dict = Field(..., description="Message payload")

