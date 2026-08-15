# SpoolReserve

SpoolReserve records the measured weight of 3D-printer filament spools and checks whether a selected spool can finish a job after a configurable safety margin.

## Customer and price

- Customer: hobby FDM users and small maker studios
- Price: one-time purchase, ₩9,900

## Core features

1. Register a spool from gross weight, empty-spool weight, material and purchase price.
2. Match a slicer estimate plus safety margin against compatible spools.
3. Record consumption and track remaining grams and stock value locally.

## Run

```bash
python3 -m http.server 4173 -d app
```

Open `http://127.0.0.1:4173`.

## Test

```bash
node --test tests/*.test.js
```

No package installation is required; the application has zero external runtime dependencies.

## Privacy and limitations

Data stays in the browser's localStorage. Do not store personal or payment information. Weight estimates do not account for failed prints, purge towers, moisture or scale calibration; leave a practical margin and verify the spool before a long unattended job.
