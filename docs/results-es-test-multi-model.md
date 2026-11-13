# redactgate on Gretel synthetic_pii_finance_multilingual, test (461 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **1026/1353 = 75.8%**
- Characters of personal data masked: 20484/25085 = 81.7%
- Documents with at least one labelled personal value left unmasked: 161/461 = 34.9%
- Masked characters inside a labelled span (precision lower bound): 67.6%
- Time: 60 s, 129 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 453 | 591 | 77% |
| company (not personal; masked only as ORG/any) | 311 | 424 | 73% |
| street_address | 295 | 343 | 86% |
| date (not personal; masked only as ORG/any) | 1 | 121 | 1% |
| phone_number | 98 | 103 | 95% |
| time (not personal; masked only as ORG/any) | 0 | 68 | 0% |
| email | 64 | 68 | 94% |
| swift_bic_code | 23 | 24 | 96% |
| date_of_birth | 9 | 23 | 39% |
| customer_id | 2 | 23 | 9% |
| iban | 15 | 19 | 79% |
| employee_id | 2 | 19 | 11% |
| first_name | 13 | 16 | 81% |
| last_name | 6 | 16 | 38% |
| ssn | 5 | 15 | 33% |
| ipv6 | 12 | 12 | 100% |
| passport_number | 0 | 12 | 0% |
| ipv4 | 10 | 11 | 91% |
| driver_license_number | 2 | 11 | 18% |
| credit_card_security_code | 2 | 9 | 22% |
| password | 2 | 9 | 22% |
| credit_card_number | 3 | 8 | 38% |
| date_time (not personal; masked only as ORG/any) | 0 | 6 | 0% |
| bban | 4 | 5 | 80% |
| bank_routing_number | 0 | 5 | 0% |
| api_key | 4 | 4 | 100% |
| user_name | 1 | 4 | 25% |
| account_pin | 0 | 2 | 0% |
| local_latlng | 1 | 1 | 100% |
