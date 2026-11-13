# redactgate on Gretel synthetic_pii_finance_multilingual, test (443 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **900/1293 = 69.6%**
- Characters of personal data masked: 20569/25509 = 80.6%
- Documents with at least one labelled personal value left unmasked: 198/443 = 44.7%
- Masked characters inside a labelled span (precision lower bound): 69.7%
- Time: 58 s, 131 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 398 | 551 | 72% |
| company (not personal; masked only as ORG/any) | 305 | 412 | 74% |
| street_address | 252 | 362 | 70% |
| date (not personal; masked only as ORG/any) | 3 | 132 | 2% |
| phone_number | 65 | 71 | 92% |
| email | 34 | 37 | 92% |
| time (not personal; masked only as ORG/any) | 0 | 29 | 0% |
| date_of_birth | 17 | 24 | 71% |
| customer_id | 11 | 24 | 46% |
| iban | 23 | 23 | 100% |
| bban | 12 | 21 | 57% |
| swift_bic_code | 17 | 18 | 94% |
| passport_number | 2 | 15 | 13% |
| ipv4 | 15 | 15 | 100% |
| bank_routing_number | 0 | 14 | 0% |
| credit_card_number | 7 | 14 | 50% |
| user_name | 0 | 14 | 0% |
| employee_id | 1 | 12 | 8% |
| first_name | 10 | 11 | 91% |
| api_key | 9 | 9 | 100% |
| ssn | 4 | 9 | 44% |
| account_pin | 3 | 9 | 33% |
| last_name | 5 | 9 | 56% |
| credit_card_security_code | 1 | 8 | 12% |
| driver_license_number | 1 | 7 | 14% |
| ipv6 | 7 | 7 | 100% |
| local_latlng | 5 | 6 | 83% |
| date_time (not personal; masked only as ORG/any) | 0 | 3 | 0% |
| password | 1 | 3 | 33% |
