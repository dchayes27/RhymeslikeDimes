"""Pytest suite for validating MF DOOM-style rhyme patterns."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, Tuple

import pronouncing
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "app"))

from app.core.datamuse import DatamuseClient


@pytest.fixture(scope="module")
def datamuse_client() -> DatamuseClient:
    """Provide a shared Datamuse client for rhyme verification."""

    return DatamuseClient()


def _last_word(phrase: str) -> str:
    """Extract the final alphabetic token from a phrase."""

    return phrase.split()[-1].lower().strip(".,!?")


def _rhyme_parts(word: str) -> Tuple[str | None, str | None]:
    """Return the phonetic representation and rhyming part for a word."""

    phones = pronouncing.phones_for_word(word)
    if not phones:
        return None, None

    pronunciation = phones[0]
    return pronunciation, pronouncing.rhyming_part(pronunciation)


def _format_debug(phrase1: str, phrase2: str) -> str:
    """Generate a helpful debug string for assertion messages."""

    word1 = _last_word(phrase1)
    word2 = _last_word(phrase2)
    pronunciation1, rhyme1 = _rhyme_parts(word1)
    pronunciation2, rhyme2 = _rhyme_parts(word2)

    sections = [f"'{phrase1}' ↔ '{phrase2}'"]
    sections.append(f"words: '{word1}' vs '{word2}'")

    if pronunciation1 or pronunciation2:
        sections.append(
            "phones: "
            f"{pronunciation1 or '∅'} vs {pronunciation2 or '∅'}; "
            f"rhyming parts: {rhyme1 or '∅'} vs {rhyme2 or '∅'}"
        )

    return " | ".join(sections)


MF_DOOM_PATTERNS: Iterable[Tuple[str, str, str]] = (
    ("beat kinda", "meat grinder", "Internal rhyme: 'kinda' vs 'grinder'"),
    ("no brain", "no chain", "Perfect rhyme: 'brain' vs 'chain'"),
    ("clever nerd", "ever heard", "Perfect rhyme: 'nerd' vs 'heard'"),
    ("cookie tear", "rookie year", "Multi-syllable: 'cookie tear' vs 'rookie year'"),
    ("his hand", "gazillion grand", "End rhyme: 'hand' vs 'grand'"),
    ("price again", "hydrogen", "Complex ending: 'again' vs 'hydrogen'"),
    ("blessed be the Lord", "message board", "End rhyme: 'Lord' vs 'board'"),
    ("kinda", "grinder", "Direct test: 'kinda' vs 'grinder'"),
    ("again", "hydrogen", "Direct test: 'again' vs 'hydrogen'"),
    ("villain man", "krills in", "DOOM internal: 'man' vs 'in'"),
    ("rockin til", "clocked in", "DOOM flow: 'til' vs 'in'"),
)


@pytest.mark.parametrize("phrase1, phrase2, description", MF_DOOM_PATTERNS)
def test_mf_doom_rhyme_patterns(
    datamuse_client: DatamuseClient, phrase1: str, phrase2: str, description: str
) -> None:
    """Assert that iconic MF DOOM rhyme pairs classify as perfect rhymes."""

    word1 = _last_word(phrase1)
    word2 = _last_word(phrase2)

    assert datamuse_client._is_perfect_rhyme(
        word1, word2
    ), f"Expected a perfect rhyme for {description}: {_format_debug(phrase1, phrase2)}"
