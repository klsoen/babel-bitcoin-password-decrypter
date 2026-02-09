"""
Library of Babel API integration.

Uses the actual libraryofbabel.info search API to get real coordinates.
"""
from __future__ import annotations

import re
import ssl
import urllib.request
import urllib.parse
from typing import Tuple, Optional

# Create SSL context that doesn't verify certificates (for compatibility)
_ssl_context = ssl.create_default_context()
_ssl_context.check_hostname = False
_ssl_context.verify_mode = ssl.CERT_NONE


def search_text(text: str) -> Tuple[str, int, int, int, int]:
    """
    Search Library of Babel for text and get coordinates.

    Uses the actual libraryofbabel.info search API.

    Returns: (hex_name, wall, shelf, volume, page)
    """
    # Prepare the search request
    url = "https://libraryofbabel.info/search.cgi"
    data = urllib.parse.urlencode({'find': text, 'method': 'x'}).encode('utf-8')

    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

    with urllib.request.urlopen(req, timeout=30, context=_ssl_context) as response:
        html = response.read().decode('utf-8')

    # Parse the response to extract coordinates
    # Look for the onclick handler: postform('hexname','wall','shelf','volume','page')
    match = re.search(
        r"onclick\s*=\s*\"postform\('([^']+)','(\d+)','(\d+)','(\d+)','(\d+)'",
        html
    )

    if not match:
        raise ValueError("Could not find coordinates in Library of Babel response")

    hex_name = match.group(1)
    wall = int(match.group(2))
    shelf = int(match.group(3))
    volume = int(match.group(4))
    page = int(match.group(5))

    return hex_name, wall, shelf, volume, page


def coordinates_to_url(hex_name: str, wall: int, shelf: int, volume: int, page: int) -> str:
    """Generate a Library of Babel URL from coordinates."""
    return f"https://libraryofbabel.info/book.cgi?{hex_name}-w{wall}-s{shelf}-v{volume:02d}:{page}"


def search_and_get_url(text: str) -> str:
    """
    Search for text and return the Library of Babel URL.

    This is the main function to use - it queries the real Library of Babel
    and returns a working URL.
    """
    hex_name, wall, shelf, volume, page = search_text(text)
    return coordinates_to_url(hex_name, wall, shelf, volume, page)
