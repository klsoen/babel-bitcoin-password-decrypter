"""
Main converter: seed phrase <-> pronounceable babel string.
"""

from .bip39 import mnemonic_to_entropy, entropy_to_mnemonic
from .syllables import bytes_to_syllables, syllables_to_bytes


def seed_to_babel(mnemonic: str) -> str:
    """
    Convert a 12-word BIP39 seed phrase to a pronounceable babel string.

    Example:
        "system rocket topple moment whisper tobacco club detail left sketch move arrange"
        -> "aztulinerblinken" (example, actual output depends on syllable table)
    """
    entropy = mnemonic_to_entropy(mnemonic)
    return bytes_to_syllables(entropy)


def babel_to_seed(babel_string: str) -> str:
    """
    Convert a babel string back to a BIP39 seed phrase.

    Example:
        "aztulinerblinken" -> "system rocket topple moment whisper tobacco club detail left sketch move arrange"
    """
    entropy = syllables_to_bytes(babel_string)
    return entropy_to_mnemonic(entropy)


def format_babel_string(babel: str, chunk_size: int = 4) -> str:
    """
    Format a babel string for easier reading/memorization.

    Breaks into chunks: "aztulinerblinken" -> "aztu-line-rbli-nken"
    """
    chunks = [babel[i:i + chunk_size] for i in range(0, len(babel), chunk_size)]
    return '-'.join(chunks)
