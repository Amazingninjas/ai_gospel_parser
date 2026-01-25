#!/usr/bin/env python3
"""
Reference Text Configuration
=============================
Modular configuration for enabling/disabling reference texts.

Allows clients to customize which scholarly sources are included in their research.

Author: AI Gospel Parser Project
Date: 2026-01-18
"""

import os
from typing import Dict, List, Optional

# --- REFERENCE TEXT CONFIGURATION ---

class ReferenceTextConfig:
    """
    Configuration for reference texts with enable/disable flags.

    Each text can be independently enabled/disabled for client customization.
    """

    # Core lexicon (always recommended)
    THAYERS_ENABLED = os.getenv("ENABLE_THAYERS", "true").lower() == "true"

    # Additional reference texts (optional)
    MOULTON_MILLIGAN_ENABLED = os.getenv("ENABLE_MOULTON_MILLIGAN", "true").lower() == "true"
    ROBERTSON_GRAMMAR_ENABLED = os.getenv("ENABLE_ROBERTSON_GRAMMAR", "true").lower() == "true"
    JOSEPHUS_ENABLED = os.getenv("ENABLE_JOSEPHUS", "true").lower() == "true"
    ROBERTSON_WORD_PICTURES_ENABLED = os.getenv('ENABLE_ROBERTSON_WORD_PICTURES', 'true').lower() == 'true'
    VINCENT_WORD_STUDIES_ENABLED = os.getenv('ENABLE_VINCENT_WORD_STUDIES', 'true').lower() == 'true'

    # Future texts (for when you add more)
    BDAG_ENABLED = os.getenv("ENABLE_BDAG", "false").lower() == "true"  # Commercial, requires license
    LOUW_NIDA_ENABLED = os.getenv("ENABLE_LOUW_NIDA", "false").lower() == "true"  # Commercial
    HEBREW_LEXICON_ENABLED = os.getenv("ENABLE_HEBREW_LEXICON", "false").lower() == "true"

    @classmethod
    def get_enabled_texts(cls) -> List[str]:
        """Return list of enabled reference text names."""
        enabled = []
        if cls.THAYERS_ENABLED:
            enabled.append("Thayer's Greek Lexicon")
        if cls.MOULTON_MILLIGAN_ENABLED:
            enabled.append("Moulton-Milligan Vocabulary")
        if cls.ROBERTSON_GRAMMAR_ENABLED:
            enabled.append("Robertson's Grammar")
        if cls.JOSEPHUS_ENABLED:
            enabled.append("Josephus Works")
        if cls.ROBERTSON_WORD_PICTURES_ENABLED:
            enabled.append("Robertson's Word Pictures")
        if cls.VINCENT_WORD_STUDIES_ENABLED:
            enabled.append("Vincent's Word Studies")
        if cls.BDAG_ENABLED:
            enabled.append("BDAG Lexicon")
        if cls.LOUW_NIDA_ENABLED:
            enabled.append("Louw-Nida Semantic Domains")
        if cls.HEBREW_LEXICON_ENABLED:
            enabled.append("Hebrew Lexicon")
        return enabled

    @classmethod
    def get_config_summary(cls) -> str:
        """Return formatted summary of configuration."""
        lines = ["Reference Text Configuration:"]
        lines.append(f"  - Thayer's Lexicon: {'✓ ENABLED' if cls.THAYERS_ENABLED else '✗ DISABLED'}")
        lines.append(f"  - Moulton-Milligan: {'✓ ENABLED' if cls.MOULTON_MILLIGAN_ENABLED else '✗ DISABLED'}")
        lines.append(f"  - Robertson Grammar: {'✓ ENABLED' if cls.ROBERTSON_GRAMMAR_ENABLED else '✗ DISABLED'}")
        lines.append(f"  - Josephus Works: {'✓ ENABLED' if cls.JOSEPHUS_ENABLED else '✗ DISABLED'}")
        lines.append(f"  - Robertson's Word Pictures: {'✓ ENABLED' if cls.ROBERTSON_WORD_PICTURES_ENABLED else '✗ DISABLED'}")
        lines.append(f"  - Vincent's Word Studies: {'✓ ENABLED' if cls.VINCENT_WORD_STUDIES_ENABLED else '✗ DISABLED'}")

        if cls.BDAG_ENABLED or cls.LOUW_NIDA_ENABLED or cls.HEBREW_LEXICON_ENABLED:
            lines.append("\nCommercial/Licensed Texts:")
            if cls.BDAG_ENABLED:
                lines.append("  - BDAG: ✓ ENABLED")
            if cls.LOUW_NIDA_ENABLED:
                lines.append("  - Louw-Nida: ✓ ENABLED")
            if cls.HEBREW_LEXICON_ENABLED:
                lines.append("  - Hebrew Lexicon: ✓ ENABLED")

        return "\n".join(lines)

    @classmethod
    def validate_config(cls) -> List[str]:
        """
        Validate configuration and return list of warnings.

        Returns:
            List of warning messages (empty if no warnings)
        """
        warnings = []

        # Warn if Thayer's is disabled
        if not cls.THAYERS_ENABLED:
            warnings.append("WARNING: Thayer's Lexicon is disabled - this is the core lexicon!")

        # Warn if commercial texts are enabled without files
        if cls.BDAG_ENABLED:
            warnings.append("INFO: BDAG is enabled but requires commercial license")
        if cls.LOUW_NIDA_ENABLED:
            warnings.append("INFO: Louw-Nida is enabled but requires commercial license")

        return warnings


# --- CLIENT PRESETS ---

class ClientPresets:
    """
    Pre-configured presets for common client types.

    Makes it easy to configure for different use cases.
    """

    @staticmethod
    def academic_full() -> Dict[str, bool]:
        """Full academic configuration - all texts enabled."""
        return {
            "THAYERS_ENABLED": True,
            "MOULTON_MILLIGAN_ENABLED": True,
            "ROBERTSON_GRAMMAR_ENABLED": True,
            "JOSEPHUS_ENABLED": True,
        }

    @staticmethod
    def basic() -> Dict[str, bool]:
        """Basic configuration - Thayer's only."""
        return {
            "THAYERS_ENABLED": True,
            "MOULTON_MILLIGAN_ENABLED": False,
            "ROBERTSON_GRAMMAR_ENABLED": False,
            "JOSEPHUS_ENABLED": False,
        }

    @staticmethod
    def linguistic_focus() -> Dict[str, bool]:
        """Linguistic focus - lexicon + grammar."""
        return {
            "THAYERS_ENABLED": True,
            "MOULTON_MILLIGAN_ENABLED": True,
            "ROBERTSON_GRAMMAR_ENABLED": True,
            "JOSEPHUS_ENABLED": False,
        }

    @staticmethod
    def historical_focus() -> Dict[str, bool]:
        """Historical focus - lexicon + Josephus."""
        return {
            "THAYERS_ENABLED": True,
            "MOULTON_MILLIGAN_ENABLED": False,
            "ROBERTSON_GRAMMAR_ENABLED": False,
            "JOSEPHUS_ENABLED": True,
        }

    @staticmethod
    def conservative_christian() -> Dict[str, bool]:
        """Conservative Christian - may prefer not to use Josephus as primary source."""
        return {
            "THAYERS_ENABLED": True,
            "MOULTON_MILLIGAN_ENABLED": True,
            "ROBERTSON_GRAMMAR_ENABLED": True,
            "JOSEPHUS_ENABLED": False,  # Some may prefer biblical sources only
        }

    @staticmethod
    def apply_preset(preset_name: str) -> None:
        """
        Apply a preset configuration.

        Args:
            preset_name: Name of preset (academic_full, basic, linguistic_focus, etc.)
        """
        presets = {
            'academic_full': ClientPresets.academic_full(),
            'basic': ClientPresets.basic(),
            'linguistic_focus': ClientPresets.linguistic_focus(),
            'historical_focus': ClientPresets.historical_focus(),
            'conservative_christian': ClientPresets.conservative_christian(),
        }

        if preset_name not in presets:
            raise ValueError(f"Unknown preset: {preset_name}")

        config = presets[preset_name]
        for key, value in config.items():
            os.environ[key] = str(value).lower()


# --- USAGE EXAMPLES ---

if __name__ == "__main__":
    print("=" * 60)
    print("REFERENCE TEXT CONFIGURATION")
    print("=" * 60)

    # Show current configuration
    print("\n" + ReferenceTextConfig.get_config_summary())

    # Show enabled texts
    print(f"\nEnabled texts ({len(ReferenceTextConfig.get_enabled_texts())}):")
    for text in ReferenceTextConfig.get_enabled_texts():
        print(f"  - {text}")

    # Validate configuration
    warnings = ReferenceTextConfig.validate_config()
    if warnings:
        print("\nConfiguration Warnings:")
        for warning in warnings:
            print(f"  {warning}")
    else:
        print("\n✓ Configuration valid - no warnings")

    # Show available presets
    print("\n" + "=" * 60)
    print("AVAILABLE PRESETS")
    print("=" * 60)
    print("\n1. academic_full - All texts enabled (scholars, researchers)")
    print("2. basic - Thayer's only (beginners, simple lookups)")
    print("3. linguistic_focus - Lexicon + Grammar (language study)")
    print("4. historical_focus - Lexicon + Josephus (historical context)")
    print("5. conservative_christian - Biblical sources focus")

    print("\nTo use a preset in .env file:")
    print('  REFERENCE_PRESET="academic_full"')
    print("\nOr set individual flags:")
    print('  ENABLE_THAYERS="true"')
    print('  ENABLE_MOULTON_MILLIGAN="true"')
    print('  ENABLE_ROBERTSON_GRAMMAR="false"')
    print('  ENABLE_JOSEPHUS="false"')

    print("\n" + "=" * 60)
