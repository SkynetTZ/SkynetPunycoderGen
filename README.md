# SkynetPunycoderGen
Unicode characters that are easy to confuse with a chosen English letter to conduct Homograph Attacks.

<img width="1400" height="933" alt="Homograph Attacks" src="https://github.com/user-attachments/assets/462e2aab-5daa-4f63-91e3-7015c863bf21" />


# About
A Homograph Attack is a type of phishing or spoofing attack where an attacker creates a fake domain name that looks visually identical (or very similar) to a legitimate website by using characters from different alphabets or similar-looking letters.

For example:

-- **Real site: paypal.com** \
-- **Fake site: paypaӏ.com**

The second domain may use a Cyrillic character instead of the normal Latin l, but to humans it looks almost the same. This technique is also called an IDN Homograph Attack because it often abuses Internationalized Domain Names (IDNs).

Internationalized Domain Name (IDN) Homograph Attacks take advantage of characters from different languages that look nearly identical, such as the Latin “a” and the Cyrillic “а”. While it might look like a regular domain or email on the surface, what’s really happening behind the scenes is a character-swap using similar-looking but technically different Unicode characters.

This repository includes a small **Punycode / IDN** toolkit: a line-wise CLI encoder/decoder (`punycodegen.py`) and a **homoglyph explorer** CLI (`punycode_gen.py`) documented below.

## `punycode_gen.py` — Punycode variants for letters `a`–`z`

`punycode_gen.py` lists **Unicode characters that are easy to confuse with a chosen English letter**, together with each character’s **IDNA Punycode (ACE) label** (`xn--…`). That is useful when studying **IDN homograph** risk, comparing lookalike scripts (Latin vs Cyrillic vs Greek, mathematical alphabets, etc.), or auditing domain-like strings.

### Requirements

- **Python 3.9+** (stdlib only; no `pip install` needed).
- **`confusables.txt`** in the **same directory** as `punycode_gen.py`.

The script resolves the data file with:

`Path(__file__).resolve().with_name("confusables.txt")`

### Obtaining `confusables.txt`

The file is part of the Unicode **Security Mechanisms** data used by [UTS #39](https://www.unicode.org/reports/tr39/).

1. Download the current release, for example:  
   [https://www.unicode.org/Public/security/latest/confusables.txt](https://www.unicode.org/Public/security/latest/confusables.txt)
2. Save it next to `punycode_gen.py` as `confusables.txt`.

If the file is missing, the script exits with an error and prints the download hint.

### Usage

**Interactive** (prompts for one letter when stdin is a TTY):

```bash
python3 punycode_gen.py
# Enter a letter (a-z): a
```

**Non-interactive** (recommended for scripts):

```bash
python3 punycode_gen.py --letter a
python3 punycode_gen.py -l z
```

**Help:**

```bash
python3 punycode_gen.py -h
```

Stdout is configured for **UTF-8** when the interpreter supports `reconfigure`, so unusual scripts print reliably in most terminals.

### Output format

For the chosen letter, the tool prints a header and one line per variant:

```text
🔎 Punycode variants for letter: 'a'

à -> xn--0ca
a -> a
А -> xn--80a
…
```

Each line is: **glyph** `->` **ACE string** (what you would see in an ASCII-only IDN label for that single code point). Some mathematical / styled letters **normalize under IDNA** to plain ASCII (for example `a`), so the right-hand side may be a single ASCII letter instead of `xn--…`.

### How variants are collected

1. **Confusables graph** — Pairs from `confusables.txt` are treated as undirected edges. Starting from the code points for the **lowercase** and **uppercase** letter, all characters in the same connected component are candidates.
2. **Latin “same base letter” expansion** — Any assigned Unicode character whose **NFD** form, with **combining marks (Mn) removed**, **casefolds** to the target letter (e.g. accented Latin letters for `a`) is included.

Results are filtered (printable, no lone control characters), then sorted by ACE string and code point for stable output.

### Performance and size

- Loading and parsing `confusables.txt` is usually on the order of **tens to low hundreds of milliseconds** on a modern machine.
- The Latin scan walks the full Unicode code space once per invocation; expect on the order of **~0.5 seconds** per letter depending on hardware.

### Limitations and ethics

- Output depends on the **version** of `confusables.txt` and on Python’s **IDNA** implementation; ACE strings may differ from other tools or registrars for edge cases.
- This tool is intended for **security research, education, and defensive review**. Do not use it to impersonate brands, phish, or register deceptive domains.

### Data license

`confusables.txt` is distributed by Unicode, Inc. under their [terms of use](https://www.unicode.org/terms_of_use.html). Keep their copyright and license notices in the file when redistributing it.

---

## License

Add a `LICENSE` file for your preferred terms if you publish this repository publicly. Code you wrote is yours to license; **`confusables.txt`** remains subject to Unicode’s terms.
