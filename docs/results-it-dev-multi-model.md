# redactgate on Gretel synthetic_pii_finance_multilingual, dev (200 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **424/565 = 75.0%**
- Characters of personal data masked: 9480/11567 = 82.0%
- Documents with at least one labelled personal value left unmasked: 76/200 = 38.0%
- Masked characters inside a labelled span (precision lower bound): 74.1%
- Time: 36 s, 181 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 162 | 227 | 71% |
| company (not personal; masked only as ORG/any) | 160 | 213 | 75% |
| street_address | 140 | 171 | 82% |
| date (not personal; masked only as ORG/any) | 0 | 42 | 0% |
| phone_number | 32 | 36 | 89% |
| email | 27 | 28 | 96% |
| time (not personal; masked only as ORG/any) | 0 | 18 | 0% |
| date_of_birth | 9 | 14 | 64% |
| swift_bic_code | 10 | 10 | 100% |
| customer_id | 2 | 9 | 22% |
| ipv4 | 8 | 8 | 100% |
| iban | 8 | 8 | 100% |
| first_name | 5 | 7 | 71% |
| bank_routing_number | 2 | 5 | 40% |
| passport_number | 0 | 5 | 0% |
| bban | 4 | 5 | 80% |
| employee_id | 0 | 5 | 0% |
| last_name | 4 | 4 | 100% |
| password | 4 | 4 | 100% |
| user_name | 0 | 4 | 0% |
| credit_card_security_code | 0 | 3 | 0% |
| local_latlng | 2 | 3 | 67% |
| date_time (not personal; masked only as ORG/any) | 0 | 2 | 0% |
| account_pin | 0 | 2 | 0% |
| ssn | 1 | 2 | 50% |
| ipv6 | 2 | 2 | 100% |
| api_key | 1 | 1 | 100% |
| driver_license_number | 0 | 1 | 0% |
| credit_card_number | 1 | 1 | 100% |
