# redactgate on Gretel synthetic_pii_finance_multilingual, test (453 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **839/1152 = 72.8%**
- Characters of personal data masked: 17273/21093 = 81.9%
- Documents with at least one labelled personal value left unmasked: 170/453 = 37.5%
- Masked characters inside a labelled span (precision lower bound): 64.0%
- Time: 56 s, 123 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 398 | 530 | 75% |
| company (not personal; masked only as ORG/any) | 367 | 436 | 84% |
| street_address | 243 | 282 | 86% |
| date (not personal; masked only as ORG/any) | 0 | 118 | 0% |
| phone_number | 21 | 49 | 43% |
| time (not personal; masked only as ORG/any) | 0 | 36 | 0% |
| email | 30 | 33 | 91% |
| employee_id | 5 | 24 | 21% |
| customer_id | 3 | 23 | 13% |
| swift_bic_code | 22 | 22 | 100% |
| iban | 16 | 19 | 84% |
| last_name | 15 | 19 | 79% |
| bban | 13 | 17 | 76% |
| date_of_birth | 15 | 17 | 88% |
| first_name | 15 | 16 | 94% |
| bank_routing_number | 1 | 15 | 7% |
| passport_number | 3 | 12 | 25% |
| account_pin | 3 | 9 | 33% |
| driver_license_number | 0 | 9 | 0% |
| ssn | 1 | 9 | 11% |
| ipv6 | 8 | 8 | 100% |
| api_key | 8 | 8 | 100% |
| ipv4 | 7 | 7 | 100% |
| user_name | 2 | 6 | 33% |
| password | 2 | 5 | 40% |
| credit_card_number | 3 | 5 | 60% |
| local_latlng | 4 | 5 | 80% |
| credit_card_security_code | 1 | 3 | 33% |
| date_time (not personal; masked only as ORG/any) | 0 | 2 | 0% |
