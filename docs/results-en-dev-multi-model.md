# redactgate on Gretel synthetic_pii_finance_multilingual, dev (500 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **1183/1409 = 84.0%**
- Characters of personal data masked: 24446/27553 = 88.7%
- Documents with at least one labelled personal value left unmasked: 119/500 = 23.8%
- Masked characters inside a labelled span (precision lower bound): 64.9%
- Time: 72 s, 144 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 521 | 621 | 84% |
| company (not personal; masked only as ORG/any) | 511 | 590 | 87% |
| street_address | 354 | 394 | 90% |
| date (not personal; masked only as ORG/any) | 2 | 168 | 1% |
| phone_number | 74 | 80 | 92% |
| email | 44 | 47 | 94% |
| time (not personal; masked only as ORG/any) | 0 | 42 | 0% |
| first_name | 23 | 29 | 79% |
| swift_bic_code | 21 | 22 | 95% |
| date_of_birth | 17 | 18 | 94% |
| api_key | 8 | 15 | 53% |
| local_latlng | 10 | 15 | 67% |
| last_name | 7 | 15 | 47% |
| credit_card_number | 13 | 15 | 87% |
| customer_id | 9 | 13 | 69% |
| bank_routing_number | 7 | 13 | 54% |
| iban | 12 | 13 | 92% |
| user_name | 4 | 12 | 33% |
| password | 4 | 11 | 36% |
| ssn | 8 | 11 | 73% |
| passport_number | 8 | 10 | 80% |
| ipv6 | 10 | 10 | 100% |
| account_pin | 4 | 9 | 44% |
| bban | 8 | 9 | 89% |
| date_time (not personal; masked only as ORG/any) | 0 | 9 | 0% |
| employee_id | 5 | 8 | 62% |
| ipv4 | 7 | 7 | 100% |
| driver_license_number | 2 | 7 | 29% |
| credit_card_security_code | 3 | 5 | 60% |
