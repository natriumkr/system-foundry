# ConsignClear

ConsignClear tracks consigned inventory sales, store commission and payout deadlines in one local-first queue.

## Customer and price
- Customer: independent select shops, craft stores and gallery shops
- Price: ₩23,000 per store per month

## Core features
1. Register consigned items with validated price, commission and payout date.
2. Move items through stocked, sold and settled states.
3. Prioritize overdue payouts and calculate store fee versus consignor payout.

## Run
```bash
python3 -m http.server 4175 -d app
```
Open `http://127.0.0.1:4175`.

## Test
```bash
node --test tests/*.test.js
```
No package installation is required; there are zero external dependencies.

## Privacy and limitations
Data remains in localStorage. This MVP does not replace accounting records, tax invoices or a signed consignment agreement. Export and multi-device collaboration are not included.
