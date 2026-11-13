# redactgate on Gretel synthetic_pii_finance_multilingual, dev (200 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **353/516 = 68.4%**
- Characters of personal data masked: 7876/9998 = 78.8%
- Documents with at least one labelled personal value left unmasked: 89/200 = 44.5%
- Masked characters inside a labelled span (precision lower bound): 61.1%
- Time: 25 s, 126 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 180 | 241 | 75% |
| company (not personal; masked only as ORG/any) | 132 | 199 | 66% |
| street_address | 91 | 131 | 69% |
| date (not personal; masked only as ORG/any) | 0 | 49 | 0% |
| iban | 21 | 22 | 95% |
| phone_number | 14 | 18 | 78% |
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
| password | 4 | 4 | 100% |
| swift_bic_code | 4 | 4 | 100% |
| last_name | 1 | 4 | 25% |
| account_pin | 1 | 4 | 25% |
| credit_card_security_code | 0 | 4 | 0% |
| ssn | 0 | 4 | 0% |
| date_of_birth | 3 | 4 | 75% |
| bban | 2 | 3 | 67% |
| local_latlng | 1 | 3 | 33% |
| api_key | 3 | 3 | 100% |
| credit_card_number | 0 | 3 | 0% |
| user_name | 1 | 2 | 50% |
| first_name | 1 | 1 | 100% |
