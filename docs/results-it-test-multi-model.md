# redactgate on Gretel synthetic_pii_finance_multilingual, test (448 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **894/1315 = 68.0%**
- Characters of personal data masked: 19247/24702 = 77.9%
- Documents with at least one labelled personal value left unmasked: 204/448 = 45.5%
- Masked characters inside a labelled span (precision lower bound): 69.8%
- Time: 55 s, 123 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 412 | 576 | 72% |
| company (not personal; masked only as ORG/any) | 295 | 425 | 69% |
| street_address | 252 | 349 | 72% |
| date (not personal; masked only as ORG/any) | 0 | 114 | 0% |
| phone_number | 53 | 63 | 84% |
| date_of_birth | 31 | 46 | 67% |
| email | 35 | 38 | 92% |
| time (not personal; masked only as ORG/any) | 0 | 36 | 0% |
| first_name | 21 | 27 | 78% |
| customer_id | 2 | 20 | 10% |
| employee_id | 4 | 18 | 22% |
| iban | 13 | 17 | 76% |
| bank_routing_number | 5 | 17 | 29% |
| credit_card_number | 2 | 15 | 13% |
| swift_bic_code | 15 | 15 | 100% |
| passport_number | 4 | 13 | 31% |
| account_pin | 6 | 13 | 46% |
| driver_license_number | 1 | 12 | 8% |
| ssn | 1 | 11 | 9% |
| bban | 7 | 11 | 64% |
| last_name | 6 | 11 | 55% |
| credit_card_security_code | 1 | 11 | 9% |
| ipv4 | 9 | 9 | 100% |
| local_latlng | 4 | 6 | 67% |
| user_name | 0 | 5 | 0% |
| api_key | 5 | 5 | 100% |
| password | 2 | 4 | 50% |
| ipv6 | 3 | 3 | 100% |
| date_time (not personal; masked only as ORG/any) | 0 | 2 | 0% |
