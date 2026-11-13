# redactgate on Gretel synthetic_pii_finance_multilingual, dev (200 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **230/616 = 37.3%**
- Characters of personal data masked: 6349/12354 = 51.4%
- Documents with at least one labelled personal value left unmasked: 137/200 = 68.5%
- Masked characters inside a labelled span (precision lower bound): 73.1%
- Time: 37 s, 184 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 126 | 272 | 46% |
| company (not personal; masked only as ORG/any) | 113 | 219 | 52% |
| street_address | 26 | 171 | 15% |
| date (not personal; masked only as ORG/any) | 0 | 43 | 0% |
| phone_number | 4 | 28 | 14% |
| email | 15 | 19 | 79% |
| bank_routing_number | 2 | 18 | 11% |
| time (not personal; masked only as ORG/any) | 0 | 11 | 0% |
| first_name | 5 | 9 | 56% |
| swift_bic_code | 9 | 9 | 100% |
| employee_id | 0 | 9 | 0% |
| customer_id | 6 | 8 | 75% |
| last_name | 5 | 7 | 71% |
| date_of_birth | 0 | 7 | 0% |
| iban | 7 | 7 | 100% |
| bban | 1 | 6 | 17% |
| ipv6 | 6 | 6 | 100% |
| ipv4 | 6 | 6 | 100% |
| driver_license_number | 0 | 5 | 0% |
| ssn | 3 | 5 | 60% |
| local_latlng | 4 | 4 | 100% |
| user_name | 0 | 4 | 0% |
| credit_card_security_code | 0 | 4 | 0% |
| password | 0 | 3 | 0% |
| credit_card_number | 3 | 3 | 100% |
| account_pin | 1 | 2 | 50% |
| date_time (not personal; masked only as ORG/any) | 0 | 2 | 0% |
| api_key | 1 | 2 | 50% |
| passport_number | 0 | 2 | 0% |
