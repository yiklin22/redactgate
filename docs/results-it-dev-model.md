# redactgate on Gretel synthetic_pii_finance_multilingual, dev (200 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **221/565 = 39.1%**
- Characters of personal data masked: 5653/11567 = 48.9%
- Documents with at least one labelled personal value left unmasked: 135/200 = 67.5%
- Masked characters inside a labelled span (precision lower bound): 62.4%
- Time: 36 s, 181 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 126 | 227 | 56% |
| company (not personal; masked only as ORG/any) | 77 | 213 | 36% |
| street_address | 26 | 171 | 15% |
| date (not personal; masked only as ORG/any) | 0 | 42 | 0% |
| phone_number | 3 | 36 | 8% |
| email | 27 | 28 | 96% |
| time (not personal; masked only as ORG/any) | 0 | 18 | 0% |
| date_of_birth | 0 | 14 | 0% |
| swift_bic_code | 10 | 10 | 100% |
| customer_id | 2 | 9 | 22% |
| ipv4 | 8 | 8 | 100% |
| iban | 3 | 8 | 38% |
| first_name | 2 | 7 | 29% |
| bank_routing_number | 0 | 5 | 0% |
| passport_number | 0 | 5 | 0% |
| bban | 4 | 5 | 80% |
| employee_id | 0 | 5 | 0% |
| last_name | 1 | 4 | 25% |
| password | 2 | 4 | 50% |
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
