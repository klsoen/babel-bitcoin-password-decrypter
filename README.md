# Babel Bitcoin Password Decrypter

Convert BIP39 seed phrases to memorable, pronounceable "babel strings" and back.

## Concept

Instead of remembering 12 random words, remember a single pronounceable string like `aztulinerblinken`. This string encodes the same entropy as your seed phrase and can be converted back at any time.

## Installation

```bash
pip install babel-bitcoin-password-decrypter
```

## Usage

### Command Line

```bash
# Encode a seed phrase to a babel string
babel-btc encode "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

# Decode a babel string back to seed phrase
babel-btc decode "abebeiabebeiabebeiabebeiabebeiabebeiabebeiabebeiabebeiabebeiabebeiaibelt"

# Format for easier memorization
babel-btc encode --format "your twelve word seed phrase here..."
```

### Python API

```python
from babel_bitcoin_password_decrypter import seed_to_babel, babel_to_seed

# Encode
babel = seed_to_babel("abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about")
print(babel)

# Decode
seed = babel_to_seed(babel)
print(seed)
```

## Security Note

This tool does NOT add any security. It simply re-encodes the same entropy in a different format. Treat your babel string with the same security as your seed phrase.
