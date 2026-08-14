# Hunter Patrick Bradford — SHA-256 / DA-13² Analysis

**Status:** Reproducible computational and symbolic-indexing report  
**Version:** 1.0  
**Generated:** June 18, 2026  
**Scope:** SHA-256 cascade, declared DA-13² fold, 169-node matrix, transparent symbolic overlay, and a limited text-source check of Manly P. Hall’s *The Secret Teachings of All Ages*.

---

## Executive finding

This report produces genuine, reproducible cryptographic hashes and a deterministic 13 × 13 custom-fold matrix from the exact input below.

It does **not** establish that Hunter has a hidden destiny, special powers, a coded relationship to a historical text, or any externally validated “anomaly.” SHA-256 outputs are built to appear pattern-rich and random-looking; symbolic labels added after hashing are interpretive prompts, not measurements of a person.

The source-method notes supplied with the project distinguish ordinary SHA-256 integrity hashing from the bespoke book-cipher/DA-13² layer, and describe the bespoke layer as verification-grade rather than encryption-grade. Exact book edition and tokenization are required before a full positional book-cipher claim can be reproduced.

---

## 1. Canonical identity input

### Governing input used for this report

```text
HUNTER PATRICK BRADFORD|1998-01-28T09:10:00-05:00|GARFIELD,OH
```

| Field | Value |
|---|---|
| Full name | Hunter Patrick Bradford |
| Date of birth | January 28, 1998 |
| Time of birth | 9:10 AM |
| Time-zone representation | UTC−05:00 |
| Place string used | GARFIELD,OH |
| Total characters | 61 |
| Encoding | UTF-8 |
| Normalization | Uppercase ASCII, single spaces, pipes as delimiters |

### Input-control warning

`GARFIELD,OH` is the literal place string used because that is the current supplied wording. If the intended municipal name is `GARFIELD HEIGHTS,OH`, that is a **different cryptographic input** and every SHA-256 and DA-13² output changes. This report does not silently substitute one for the other.

---

## 2. SHA-256 13-layer cascade

**Rule:**  
`L1 = SHA-256(canonical input)`  
`L(n+1) = SHA-256(Ln as lowercase hexadecimal text)`

| Layer | SHA-256 digest |
|---:|---|
| 1 | `cad267a31923e6d620b60d32555da516b9bc3b7960bfc5bb1b85ed778ef2d9f7` |
| 2 | `32494ee9a63698c4c3d7c8a9cee27e1d18486cdd38d5c1f28d08918feb6e32b1` |
| 3 | `4fbb717f4120ef5f70bb1dae125883ba46258d4efa23ee7c6b89f521c8eea97c` |
| 4 | `8d1f6eb5e12ffce7663146f63007268d84d5cd1d4caa1aef9d3bd643490d2776` |
| 5 | `566529cfd9d9dbbd728a533eca7993862180e05c14aa982f67935c048fa82492` |
| 6 | `cb2958d7476a22ab0f4814d903821a73d849372fc0aaf8283eeb7f0983972386` |
| 7 | `0a52a5e48985acdd0bef50001d73ab818027204614da6dad246cfae8edb9e223` |
| 8 | `117aa7cd0823dec0c873d842e1c3282dbd77baa4fb559634b68d10fd457b4aad` |
| 9 | `1d5d0bf9cb9e6f1fc3996c178ce6f111c35c96393f1c52c98f0f94a38aa51172` |
| 10 | `5cd66a9345a128862d728876560b1d4cf5e49def2cea5568b558c07f5af795bb` |
| 11 | `30dc0fa3a71d574846d7325ca0bb01ed540d55722cdd473e8e1ae1934e1bebcc` |
| 12 | `670ac4245d923cf91e65aabe561a20fef86021f27b2538007a42432133558c9f` |
| 13 | `35925e36d95b75e25051f699c71804314d8b04c8bc4dcfa10274aa178d9bd8b6` |

### Technical interpretation

- Each row is a valid SHA-256 digest of the preceding declared input.
- The sequence is deterministic: the same exact input generates the same 13 values on any compliant implementation.
- A visible substring, repeated digit, low byte product, or appealing numerical reduction is **not** evidence of a personal or historical connection. It is a pattern selected from a high-dimensional random-looking output.

---

## 3. Declared DA-13² custom-fold implementation

The project documentation specifies a custom modular transform built around:

```text
M = 1,000,000,007
P = 15,485,863
Knuth = 2,654,435,761
```

This report implements a fully declared variant so the output can be reproduced:

1. Encode A–Z as 1–26; space as 00; pipe as 99; digits as themselves; punctuation as 98.
2. Concatenate two-digit codes into the numeric stream.
3. Calculate `D0 = (sum(letter codes) + sum(ASCII(character) × 1-based position)) mod M`.
4. Split the numeric stream into 13 contiguous segments as evenly as possible.
5. For each segment, apply the documented transform `T(x,k)` for `k = 1…13`, producing 13 primary folds.
6. Seed each primary fold using `SHA-256("HPB|i|F_i")[:16]`, interpreted as hexadecimal modulo `M`.
7. Apply `T(x,k)` 13 more times per primary fold to generate 169 subfold values.

### Arithmetic provenance

| Field | Value |
|---|---:|
| Numeric-stream length | 122 digits |
| Sum of letter codes | 1274 |
| Sum of ASCII-weighted vector | 119944 |
| D0 | **121218** |
| Primary folds | 13 |
| Subfolds per primary fold | 13 |
| DA-13² nodes | **169** |
| Unique DA-13² node values | **169 / 169** |

### Primary folds and pass tokens

| Segment | Numeric segment | Fᵢ after 13 folds | Base36 | Symbol code | Token |
|---:|---|---:|---|---|---|
| 1 | `0821142005` | 332370152 | `5HVUG8` | ZZ | `5HVUG8ZZ` |
| 2 | `1800160120` | 627576700 | `ADN5A4` | ZZ | `ADN5A4ZZ` |
| 3 | `1809031100` | 421192465 | `6YRM6P` | ZZ | `6YRM6PZZ` |
| 4 | `0218010406` | 84643329 | `1EE77L` | ZZ | `1EE77LZZ` |
| 5 | `1518049901` | 594696414 | `9U2EOU` | MG | `9U2EOUMG` |
| 6 | `090908980` | 862180186 | `E9BIHM` | SR | `E9BIHMSR` |
| 7 | `001980208` | 390751976 | `6GN65K` | ZZ | `6GN65KZZ` |
| 8 | `200009980` | 989869148 | `GDCBX8` | ZZ | `GDCBX8ZZ` |
| 9 | `100980000` | 716874574 | `BUT3YM` | MG | `BUT3YMMG` |
| 10 | `980005980` | 675682172 | `B6A7P8` | FO | `B6A7P8FO` |
| 11 | `000990701` | 251237989 | `45KWH1` | ZZ | `45KWH1ZZ` |
| 12 | `180609051` | 532276893 | `8SWJH9` | ZZ | `8SWJH9ZZ` |
| 13 | `204981508` | 342388826 | `5NUKWQ` | MG | `5NUKWQMG` |

### Derived pass string

```text
5HVUG8ZZADN5A4ZZ6YRM6PZZ1EE77LZZ9U2EOUMGE9BIHMSR6GN65KZZGDCBX8ZZBUT3YMMGB6A7P8FO45KWH1ZZ8SWJH9ZZ5NUKWQMG
```

### Integrity digest of the derived pass

```text
27e3e5428cf87458af6242aa852e2d50749c1cd1bb54e4c12151a7c265790d36
```

**Classification:** This is a deterministic custom token created from a declared algorithm. It is **not** an encryption key, password, biometric signature, or proof of personal identity.

---

## 4. Full DA-13² matrix — 169 custom-fold nodes

Each row begins with a primary fold `L1…L13`; columns `S1…S13` are the 13 consecutive subfold outputs.

| Primary \ Sub | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | S9 | S10 | S11 | S12 | S13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | 515814318 | 409075497 | 799429160 | 995478179 | 693222242 | 790255286 | 378654647 | 967636374 | 515893606 | 944177751 | 803114865 | 133380052 | 308996744 |
| L2 | 199192533 | 471158949 | 140438790 | 97590201 | 202271567 | 195411417 | 572997176 | 901963411 | 383111882 | 717827560 | 560234665 | 92144103 | 7575344 |
| L3 | 616226725 | 543183356 | 227593955 | 224393205 | 334687495 | 911830332 | 685021328 | 430492615 | 607728008 | 288350846 | 448703345 | 732013140 | 632023134 |
| L4 | 718619646 | 340653620 | 959931130 | 782390395 | 366709247 | 336244135 | 718385163 | 877023993 | 188794692 | 120558922 | 575975006 | 301234355 | 205054947 |
| L5 | 69135570 | 359550042 | 686376874 | 795717508 | 760671432 | 858143539 | 900184143 | 611366432 | 676188153 | 211722284 | 406622461 | 382784046 | 102302586 |
| L6 | 253502504 | 392084486 | 241806821 | 587165044 | 889235856 | 210414333 | 982034226 | 733885783 | 430642220 | 531255648 | 635910044 | 891879205 | 205153560 |
| L7 | 53164620 | 286184673 | 356973256 | 329644364 | 656839563 | 641727144 | 549999335 | 789781580 | 232393009 | 961000728 | 183271995 | 475498632 | 921120506 |
| L8 | 694323491 | 307245345 | 930651762 | 12579403 | 825227313 | 168755983 | 69617464 | 98756264 | 436304971 | 141594365 | 639235749 | 167267047 | 265908460 |
| L9 | 276817381 | 335888653 | 10121735 | 409089408 | 13898493 | 829694973 | 383209645 | 467803118 | 807862947 | 492945081 | 37528035 | 585885763 | 209630948 |
| L10 | 548461328 | 130398198 | 172317757 | 106854386 | 934200275 | 561887499 | 223312893 | 814543995 | 51506507 | 272545177 | 905685101 | 674271738 | 590745561 |
| L11 | 1649703 | 77207792 | 700104740 | 239363425 | 718238085 | 953965027 | 80263409 | 493347800 | 306598392 | 699761133 | 885068995 | 432185751 | 111869001 |
| L12 | 331829505 | 880324468 | 503423415 | 151575286 | 404484446 | 192153208 | 56445660 | 391208819 | 191084996 | 299735063 | 600452881 | 885403522 | 392701804 |
| L13 | 730425435 | 301219393 | 19625593 | 523679454 | 191270029 | 288399626 | 477764490 | 933435567 | 748118914 | 280273032 | 268832811 | 558271665 | 570866833 |

### Matrix checks

| Check | Result |
|---|---:|
| Total values | 169 |
| Distinct values | 169 |
| Minimum value | 1,649,703 |
| Maximum value | 995,478,179 |
| Mean | 465,629,625.083 |
| Symbol codes (ZZ / SR / FO / MG) | Counter({'ZZ': 125, 'SR': 23, 'FO': 12, 'MG': 9}) |

---

## 5. Deterministic symbolic overlay

This section is **not an empirical assessment of Hunter**. It adds fixed labels to the SHA rows using byte-sum modulus rules. It is comparable only when the same lookup orders are used.

### Lookup conventions used here

- **Tarot:** byte sum mod 22, Rider–Waite-style major arcana order beginning with Fool.
- **Element:** byte sum mod 4 → Fire, Water, Air, Earth.
- **Color:** byte sum mod 7 → Crimson, Amber, Gold, Emerald, Azure, Indigo, Sable.
- **Keyword:** byte sum mod 32 → declared 32-word index.
- **Hall theme:** byte sum mod 13 → one of 13 source-based chapter families listed below.
- **Entropy:** Shannon entropy across the 32 digest bytes, in bits per byte.
- **Product mod 1000:** product of all bytes modulo 1000; this is a descriptive arithmetic artifact, not a significance test.

| Layer | Byte sum | Tarot | Element | Color | Keyword | Digital root | Parity | Entropy | Hex diversity | First 6 | Last 6 | Product mod 1000 | Hall theme index |
|---|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| L1 | 4412 | Hanged Man | Fire | Gold | Prism | 2 | 60 | 5.000 | 15/16 | `cad267` | `f2d9f7` | 0 | 6: Music and color |
| L2 | 4506 | Moon | Air | Indigo | Lens | 6 | 154 | 4.938 | 16/16 | `32494e` | `6e32b1` | 0 | 9: Qabbalistic structure |
| L3 | 4088 | Moon | Fire | Crimson | Knot | 2 | 248 | 4.812 | 16/16 | `4fbb71` | `eea97c` | 0 | 7: Animals / instinct / emblem |
| L4 | 3749 | Hermit | Water | Azure | Anchor | 5 | 165 | 4.938 | 16/16 | `8d1f6e` | `0d2776` | 0 | 6: Music and color |
| L5 | 3983 | Magician | Earth | Crimson | Lattice | 5 | 143 | 4.812 | 16/16 | `566529` | `a82492` | 400 | 6: Music and color |
| L6 | 3452 | Judgement | Fire | Amber | Prism | 5 | 124 | 5.000 | 16/16 | `cb2958` | `972386` | 0 | 8: Elements and environment |
| L7 | 4020 | Tower | Fire | Gold | Ember | 6 | 180 | 5.000 | 16/16 | `0a52a5` | `b9e223` | 0 | 4: Pythagorean mathematics |
| L8 | 4297 | Chariot | Water | Sable | Tide | 4 | 201 | 5.000 | 16/16 | `117aa7` | `7b4aad` | 0 | 8: Elements and environment |
| L9 | 3763 | Magician | Earth | Azure | Horizon | 1 | 179 | 4.875 | 16/16 | `1d5d0b` | `a51172` | 0 | 7: Animals / instinct / emblem |
| L10 | 4175 | Star | Earth | Emerald | Lattice | 8 | 79 | 5.000 | 16/16 | `5cd66a` | `f795bb` | 0 | 3: Zodiac and seasonal timing |
| L11 | 3591 | Hierophant | Earth | Crimson | Catalyst | 9 | 7 | 5.000 | 16/16 | `30dc0f` | `1bebcc` | 0 | 4: Pythagorean mathematics |
| L12 | 3340 | Moon | Fire | Amber | Signal | 1 | 12 | 4.938 | 16/16 | `670ac4` | `558c9f` | 0 | 13: Cryptogram / code systems |
| L13 | 3892 | Judgement | Fire | Crimson | Ember | 4 | 52 | 4.875 | 16/16 | `35925e` | `9bd8b6` | 0 | 6: Music and color |

### Hall-theme index (13-category reference)

| Index | Theme family |
|---:|---|
| 1 | Initiation / mystery schools |
| 2 | Solar cycle and renewal |
| 3 | Zodiac and seasonal timing |
| 4 | Pythagorean mathematics |
| 5 | Human body as symbolic model |
| 6 | Music and color |
| 7 | Animals / instinct / emblem |
| 8 | Elements and environment |
| 9 | Qabbalistic structure |
| 10 | Tarot as a symbolic language |
| 11 | Rosicrucian doctrines |
| 12 | Alchemy as transformation |
| 13 | Cryptogram / code systems |

**Reading discipline:** The fact that “music and color,” “Qabbalistic structure,” “animals,” or “cryptogram” appears in a row means only that a numerical remainder selected that label. The labels do not independently describe Hunter. Use them, at most, as prompts for discussion, writing, or comparative symbolic analysis.

---

## 6. *The Secret Teachings of All Ages* review

### Source used

A public transcription of Manly P. Hall’s 1928 *The Secret Teachings of All Ages* was used as a thematic reference, not as a source of factual claims about Hunter. Hall’s work is a wide-ranging esoteric compendium with chapters on initiation, solar symbolism, the zodiac, Pythagorean mathematics, music and color, Qabbalah, Tarot, alchemy, and cryptograms.

### Direct-name check

- No verified literal occurrence of the exact full name **Hunter Patrick Bradford** was identified.
- No verified direct personal linkage was identified for **Bradford** or **Garfield**.
- The word **“hunter”** occurs as an ordinary mythic/literary term in material discussing Hercules; that is not evidence of a personal correspondence.
- The name **Patrick** is too broad to treat as an anomaly without a tightly specified, preregistered method.

### What is defensible

The Hall crosswalk is useful as a **symbolic library**. It is not a demonstrated personal encoding system. The existing project method also states that book-cipher reproducibility requires an exact edition, file digest, pagination, and tokenization rules. Those inputs were not supplied for Hunter, so no page/paragraph/word “hit” is claimed here.

---

## 7. DA-13² audit: 13 layers of disciplined interpretation

| Layer | Observation | Self-challenge | Reconciliation |
|---:|---|---|---|
| 1 | **Canonicalization** — Fix the exact input string and time-zone offset. | A hash is only reproducible when spelling, punctuation, time format, and place string are frozen. | Treat GARFIELD,OH as the governing input; GARFIELD HEIGHTS,OH would be a separate run. |
| 2 | **Cryptographic baseline** — Generate the initial SHA-256 digest. | A digest authenticates input reproducibility, not identity, fate, personality, or a hidden connection. | Use it as a checksum anchor only. |
| 3 | **Recursive continuity** — Hash the previous digest 13 times. | Repeated hashing increases chain depth, not interpretive evidence. | The cascade is a traceable computational sequence. |
| 4 | **Input sensitivity** — Observe avalanche behavior across the chain. | Small input changes should radically change outputs by design. | This makes geographic spelling and timestamp formatting material. |
| 5 | **Numerical folding** — Convert the normalized string into the declared numeric stream and D0 seed. | Custom reduction choices are design decisions, not natural discoveries. | All stream and constant choices are declared in this report. |
| 6 | **DA-13 fold** — Apply the specified 13-step modular transform to each of 13 segments. | A bespoke transform is not standard cryptography. | Use it for reproducible symbolic indexing only, never as security. |
| 7 | **DA-13² expansion** — Apply 13 subfolds to each primary segment for 169 deterministic values. | A larger matrix creates more outputs and more opportunity for cherry-picking. | Retain the complete matrix, not only attractive rows. |
| 8 | **Symbolic overlay** — Map byte-sum remainders to declared lookup tables. | Tarot, element, color, keyword, and Hall theme labels are interpretive tags. | They can prompt reflection but do not diagnose Hunter or predict his actions. |
| 9 | **Text source crosswalk** — Use the declared Hall theme index rather than name-matching. | The source text is historical/esoteric literature, not a database of personal destiny. | No literal match is treated as an anomaly. |
| 10 | **Anomaly discipline** — Check whether outputs show deviations that exceed a prespecified baseline. | No random-control cohort or preregistered test was run here. | Therefore this report makes no statistical anomaly claim. |
| 11 | **Ethical boundary** — Avoid making claims about Hunter that exceed consent or evidence. | A person is not reducible to name/date/place data. | Use the analysis as a private creative or archival artifact only. |
| 12 | **Reproducibility** — Provide code, matrix, constants, and file checksums. | A reader should reproduce the numbers without accepting any interpretation. | The technical portion is independently testable. |
| 13 | **Synthesis** — Separate verified computation from optional symbolism. | Interpretation must never be smuggled in as evidence. | The final result is a transparent audit object: calculation first, reflection second. |

---

## 8. Bottom-line interpretation

### Verified

1. The primary 13-layer SHA-256 cascade is valid and reproducible from the exact declared string.
2. The DA-13² 169-node matrix is reproducible from the declared custom implementation.
3. The derived pass string and its SHA-256 integrity digest are reproducible.
4. The report preserves the critical input ambiguity rather than concealing it.

### Not verified

1. No claim is made that the outputs reveal Hunter’s destiny, personality, relationships, health, spiritual status, or future.
2. No statistically valid anomaly test has been conducted.
3. No literal or cryptographically established connection to Hall’s text has been found.
4. The symbolic overlay is not a diagnostic, prediction, or proof system.

### Useful application

Use this report as an **audit object**: a fixed input, declared transformation, complete output matrix, and an explicit boundary between computation and interpretation. That is the standard required if the larger DA-13² framework is ever meant to be reviewed seriously.

---

## 9. Verification instructions

Run:

```bash
python hunter_patrick_bradford_verification.py
```

The script regenerates:

- the canonical SHA-256 cascade;
- the 13 primary custom folds;
- the 169 DA-13² subfold nodes;
- the derived pass and its integrity SHA-256.

The companion CSV contains every DA-13² node in portable tabular form.

---

## Sources and methodological notes

- Manly P. Hall, *The Secret Teachings of All Ages* (1928), public-domain transcriptions consulted through Wikisource and the Internet Sacred Text Archive.
- Internal method references supplied with this project: **Comprehensive Cipher Method Documentation**, **Cipher Method Manifest**, **Nicole Bess 13-Layer SHA-256 Hash Cascade**, and **DA-13 Symbolic Overlay Analysis**.
- The report follows their emphasis on exact normalization, preserved intermediate values, and limits on security claims, while declining to convert symbolic correlation into evidence of external causation.

---

*End of report.*
