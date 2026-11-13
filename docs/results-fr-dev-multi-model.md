# redactgate on Gretel synthetic_pii_finance_multilingual, dev (200 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **457/616 = 74.2%**
- Characters of personal data masked: 10473/12354 = 84.8%
- Documents with at least one labelled personal value left unmasked: 73/200 = 36.5%
- Masked characters inside a labelled span (precision lower bound): 74.9%
- Time: 29 s, 145 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 189 | 272 | 69% |
| company (not personal; masked only as ORG/any) | 151 | 219 | 69% |
| street_address | 153 | 171 | 89% |
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
| user_name | 2 | 4 | 50% |
| credit_card_security_code | 0 | 4 | 0% |
| password | 3 | 3 | 100% |
| credit_card_number | 3 | 3 | 100% |
| account_pin | 1 | 2 | 50% |
| date_time (not personal; masked only as ORG/any) | 0 | 2 | 0% |
| api_key | 2 | 2 | 100% |
| passport_number | 0 | 2 | 0% |
