# SourceWeave

SourceWeave links research claims to their sources and prioritizes unsupported or weakly cross-checked statements.

## Customer and price

- Customer: students, independent researchers and science-project teams
- Price: one-time purchase, ₩11,900

## Core features

1. Register validated HTTPS sources with type and credibility score.
2. Create claims and attach supporting sources.
3. Rank evidence gaps, single-source claims and independently cross-checked claims.

## Run

```bash
python3 -m http.server 4175 -d app
```

Open `http://127.0.0.1:4175`.

## Test

```bash
node --test tests/*.test.js
```

No package installation is required; the app has zero external runtime dependencies.

## Privacy and limitations

Data remains in localStorage. Do not store private participant information or unpublished confidential material. Credibility scores are user judgments, and a high score or multiple domains do not prove a claim is true; users must read the original material and follow the citation rules of their institution.
