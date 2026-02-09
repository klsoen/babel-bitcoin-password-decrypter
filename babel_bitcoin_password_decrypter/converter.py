"""
Main converter: seed phrase <-> pronounceable babel string <-> Library of Babel URL.

Flow:
  Encode: seed phrase -> entropy -> babel string (memorizable)
  Decode: babel string -> entropy -> seed phrase -> Library of Babel URL
"""
from __future__ import annotations

from .bip39 import mnemonic_to_entropy, entropy_to_mnemonic
from .syllables import bytes_to_syllables, syllables_to_bytes
from .babel_lib import search_text, coordinates_to_url


def seed_to_babel(mnemonic: str) -> str:
    """
    Convert a 12-word BIP39 seed phrase to a pronounceable babel string.

    The babel string encodes the seed's entropy and can be used to recover
    both the seed phrase and its Library of Babel location.
    """
    entropy = mnemonic_to_entropy(mnemonic)
    return bytes_to_syllables(entropy)


def babel_to_seed(babel_string: str) -> str:
    """
    Convert a babel string back to a BIP39 seed phrase.
    """
    entropy = syllables_to_bytes(babel_string)
    return entropy_to_mnemonic(entropy)


def babel_to_url(babel_string: str) -> str:
    """
    Convert a babel string to a Library of Babel URL.

    The URL, when opened, displays a page containing the seed phrase.
    """
    # Decode babel string to seed phrase
    seed_phrase = babel_to_seed(babel_string)

    # Find Library of Babel coordinates for the seed phrase text
    hex_name, wall, shelf, volume, page = search_text(seed_phrase)

    # Generate URL
    return coordinates_to_url(hex_name, wall, shelf, volume, page)


def seed_to_url(mnemonic: str) -> str:
    """
    Convert a seed phrase directly to its Library of Babel URL.
    """
    hex_name, wall, shelf, volume, page = search_text(mnemonic)
    return coordinates_to_url(hex_name, wall, shelf, volume, page)


def format_babel_string(babel: str, chunk_size: int = 4) -> str:
    """
    Format a babel string for easier reading/memorization.

    Breaks into chunks: "aztulinerblinken" -> "aztu-line-rbli-nken"
    """
    chunks = [babel[i:i + chunk_size] for i in range(0, len(babel), chunk_size)]
    return '-'.join(chunks)
