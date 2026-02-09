"""
Library of Babel coordinate system.

Implements the actual Library of Babel algorithm to generate working URLs.
Based on: https://github.com/louis-e/LibraryOfBabel-Python

The algorithm encodes text as a base-29 number, combines it with location
coordinates, and converts to a base-36 hexagon address.
"""
from __future__ import annotations

import string
from typing import Tuple

# Library of Babel character set (29 characters)
# a-z (26) + space + comma + period
CHARSET = 'abcdefghijklmnopqrstuvwxyz ,.'
CHARSET_LENGTH = len(CHARSET)  # 29

# Page dimensions
PAGE_LENGTH = 3200  # 80 chars × 40 lines

# Structure constants
MAX_WALLS = 4
MAX_SHELVES = 5
MAX_VOLUMES = 32
MAX_PAGES = 410

# Base-36 digits for hexagon address
BASE36_DIGITS = string.digits + string.ascii_lowercase


def _char_to_value(c: str) -> int:
    """Convert a character to its numeric value (0-28)."""
    if c.isalpha():
        return ord(c.lower()) - ord('a')  # a=0, z=25
    elif c == ' ':
        return 26
    elif c == ',':
        return 27
    elif c == '.':
        return 28
    else:
        return 26  # Default to space for unknown chars


def _value_to_char(v: int) -> str:
    """Convert a numeric value back to character."""
    if 0 <= v <= 25:
        return chr(ord('a') + v)
    elif v == 26:
        return ' '
    elif v == 27:
        return ','
    elif v == 28:
        return '.'
    else:
        return ' '


def _to_base36(num: int) -> str:
    """Convert an integer to base-36 string."""
    if num == 0:
        return '0'

    chars = []
    while num > 0:
        chars.append(BASE36_DIGITS[num % 36])
        num //= 36

    return ''.join(reversed(chars))


def _from_base36(s: str) -> int:
    """Convert a base-36 string to integer."""
    return int(s, 36)


def _normalize_text(text: str) -> str:
    """Normalize text for Library of Babel: lowercase, valid chars only, pad to 3200."""
    # Convert to lowercase and filter to valid characters
    result = []
    for c in text.lower():
        if c in CHARSET:
            result.append(c)
        else:
            result.append(' ')  # Replace invalid chars with space

    text = ''.join(result)

    # Pad or truncate to exactly PAGE_LENGTH characters
    if len(text) < PAGE_LENGTH:
        text = text + ' ' * (PAGE_LENGTH - len(text))
    else:
        text = text[:PAGE_LENGTH]

    return text


def search_text(text: str, wall: int = 1, shelf: int = 1, volume: int = 1, page: int = 1) -> Tuple[str, int, int, int, int]:
    """
    Find the Library of Babel coordinates for a given text.

    Args:
        text: The text to search for
        wall: Wall number (1-4), default 1
        shelf: Shelf number (1-5), default 1
        volume: Volume number (1-32), default 1
        page: Page number (1-410), default 1

    Returns: (hex_name, wall, shelf, volume, page)
    """
    text = _normalize_text(text)

    # Create library coordinate: concatenate page, volume, shelf, wall as decimal
    # Format: PPPVVSWW where P=page(3), V=volume(2), S=shelf(1), W=wall(1)
    library_coordinate = int(f"{page:03d}{volume:02d}{shelf}{wall}")

    # Convert text to base-29 number (read right to left, so reverse)
    text_value = 0
    for i, c in enumerate(reversed(text)):
        char_value = _char_to_value(c)
        text_value += char_value * (CHARSET_LENGTH ** i)

    # Combine: location * 29^3200 + text_value
    combined = library_coordinate * (CHARSET_LENGTH ** PAGE_LENGTH) + text_value

    # Convert to base-36 hexagon address
    hex_name = _to_base36(combined)

    return hex_name, wall, shelf, volume, page


def get_text_from_address(hex_name: str, wall: int, shelf: int, volume: int, page: int) -> str:
    """
    Retrieve the text at a Library of Babel address.

    Args:
        hex_name: The hexagon address
        wall: Wall number (1-4)
        shelf: Shelf number (1-5)
        volume: Volume number (1-32)
        page: Page number (1-410)

    Returns: The 3200-character text at that location
    """
    # Reconstruct library coordinate
    library_coordinate = int(f"{page:03d}{volume:02d}{shelf}{wall}")

    # Convert hexagon address from base-36 to integer
    combined = _from_base36(hex_name)

    # Extract text value by subtracting location component
    text_value = combined - library_coordinate * (CHARSET_LENGTH ** PAGE_LENGTH)

    # Convert from base-29 to text
    chars = []
    remaining = text_value
    for _ in range(PAGE_LENGTH):
        char_value = remaining % CHARSET_LENGTH
        chars.append(_value_to_char(char_value))
        remaining //= CHARSET_LENGTH

    # Reverse since we extracted from least significant
    return ''.join(reversed(chars))


def coordinates_to_url(hex_name: str, wall: int, shelf: int, volume: int, page: int) -> str:
    """Generate a Library of Babel URL from coordinates."""
    return f"https://libraryofbabel.info/book.cgi?{hex_name}:{wall}:{shelf}:{volume:02d}:{page:03d}"


def parse_url(url: str) -> Tuple[str, int, int, int, int]:
    """Parse a Library of Babel URL to extract coordinates."""
    # URL format: https://libraryofbabel.info/book.cgi?hexname:wall:shelf:volume:page
    if '?' in url:
        url = url.split('?')[1]

    parts = url.split(':')
    if len(parts) != 5:
        raise ValueError(f"Invalid Library of Babel URL format: {url}")

    hex_name = parts[0]
    wall = int(parts[1])
    shelf = int(parts[2])
    volume = int(parts[3])
    page = int(parts[4])

    return hex_name, wall, shelf, volume, page
