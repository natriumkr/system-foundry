# MakeupLedger

MakeupLedger helps small recurring-lesson studios manage replacement-session credits created by absences and cancellations.

## Customer and price

- Customer: small music, art and language academies
- Price: ₩21,000 per studio per month

## Core features

1. Issue validated make-up credits with sessions, expiry and per-session value.
2. Prioritize expired and near-expiry promises.
3. Redeem sessions while tracking outstanding sessions and liability value.

## Run

```bash
python3 -m http.server 4174 -d app
```

Open `http://127.0.0.1:4174`.

## Test

```bash
node --test tests/*.test.js
```

No package installation is required; the application has zero external runtime dependencies.

## Privacy and limitations

Data stays in localStorage. Use non-sensitive learner labels and do not enter contact, payment, medical or authentication information. The MVP does not send reminders, book calendars or interpret local refund law; studio policy and final scheduling remain the operator's responsibility.
