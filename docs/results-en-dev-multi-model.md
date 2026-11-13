# redactgate on Gretel synthetic_pii_finance_multilingual, dev (500 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **1223/1409 = 86.8%**
- Characters of personal data masked: 25128/27553 = 91.2%
- Documents with at least one labelled personal value left unmasked: 101/500 = 20.2%
- Masked characters inside a labelled span (precision lower bound): 65.7%
- Time: 130 s, 259 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 521 | 621 | 84% |
| company (not personal; masked only as ORG/any) | 511 | 590 | 87% |
| street_address | 378 | 394 | 96% |
| date (not personal; masked only as ORG/any) | 2 | 168 | 1% |
| phone_number | 74 | 80 | 92% |
| email | 44 | 47 | 94% |
| time (not personal; masked only as ORG/any) | 0 | 42 | 0% |
| first_name | 23 | 29 | 79% |
| swift_bic_code | 21 | 22 | 95% |
| date_of_birth | 17 | 18 | 94% |
| api_key | 15 | 15 | 100% |
| local_latlng | 10 | 15 | 67% |
| last_name | 7 | 15 | 47% |
| credit_card_number | 13 | 15 | 87% |
| customer_id | 10 | 13 | 77% |
| bank_routing_number | 9 | 13 | 69% |
| iban | 12 | 13 | 92% |
| user_name | 7 | 12 | 58% |
| password | 6 | 11 | 55% |
| ssn | 8 | 11 | 73% |
| passport_number | 8 | 10 | 80% |
| ipv6 | 10 | 10 | 100% |
| account_pin | 4 | 9 | 44% |
| bban | 8 | 9 | 89% |
| date_time (not personal; masked only as ORG/any) | 0 | 9 | 0% |
| employee_id | 6 | 8 | 75% |
| ipv4 | 7 | 7 | 100% |
| driver_license_number | 2 | 7 | 29% |
| credit_card_security_code | 3 | 5 | 60% |
