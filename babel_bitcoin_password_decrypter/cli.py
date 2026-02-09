"""
Command-line interface for babel-bitcoin-password-decrypter.
"""

import argparse
import sys

from .converter import seed_to_babel, babel_to_seed, format_babel_string


def main():
    parser = argparse.ArgumentParser(
        description="Convert BIP39 seed phrases to memorable babel strings and back.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert seed phrase to babel string
  babel-btc encode "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

  # Convert babel string back to seed phrase
  babel-btc decode "abebeiabebeiabebeiabebeiabebeiabebeiabebeiabebeiabebeiabebeiabebeiaibelt"

  # Show formatted output (easier to memorize)
  babel-btc encode --format "abandon abandon ... about"
        """
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Encode command
    encode_parser = subparsers.add_parser(
        'encode',
        help='Convert a seed phrase to a babel string'
    )
    encode_parser.add_argument(
        'seed_phrase',
        help='12-word BIP39 seed phrase (in quotes)'
    )
    encode_parser.add_argument(
        '--format', '-f',
        action='store_true',
        help='Format output with hyphens for readability'
    )

    # Decode command
    decode_parser = subparsers.add_parser(
        'decode',
        help='Convert a babel string back to a seed phrase'
    )
    decode_parser.add_argument(
        'babel_string',
        help='The babel string to decode'
    )

    args = parser.parse_args()

    try:
        if args.command == 'encode':
            babel = seed_to_babel(args.seed_phrase)
            if args.format:
                print(format_babel_string(babel))
            else:
                print(babel)

        elif args.command == 'decode':
            # Remove any formatting (hyphens, spaces)
            clean_babel = args.babel_string.replace('-', '').replace(' ', '')
            seed = babel_to_seed(clean_babel)
            print(seed)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
