# SkynetPunycoderGen
Unicode characters that are easy to confuse with a chosen English letter to conduct Homograph Attacks.

# About
Internationalized Domain Name (IDN) Homograph Attacks take advantage of characters from different languages that look nearly identical, such as the Latin “a” and the Cyrillic “а”. While it might look like a regular domain or email on the surface, what’s really happening behind the scenes is a character-swap using similar-looking but technically different Unicode characters.

This repository includes a small **Punycode / IDN** toolkit: a line-wise CLI encoder/decoder (`punycodegen.py`) and a **homoglyph explorer** CLI (`punycode_gen.py`) documented below.

## `punycode_gen.py` — Punycode variants for letters `a`–`z`

`punycode_gen.py` lists **Unicode characters that are easy to confuse with a chosen English letter**, together with each character’s **IDNA Punycode (ACE) label** (`xn--…`). That is useful when studying **IDN homograph** risk, comparing lookalike scripts (Latin vs Cyrillic vs Greek, mathematical alphabets, etc.), or auditing domain-like strings.
