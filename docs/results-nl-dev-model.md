# redactgate on Gretel synthetic_pii_finance_multilingual, dev (200 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **209/506 = 41.3%**
- Characters of personal data masked: 4647/9178 = 50.6%
- Documents with at least one labelled personal value left unmasked: 123/200 = 61.5%
- Masked characters inside a labelled span (precision lower bound): 52.6%
- Time: 35 s, 174 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 115 | 224 | 51% |
| company (not personal; masked only as ORG/any) | 92 | 199 | 46% |
| street_address | 14 | 119 | 12% |
| date (not personal; masked only as ORG/any) | 0 | 30 | 0% |
| email | 26 | 29 | 90% |
| phone_number | 8 | 24 | 33% |
| time (not personal; masked only as ORG/any) | 0 | 17 | 0% |
| bban | 7 | 10 | 70% |
| ssn | 0 | 8 | 0% |
| first_name | 3 | 8 | 38% |
| customer_id | 0 | 8 | 0% |
| employee_id | 0 | 7 | 0% |
| account_pin | 5 | 7 | 71% |
| ipv4 | 6 | 6 | 100% |
| driver_license_number | 0 | 6 | 0% |
| credit_card_number | 5 | 6 | 83% |
| swift_bic_code | 6 | 6 | 100% |
| local_latlng | 3 | 5 | 60% |
| api_key | 1 | 5 | 20% |
| iban | 3 | 5 | 60% |
| user_name | 0 | 4 | 0% |
| last_name | 1 | 4 | 25% |
| passport_number | 2 | 3 | 67% |
| bank_routing_number | 0 | 3 | 0% |
| password | 1 | 3 | 33% |
| date_of_birth | 1 | 2 | 50% |
| credit_card_security_code | 0 | 2 | 0% |
| ipv6 | 2 | 2 | 100% |
| date_time (not personal; masked only as ORG/any) | 0 | 1 | 0% |
