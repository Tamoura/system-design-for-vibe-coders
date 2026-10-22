# Corridors and fees

*All numbers are fictional. This page describes `src/remit/corridors.py`, `src/remit/fees.py` and `src/remit/fx.py`. When they disagree with this page, the code wins and the page needs a fix.*

## Corridors

Customers send from Qatar, so every corridor starts in QAR. Minimum and maximum are per transfer and both are included. The first delivery method is the default.

| Code | Minimum (QAR) | Maximum (QAR) | Delivery methods | Fee schedule | Mid rate | Margin |
|---|---:|---:|---|---|---:|---:|
| QAR-BDT | 100.00 | 12,000.00 | bank_deposit, wallet | STD-C | 33.46 | 0.0175 |
| QAR-EGP | 100.00 | 15,000.00 | bank_deposit, wallet | STD-B | 13.20 | 0.0150 |
| QAR-INR | 50.00 | 25,000.00 | bank_deposit, wallet | STD-A | 22.80 | 0.0100 |
| QAR-PHP | 50.00 | 20,000.00 | bank_deposit, cash_pickup, wallet | STD-A | 15.40 | 0.0125 |
| QAR-PKR | 100.00 | 15,000.00 | bank_deposit, cash_pickup | STD-B | 77.00 | 0.0150 |

The customer rate is the mid rate less the margin, rounded half up to four decimals. A quote lasts 60 seconds. The KYC limits (daily and monthly, by tier) do not depend on the corridor; see `src/remit/limits.py`.

## Fee schedules

The tier is chosen by the whole send amount and its upper bound is included. The fee is the amount times the percent plus the flat part, rounded half up, then raised to the minimum or lowered to the cap. The express surcharge is added after the cap, so an express fee can be higher than the cap.

| Schedule | Tiers (amount up to: percent + flat, in QAR) | Minimum | Cap | Express surcharge |
|---|---|---:|---:|---:|
| STD-A | 500.00: 2% + 2.00; 2,000.00: 1.5% + 5.00; 10,000.00: 1% + 20.00; above: 0.75% + 50.00 | 5.00 | 150.00 | 15.00 |
| STD-B | 1,000.00: 2.5% + 3.00; 5,000.00: 1.8% + 10.00; above: 1.2% + 40.00 | 6.00 | 120.00 | 20.00 |
| STD-C | 1,000.00: 2.2% + 3.50; 5,000.00: 1.6% + 12.00; above: 1.1% + 45.00 | 7.00 | 130.00 | 18.00 |

Examples for QAR-BDT (`STD-C`): 500.00 QAR costs a fee of 14.50 and buys 16,437.25 BDT at 32.8745. From 7,727.27 QAR upwards the fee is the cap, 130.00, so 8,000.00 and 12,000.00 cost the same; the express surcharge of 18.00 comes on top.

## What the customer reads

A transfer on `QAR-BDT` sends the template `transfer_sent_bdt`, with the rate in the message. Every other corridor sends `transfer_sent`. Both exist in English and Arabic; the Arabic text uses Arabic-Indic digits.
