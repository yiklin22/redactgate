# redactgate on Gretel synthetic_pii_finance_multilingual, dev (200 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **435/654 = 66.5%**
- Characters of personal data masked: 8761/11940 = 73.4%
- Documents with at least one labelled personal value left unmasked: 98/200 = 49.0%
- Masked characters inside a labelled span (precision lower bound): 64.5%
- Time: 27 s, 136 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 222 | 329 | 67% |
| company (not personal; masked only as ORG/any) | 138 | 179 | 77% |
| street_address | 112 | 167 | 67% |
| date (not personal; masked only as ORG/any) | 0 | 52 | 0% |
| phone_number | 36 | 37 | 97% |
| time (not personal; masked only as ORG/any) | 0 | 29 | 0% |
| email | 17 | 17 | 100% |
| customer_id | 0 | 13 | 0% |
| driver_license_number | 2 | 10 | 20% |
| account_pin | 0 | 8 | 0% |
| swift_bic_code | 7 | 7 | 100% |
| date_of_birth | 5 | 7 | 71% |
| credit_card_security_code | 0 | 7 | 0% |
| first_name | 5 | 7 | 71% |
| employee_id | 0 | 6 | 0% |
| ipv4 | 5 | 5 | 100% |
| bank_routing_number | 2 | 5 | 40% |
| bban | 4 | 4 | 100% |
| iban | 4 | 4 | 100% |
| date_time (not personal; masked only as ORG/any) | 0 | 3 | 0% |
| credit_card_number | 3 | 3 | 100% |
| ssn | 1 | 3 | 33% |
| last_name | 3 | 3 | 100% |
| user_name | 2 | 3 | 67% |
| api_key | 1 | 3 | 33% |
| local_latlng | 2 | 2 | 100% |
| passport_number | 0 | 2 | 0% |
| ipv6 | 2 | 2 | 100% |
