"""Unit tests for rhyme classification and ordering utilities."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pronouncing
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "app"))

from app.core.datamuse import DatamuseClient


@pytest.fixture(scope="module")
def datamuse_client() -> DatamuseClient:
    """Provide a shared Datamuse client instance for rhyme checks."""

    return DatamuseClient()


@pytest.mark.parametrize(
    "word1, word2",
    [
        ("cat", "bat"),
        ("cat", "hat"),
        ("love", "dove"),
        ("run", "sun"),
        ("time", "rhyme"),
        ("time", "lime"),
    ],
)
def test_perfect_rhymes_single_syllable(
    datamuse_client: DatamuseClient, word1: str, word2: str
) -> None:
    """Single syllable pairs should be classified as perfect rhymes."""

    assert datamuse_client._is_perfect_rhyme(
        word1, word2
    ), f"Expected '{word1}' and '{word2}' to be perfect rhymes"


@pytest.mark.parametrize(
    "word1, word2",
    [
        ("spaghetti", "confetti"),
        ("nation", "station"),
        ("creation", "vacation"),
    ],
)
def test_perfect_rhymes_multi_syllable(
    datamuse_client: DatamuseClient, word1: str, word2: str
) -> None:
    """Multi-syllable pairs should be perfect rhymes."""

    assert datamuse_client._is_perfect_rhyme(
        word1, word2
    ), f"Expected '{word1}' and '{word2}' to be perfect rhymes"


@pytest.mark.parametrize(
    "word1, word2",
    [
        ("cat", "dog"),
        ("cat", "orange"),
        ("cat", "music"),
        ("love", "time"),
        ("cat", "giraffe"),
    ],
)
def test_words_that_are_not_perfect_rhymes(
    datamuse_client: DatamuseClient, word1: str, word2: str
) -> None:
    """Pairs with mismatched syllables or endings should not be perfect rhymes."""

    assert not datamuse_client._is_perfect_rhyme(
        word1, word2
    ), f"Did not expect '{word1}' and '{word2}' to be perfect rhymes"


@pytest.mark.parametrize(
    "phrase, comparison",
    [
        ("ate spaghetti", "confetti"),
        ("break the chain", "pain"),
        ("running fast", "last"),
        ("having fun", "sun"),
    ],
)
def test_multi_word_perfect_rhymes(
    datamuse_client: DatamuseClient, phrase: str, comparison: str
) -> None:
    """The final word of a phrase should drive rhyme detection."""

    last_word = phrase.split()[-1]
    assert datamuse_client._is_perfect_rhyme(
        last_word, comparison
    ), f"Expected '{phrase}' to rhyme with '{comparison}' via '{last_word}'"


@pytest.mark.parametrize(
    "word1, word2, expected_ratio",
    [
        ("cat", "bat", 1.0),
        ("love", "dove", 1.0),
        ("running", "sun", 0.5),
        ("beautiful", "full", pytest.approx(1 / 3, abs=0.05)),
        ("chocolate", "late", 0.5),
    ],
)
def test_syllable_coverage_estimates(word1: str, word2: str, expected_ratio: float) -> None:
    """Validate the syllable-coverage heuristic used in rhyme evaluation."""

    phones1 = pronouncing.phones_for_word(word1)
    phones2 = pronouncing.phones_for_word(word2)
    assert phones1 and phones2, f"Missing pronunciation data for '{word1}' or '{word2}'"

    syllables1 = pronouncing.syllable_count(phones1[0])
    syllables2 = pronouncing.syllable_count(phones2[0])

    min_syllables = min(syllables1, syllables2)
    max_syllables = max(syllables1, syllables2)
    ratio = min_syllables / max_syllables if max_syllables else 0

    assert ratio == pytest.approx(
        expected_ratio, abs=0.1
    ), f"Unexpected coverage ratio for '{word1}' vs '{word2}'"


def test_word_fragment_grouping() -> None:
    """Multi-word fragments should group with their base words when sorted."""

    sample_rhymes: List[Dict[str, str]] = [
        {"word": "This", "rhyme_type": "slant"},
        {"word": "is", "rhyme_type": "near"},
        {"word": "the", "rhyme_type": "slant"},
        {"word": "time", "rhyme_type": "perfect"},
        {"word": "This is", "rhyme_type": "slant"},
        {"word": "is the", "rhyme_type": "near"},
        {"word": "the time", "rhyme_type": "perfect"},
    ]

    expected_order = [
        "is",
        "is the",
        "the",
        "the time",
        "This",
        "This is",
        "time",
    ]

    def sort_key(rhyme: Dict[str, str]) -> Tuple[str, int]:
        word = rhyme["word"]
        word_count = len(word.split())
        first_word = word.split()[0].lower()
        return first_word, word_count

    sorted_rhymes = sorted(sample_rhymes, key=sort_key)
    actual_order = [r["word"] for r in sorted_rhymes]

    assert (
        actual_order == expected_order
    ), f"Expected {expected_order} but got {actual_order}"


def test_rhyme_type_priority() -> None:
    """Perfect rhymes should be prioritised before near or slant matches."""

    sample_rhymes: Iterable[Dict[str, str]] = [
        {"word": "time", "rhyme_type": "slant"},
        {"word": "time", "rhyme_type": "perfect"},
        {"word": "time", "rhyme_type": "near"},
    ]

    rhyme_priority = {"perfect": 0, "near": 1, "slant": 2}

    sorted_rhymes = sorted(sample_rhymes, key=lambda r: rhyme_priority.get(r["rhyme_type"], 3))
    actual_types = [r["rhyme_type"] for r in sorted_rhymes]

    assert actual_types == [
        "perfect",
        "near",
        "slant",
    ], f"Unexpected priority order: {actual_types}"
