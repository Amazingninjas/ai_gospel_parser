"""
Lexicon API Schemas
===================
Pydantic models for lexicon-related API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional


class MorphologyStats(BaseModel):
    """Morphological statistics for a Greek word"""
    total_occurrences: int = Field(..., description="Total occurrences in NT")
    tenses: Optional[dict[str, int]] = Field(None, description="Tense distribution (for verbs)")
    voices: Optional[dict[str, int]] = Field(None, description="Voice distribution (for verbs)")
    moods: Optional[dict[str, int]] = Field(None, description="Mood distribution (for verbs)")
    cases: Optional[dict[str, int]] = Field(None, description="Case distribution (for nouns)")
    numbers: Optional[dict[str, int]] = Field(None, description="Number distribution (singular/plural)")
    genders: Optional[dict[str, int]] = Field(None, description="Gender distribution (for nouns/adjectives)")
    persons: Optional[dict[str, int]] = Field(None, description="Person distribution (1st/2nd/3rd)")

    class Config:
        json_schema_extra = {
            "example": {
                "total_occurrences": 143,
                "tenses": {"Present": 78, "Aorist": 32, "Future": 16},
                "voices": {"Active": 133, "Passive": 10},
                "moods": {"Indicative": 73, "Participle": 37}
            }
        }


class LexiconEntry(BaseModel):
    """Complete lexicon entry for a Greek word"""
    strongs: str = Field(..., description="Strong's number (e.g., 'G25')")
    lemma: str = Field(..., description="Greek lemma (e.g., 'ἀγαπάω')")
    transliteration: Optional[str] = Field(None, description="Transliteration (e.g., 'agapaō')")
    pronunciation: Optional[str] = Field(None, description="Pronunciation guide")
    part_of_speech: Optional[str] = Field(None, description="Part of speech (Verb, Noun, etc.)")

    # Definitions
    definition_strongs: Optional[str] = Field(None, description="Strong's definition")
    definition_kjv: Optional[str] = Field(None, description="KJV translation definition")

    # Etymology and usage
    derivation: Optional[str] = Field(None, description="Etymology/derivation")
    usage: Optional[str] = Field(None, description="Usage notes")

    # Cross-references
    cross_refs: Optional[list[str]] = Field(None, description="Related Strong's numbers")

    # Morphology data
    morphology: Optional[MorphologyStats] = Field(None, description="Morphological statistics from NT")

    class Config:
        json_schema_extra = {
            "example": {
                "strongs": "G25",
                "lemma": "ἀγαπάω",
                "transliteration": "agapaō",
                "part_of_speech": "Verb",
                "definition_strongs": "to love (in a social or moral sense)",
                "definition_kjv": "to love",
                "morphology": {
                    "total_occurrences": 143,
                    "tenses": {"Present": 78, "Aorist": 32}
                },
                "cross_refs": ["G26", "G5368"]
            }
        }


class LexiconSearchResult(BaseModel):
    """Search result item"""
    strongs: str
    lemma: str
    transliteration: Optional[str] = None
    part_of_speech: Optional[str] = None
    definition_short: str = Field(..., description="Short definition (truncated)")
    relevance_score: Optional[float] = Field(None, description="Search relevance score")


class LexiconSearchResponse(BaseModel):
    """Response for lexicon search"""
    query: str = Field(..., description="Search query")
    results: list[LexiconSearchResult] = Field(..., description="Matching entries")
    total_results: int = Field(..., description="Total number of results")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "love",
                "results": [
                    {
                        "strongs": "G25",
                        "lemma": "ἀγαπάω",
                        "transliteration": "agapaō",
                        "part_of_speech": "Verb",
                        "definition_short": "to love (in a social or moral sense)"
                    },
                    {
                        "strongs": "G26",
                        "lemma": "ἀγάπη",
                        "transliteration": "agapē",
                        "part_of_speech": "Noun",
                        "definition_short": "love, affection, goodwill"
                    }
                ],
                "total_results": 2
            }
        }
