# redactgate on Gretel synthetic_pii_finance_multilingual, dev (200 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **229/516 = 44.4%**
- Characters of personal data masked: 5682/9998 = 56.8%
- Documents with at least one labelled personal value left unmasked: 129/200 = 64.5%
- Masked characters inside a labelled span (precision lower bound): 53.2%
- Time: 36 s, 180 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 150 | 241 | 62% |
| company (not personal; masked only as ORG/any) | 131 | 199 | 66% |
| street_address | 21 | 131 | 16% |
| date (not personal; masked only as ORG/any) | 0 | 49 | 0% |
| iban | 15 | 22 | 68% |
| phone_number | 3 | 18 | 17% |
| time (not personal; masked only as ORG/any) | 0 | 17 | 0% |
| email | 8 | 11 | 73% |
| employee_id | 2 | 11 | 18% |
| driver_license_number | 2 | 9 | 22% |
| bank_routing_number | 0 | 7 | 0% |
| ipv4 | 7 | 7 | 100% |
| passport_number | 0 | 7 | 0% |
| date_time (not personal; masked only as ORG/any) | 0 | 6 | 0% |
| ipv6 | 5 | 5 | 100% |
| customer_id | 2 | 4 | 50% |
| password | 3 | 4 | 75% |
| swift_bic_code | 4 | 4 | 100% |
| last_name | 1 | 4 | 25% |
| account_pin | 1 | 4 | 25% |
| credit_card_security_code | 0 | 4 | 0% |
| ssn | 0 | 4 | 0% |
| date_of_birth | 0 | 4 | 0% |
| bban | 2 | 3 | 67% |
| local_latlng | 1 | 3 | 33% |
| api_key | 1 | 3 | 33% |
| credit_card_number | 0 | 3 | 0% |
| user_name | 0 | 2 | 0% |
| first_name | 1 | 1 | 100% |
