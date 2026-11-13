# redactgate on Gretel synthetic_pii_finance_multilingual, dev (200 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **420/616 = 68.2%**
- Characters of personal data masked: 9835/12354 = 79.6%
- Documents with at least one labelled personal value left unmasked: 92/200 = 46.0%
- Masked characters inside a labelled span (precision lower bound): 74.5%
- Time: 28 s, 140 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 189 | 272 | 69% |
| company (not personal; masked only as ORG/any) | 153 | 219 | 70% |
| street_address | 121 | 171 | 71% |
| date (not personal; masked only as ORG/any) | 0 | 43 | 0% |
| phone_number | 25 | 28 | 89% |
| email | 15 | 19 | 79% |
| bank_routing_number | 2 | 18 | 11% |
| time (not personal; masked only as ORG/any) | 0 | 11 | 0% |
| first_name | 8 | 9 | 89% |
| swift_bic_code | 9 | 9 | 100% |
| employee_id | 0 | 9 | 0% |
| customer_id | 6 | 8 | 75% |
| last_name | 6 | 7 | 86% |
| date_of_birth | 6 | 7 | 86% |
| iban | 7 | 7 | 100% |
| bban | 1 | 6 | 17% |
| ipv6 | 6 | 6 | 100% |
| ipv4 | 6 | 6 | 100% |
| driver_license_number | 0 | 5 | 0% |
| ssn | 3 | 5 | 60% |
| local_latlng | 4 | 4 | 100% |
| user_name | 1 | 4 | 25% |
| credit_card_security_code | 0 | 4 | 0% |
| password | 0 | 3 | 0% |
| credit_card_number | 3 | 3 | 100% |
| account_pin | 1 | 2 | 50% |
| date_time (not personal; masked only as ORG/any) | 0 | 2 | 0% |
| api_key | 1 | 2 | 50% |
| passport_number | 0 | 2 | 0% |
