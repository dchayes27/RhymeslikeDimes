"""Tests for ensuring schema serialization includes enhanced rhyme fields."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "app"))

from app.models.schemas import AnalyzeResponse


def test_rhyme_info_includes_phrase_fields_when_present():
    """Explicit phrase rhyme fields should survive serialization."""

    response = AnalyzeResponse(
        fragments={
            "villain man": {
                "perfect": ["chillin' fam"],
                "near": [],
                "slant": [],
                "phrase_perfect": ["krills in his hand"],
                "phrase_near": ["million grand"],
                "phrase_slant": [],
                "span": (0, 2),
            }
        },
        original_bar="Villain man holding krills in his hand",
    )

    fragment = response.fragments["villain man"].model_dump()

    assert fragment["phrase_perfect"] == ["krills in his hand"]
    assert fragment["phrase_near"] == ["million grand"]
    assert fragment["phrase_slant"] == []


def test_rhyme_info_populates_phrase_fields_when_missing():
    """Missing phrase rhyme keys should default to empty lists."""

    response = AnalyzeResponse(
        fragments={
            "villain": {
                "perfect": ["chillin"],
                "near": [],
                "slant": [],
                "span": (0, 1),
            }
        },
        original_bar="Villain",
    )

    fragment = response.fragments["villain"].model_dump()

    assert fragment["phrase_perfect"] == []
    assert fragment["phrase_near"] == []
    assert fragment["phrase_slant"] == []

