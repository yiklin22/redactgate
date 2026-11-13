# redactgate on Gretel synthetic_pii_finance_multilingual, test (445 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **807/1236 = 65.3%**
- Characters of personal data masked: 16770/22473 = 74.6%
- Documents with at least one labelled personal value left unmasked: 207/445 = 46.5%
- Masked characters inside a labelled span (precision lower bound): 61.7%
- Time: 54 s, 122 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 417 | 599 | 70% |
| company (not personal; masked only as ORG/any) | 441 | 561 | 79% |
| street_address | 181 | 284 | 64% |
| date (not personal; masked only as ORG/any) | 0 | 92 | 0% |
| phone_number | 29 | 66 | 44% |
| time (not personal; masked only as ORG/any) | 0 | 51 | 0% |
| email | 30 | 33 | 91% |
| iban | 27 | 28 | 96% |
| first_name | 24 | 25 | 96% |
| swift_bic_code | 18 | 18 | 100% |
| customer_id | 1 | 17 | 6% |
| driver_license_number | 0 | 16 | 0% |
| ipv4 | 16 | 16 | 100% |
| ipv6 | 14 | 15 | 93% |
| credit_card_number | 9 | 13 | 69% |
| password | 4 | 11 | 36% |
| bank_routing_number | 1 | 11 | 9% |
| account_pin | 6 | 10 | 60% |
| passport_number | 1 | 9 | 11% |
| bban | 7 | 9 | 78% |
| last_name | 3 | 9 | 33% |
| credit_card_security_code | 4 | 8 | 50% |
| user_name | 1 | 8 | 12% |
| employee_id | 1 | 8 | 12% |
| date_time (not personal; masked only as ORG/any) | 0 | 8 | 0% |
| local_latlng | 6 | 7 | 86% |
| date_of_birth | 5 | 7 | 71% |
| ssn | 1 | 6 | 17% |
| api_key | 1 | 3 | 33% |
