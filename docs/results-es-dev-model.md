# redactgate on Gretel synthetic_pii_finance_multilingual, dev (200 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **300/654 = 45.9%**
- Characters of personal data masked: 6353/11940 = 53.2%
- Documents with at least one labelled personal value left unmasked: 143/200 = 71.5%
- Masked characters inside a labelled span (precision lower bound): 59.3%
- Time: 38 s, 191 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 194 | 329 | 59% |
| company (not personal; masked only as ORG/any) | 109 | 179 | 61% |
| street_address | 17 | 167 | 10% |
| date (not personal; masked only as ORG/any) | 0 | 52 | 0% |
| phone_number | 30 | 37 | 81% |
| time (not personal; masked only as ORG/any) | 0 | 29 | 0% |
| email | 17 | 17 | 100% |
| customer_id | 0 | 13 | 0% |
| driver_license_number | 2 | 10 | 20% |
| account_pin | 0 | 8 | 0% |
| swift_bic_code | 7 | 7 | 100% |
| date_of_birth | 1 | 7 | 14% |
| credit_card_security_code | 0 | 7 | 0% |
| first_name | 5 | 7 | 71% |
| employee_id | 0 | 6 | 0% |
| ipv4 | 5 | 5 | 100% |
| bank_routing_number | 2 | 5 | 40% |
| bban | 4 | 4 | 100% |
| iban | 3 | 4 | 75% |
| date_time (not personal; masked only as ORG/any) | 0 | 3 | 0% |
| credit_card_number | 3 | 3 | 100% |
| ssn | 1 | 3 | 33% |
| last_name | 2 | 3 | 67% |
| user_name | 2 | 3 | 67% |
| api_key | 1 | 3 | 33% |
| local_latlng | 2 | 2 | 100% |
| passport_number | 0 | 2 | 0% |
| ipv6 | 2 | 2 | 100% |
