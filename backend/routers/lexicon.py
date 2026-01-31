"""
Lexicon API Router
==================
REST API endpoints for lexicon (Strong's Greek) lookups.
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional

from schemas.lexicon import (
    LexiconEntry,
    LexiconSearchResult,
    LexiconSearchResponse,
    MorphologyStats
)
from schemas.verse import ErrorResponse
from services.lexicon_service import LexiconService, get_lexicon_service


router = APIRouter()


def _entry_to_response(entry: dict) -> LexiconEntry:
    """Convert internal entry dict to LexiconEntry response model"""
    # Extract morphology if present
    morphology = None
    if entry.get('morphology'):
        morph_data = entry['morphology']
        morphology = MorphologyStats(
            total_occurrences=morph_data.get('total_occurrences', 0),
            tenses=morph_data.get('tenses'),
            voices=morph_data.get('voices'),
            moods=morph_data.get('moods'),
            cases=morph_data.get('cases'),
            numbers=morph_data.get('numbers'),
            genders=morph_data.get('genders'),
            persons=morph_data.get('persons')
        )

    return LexiconEntry(
        strongs=entry.get('strongs', ''),
        lemma=entry.get('lemma', ''),
        transliteration=entry.get('transliteration'),
        pronunciation=entry.get('pronunciation'),
        part_of_speech=entry.get('part_of_speech'),
        definition_strongs=entry.get('definition_strongs'),
        definition_kjv=entry.get('definition_kjv'),
        derivation=entry.get('derivation'),
        usage=entry.get('usage'),
        cross_refs=entry.get('cross_refs'),
        morphology=morphology
    )


@router.get(
    "/strongs/{strongs_number}",
    response_model=LexiconEntry,
    responses={
        404: {"model": ErrorResponse, "description": "Strong's number not found"}
    },
    summary="Look up by Strong's number",
    description="""
    Look up a Greek word by Strong's number.

    Examples:
    - `G25` - ἀγαπάω (to love)
    - `G26` - ἀγάπη (love, noun)
    - `25` - Also accepts without 'G' prefix

    Returns complete lexicon entry with:
    - Greek lemma and transliteration
    - Definitions (Strong's and KJV)
    - Morphological statistics from NT
    - Cross-references to related words
    """
)
async def get_strongs(
    strongs_number: str,
    lexicon_service: LexiconService = Depends(get_lexicon_service)
):
    """
    Look up lexicon entry by Strong's number.

    Args:
        strongs_number: Strong's number (e.g., 'G25', 'g25', or '25')

    Returns:
        Complete lexicon entry with definitions and morphology
    """
    entry = lexicon_service.lookup_by_strongs(strongs_number)

    if not entry:
        raise HTTPException(
            status_code=404,
            detail=f"Strong's number not found: {strongs_number}"
        )

    return _entry_to_response(entry)


@router.get(
    "/greek/{greek_word}",
    response_model=list[LexiconEntry],
    responses={
        404: {"model": ErrorResponse, "description": "Greek word not found"}
    },
    summary="Look up by Greek word",
    description="""
    Look up lexicon entries by Greek lemma.

    Note: May return multiple entries if the same Greek word has different meanings
    or different Strong's numbers.

    Example:
    - `ἀγαπάω` - Returns G25 (verb: to love)
    - `ἀγάπη` - Returns G26 (noun: love)
    """
)
async def get_greek(
    greek_word: str,
    lexicon_service: LexiconService = Depends(get_lexicon_service)
):
    """
    Look up lexicon entries by Greek word.

    Args:
        greek_word: Greek lemma (e.g., 'ἀγαπάω')

    Returns:
        List of matching entries (may be multiple)
    """
    entries = lexicon_service.lookup_by_greek(greek_word)

    if not entries:
        raise HTTPException(
            status_code=404,
            detail=f"Lexicon entry not found for '{greek_word}'. Note: The lexicon contains base forms (lemmas) only, not inflected forms. Try searching by transliteration or use the full-text search endpoint."
        )

    return [_entry_to_response(entry) for entry in entries]


@router.get(
    "/transliteration/{transliteration}",
    response_model=list[LexiconEntry],
    responses={
        404: {"model": ErrorResponse, "description": "Transliteration not found"}
    },
    summary="Look up by transliteration",
    description="""
    Look up lexicon entries by transliteration.

    Useful for users who can't type Greek characters.

    Examples:
    - `agapao` - Returns ἀγαπάω (G25)
    - `agape` - Returns ἀγάπη (G26)
    """
)
async def get_transliteration(
    transliteration: str,
    lexicon_service: LexiconService = Depends(get_lexicon_service)
):
    """
    Look up lexicon entries by transliteration.

    Args:
        transliteration: Transliterated Greek word (e.g., 'agapao')

    Returns:
        List of matching entries
    """
    entries = lexicon_service.lookup_by_transliteration(transliteration)

    if not entries:
        raise HTTPException(
            status_code=404,
            detail=f"Transliteration not found: {transliteration}"
        )

    return [_entry_to_response(entry) for entry in entries]


@router.get(
    "/search",
    response_model=LexiconSearchResponse,
    summary="Search lexicon",
    description="""
    Full-text search across all lexicon entries.

    Searches:
    - Strong's numbers
    - Greek lemmas
    - Transliterations
    - Definitions (Strong's and KJV)
    - Etymology/derivation

    Results are ranked by relevance.

    Examples:
    - `love` - Finds ἀγαπάω, ἀγάπη, φιλέω, etc.
    - `water` - Finds ὕδωρ, βαπτίζω, etc.
    - `believe` - Finds πιστεύω, πίστις, etc.
    """
)
async def search_lexicon(
    q: str = Query(..., description="Search query", min_length=1),
    limit: int = Query(20, description="Maximum results", ge=1, le=100),
    lexicon_service: LexiconService = Depends(get_lexicon_service)
):
    """
    Search lexicon with full-text query.

    Args:
        q: Search query string
        limit: Maximum number of results (default 20, max 100)

    Returns:
        Search results ranked by relevance
    """
    results = lexicon_service.search(q, limit=limit)

    # Convert to search result format
    search_results = []
    for entry, score in results:
        # Truncate definition for preview
        definition = entry.get('definition_strongs', '') or entry.get('definition_kjv', '')
        if len(definition) > 100:
            definition = definition[:97] + "..."

        search_results.append(
            LexiconSearchResult(
                strongs=entry.get('strongs', ''),
                lemma=entry.get('lemma', ''),
                transliteration=entry.get('transliteration'),
                part_of_speech=entry.get('part_of_speech'),
                definition_short=definition,
                relevance_score=score
            )
        )

    return LexiconSearchResponse(
        query=q,
        results=search_results,
        total_results=len(search_results)
    )


@router.get(
    "/stats",
    summary="Get lexicon statistics",
    description="Get statistics about the lexicon (total entries, coverage, etc.)"
)
async def get_stats(
    lexicon_service: LexiconService = Depends(get_lexicon_service)
):
    """
    Get lexicon statistics.

    Returns:
        Statistics about lexicon size and coverage
    """
    return lexicon_service.get_stats()
