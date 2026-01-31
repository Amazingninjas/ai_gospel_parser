"""
Verse API Router
================
REST API endpoints for verse lookups.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Union

from schemas.verse import VerseResponse, VerseRangeResponse, BookInfo, ErrorResponse
from services.verse_service import VerseService, get_verse_service


router = APIRouter()


@router.get(
    "/{reference}",
    response_model=Union[VerseResponse, VerseRangeResponse],
    responses={
        404: {"model": ErrorResponse, "description": "Verse not found"},
        400: {"model": ErrorResponse, "description": "Invalid verse reference"}
    },
    summary="Look up a verse by reference",
    description="""
    Look up a Bible verse by reference string.

    Examples:
    - `John 3:16` - Single verse
    - `John 3:16-18` - Verse range
    - `1 John 4:8` - Numbered books
    - `Matt 5:1` - Abbreviations work too

    Returns Greek text from SBLGNT and English text from WEB for reference.
    """
)
async def get_verse(
    reference: str,
    verse_service: VerseService = Depends(get_verse_service)
):
    """
    Look up a verse by reference string.

    Args:
        reference: Verse reference (e.g., "John 3:16", "Matt 5:1-10")
        verse_service: Injected verse service

    Returns:
        VerseResponse or VerseRangeResponse with Greek + English text
    """
    # Parse the reference
    parsed = verse_service.parse_verse_reference(reference)

    if parsed is None:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid verse reference: '{reference}'. Use format like 'John 3:16'"
        )

    # Handle single verse
    if isinstance(parsed, dict):
        text, metadata = verse_service.lookup_verse(parsed)

        if text is None:
            raise HTTPException(
                status_code=404,
                detail=f"Verse not found: {reference}"
            )

        return VerseResponse(
            greek_text=text,
            english_text=metadata.get('english_text', ''),
            book=metadata['book'],
            chapter=metadata['chapter'],
            verse=metadata['verse'],
            reference=metadata['reference'],
            reference_id=metadata['reference_id']
        )

    # Handle verse range
    else:  # parsed is a list
        verses = []
        for verse_ref in parsed:
            text, metadata = verse_service.lookup_verse(verse_ref)

            if text is None:
                # Skip missing verses in range (shouldn't happen, but be defensive)
                continue

            verses.append(VerseResponse(
                greek_text=text,
                english_text=metadata.get('english_text', ''),
                book=metadata['book'],
                chapter=metadata['chapter'],
                verse=metadata['verse'],
                reference=metadata['reference'],
                reference_id=metadata['reference_id']
            ))

        if not verses:
            raise HTTPException(
                status_code=404,
                detail=f"No verses found in range: {reference}"
            )

        # Format range reference
        first = parsed[0]
        last = parsed[-1]
        range_ref = f"{first['book_name']} {first['chapter']}:{first['verse']}-{last['verse']}"

        return VerseRangeResponse(
            verses=verses,
            reference=range_ref
        )


@router.get(
    "/book/{book_code}/{chapter}/{verse}",
    response_model=VerseResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Verse not found"}
    },
    summary="Look up verse by book code, chapter, and verse numbers",
    description="""
    Look up a verse using numeric identifiers.

    Book codes (SBLGNT):
    - 61: Matthew
    - 62: Mark
    - 63: Luke
    - 64: John
    - 65: Acts
    - ... (see /books endpoint for full list)
    """
)
async def get_verse_by_code(
    book_code: int,
    chapter: int,
    verse: int,
    verse_service: VerseService = Depends(get_verse_service)
):
    """
    Look up verse by numeric book code, chapter, and verse.

    Args:
        book_code: SBLGNT book code (61-87 for NT)
        chapter: Chapter number
        verse: Verse number

    Returns:
        VerseResponse with Greek + English text
    """
    # Validate book code
    if book_code not in verse_service.CODE_TO_BOOK:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid book code: {book_code}. Use /books to see valid codes."
        )

    # Build verse reference
    verse_ref = {
        "book": book_code,
        "book_name": verse_service.CODE_TO_BOOK[book_code],
        "chapter": chapter,
        "verse": verse
    }

    # Look up verse
    text, metadata = verse_service.lookup_verse(verse_ref)

    if text is None:
        raise HTTPException(
            status_code=404,
            detail=f"Verse not found: {verse_service.CODE_TO_BOOK[book_code]} {chapter}:{verse}"
        )

    return VerseResponse(
        greek_text=text,
        english_text=metadata.get('english_text', ''),
        book=metadata['book'],
        chapter=metadata['chapter'],
        verse=metadata['verse'],
        reference=metadata['reference'],
        reference_id=metadata['reference_id']
    )


@router.get(
    "/books/list",
    response_model=list[BookInfo],
    summary="List all Bible books",
    description="""
    Get a list of all New Testament books with their codes and abbreviations.

    Useful for:
    - Autocomplete in search boxes
    - Mapping book names to codes
    - Validating user input
    """
)
async def list_books(
    verse_service: VerseService = Depends(get_verse_service)
):
    """
    Get list of all NT books.

    Returns:
        List of BookInfo objects with name, code, and abbreviations
    """
    books = verse_service.get_all_books()

    return [
        BookInfo(
            name=book["name"],
            code=book["code"],
            abbreviations=book["abbreviations"]
        )
        for book in books
    ]
