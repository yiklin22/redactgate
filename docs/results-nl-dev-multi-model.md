# redactgate on Gretel synthetic_pii_finance_multilingual, dev (200 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **350/506 = 69.2%**
- Characters of personal data masked: 7314/9178 = 79.7%
- Documents with at least one labelled personal value left unmasked: 78/200 = 39.0%
- Masked characters inside a labelled span (precision lower bound): 61.6%
- Time: 38 s, 191 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 162 | 224 | 72% |
| company (not personal; masked only as ORG/any) | 143 | 199 | 72% |
| street_address | 90 | 119 | 76% |
| date (not personal; masked only as ORG/any) | 0 | 30 | 0% |
| email | 26 | 29 | 90% |
| phone_number | 13 | 24 | 54% |
| time (not personal; masked only as ORG/any) | 0 | 17 | 0% |
| bban | 7 | 10 | 70% |
| ssn | 0 | 8 | 0% |
| first_name | 7 | 8 | 88% |
| customer_id | 0 | 8 | 0% |
| employee_id | 0 | 7 | 0% |
| account_pin | 5 | 7 | 71% |
| ipv4 | 6 | 6 | 100% |
| driver_license_number | 0 | 6 | 0% |
| credit_card_number | 5 | 6 | 83% |
| swift_bic_code | 6 | 6 | 100% |
| local_latlng | 3 | 5 | 60% |
| api_key | 4 | 5 | 80% |
| iban | 5 | 5 | 100% |
| user_name | 0 | 4 | 0% |
| last_name | 4 | 4 | 100% |
| passport_number | 2 | 3 | 67% |
| bank_routing_number | 0 | 3 | 0% |
| password | 1 | 3 | 33% |
| date_of_birth | 2 | 2 | 100% |
| credit_card_security_code | 0 | 2 | 0% |
| ipv6 | 2 | 2 | 100% |
| date_time (not personal; masked only as ORG/any) | 0 | 1 | 0% |
