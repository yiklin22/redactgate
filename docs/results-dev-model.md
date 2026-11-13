# redactgate on Gretel synthetic_pii_finance_multilingual, dev (500 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **1118/1409 = 79.3%**
- Characters of personal data masked: 23591/27553 = 85.6%
- Documents with at least one labelled personal value left unmasked: 161/500 = 32.2%
- Masked characters inside a labelled span (precision lower bound): 66.6%
- Time: 81 s, 161 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 470 | 621 | 76% |
| company (not personal; masked only as ORG/any) | 480 | 590 | 81% |
| street_address | 344 | 394 | 87% |
| date (not personal; masked only as ORG/any) | 2 | 168 | 1% |
| phone_number | 71 | 80 | 89% |
| email | 44 | 47 | 94% |
| time (not personal; masked only as ORG/any) | 0 | 42 | 0% |
| first_name | 18 | 29 | 62% |
| swift_bic_code | 21 | 22 | 95% |
| date_of_birth | 17 | 18 | 94% |
| api_key | 8 | 15 | 53% |
| local_latlng | 10 | 15 | 67% |
| last_name | 13 | 15 | 87% |
| credit_card_number | 13 | 15 | 87% |
| customer_id | 9 | 13 | 69% |
| bank_routing_number | 7 | 13 | 54% |
| iban | 12 | 13 | 92% |
| user_name | 2 | 12 | 17% |
| password | 4 | 11 | 36% |
| ssn | 8 | 11 | 73% |
| passport_number | 8 | 10 | 80% |
| ipv6 | 10 | 10 | 100% |
| account_pin | 4 | 9 | 44% |
| bban | 8 | 9 | 89% |
| date_time (not personal; masked only as ORG/any) | 0 | 9 | 0% |
| employee_id | 5 | 8 | 62% |
| ipv4 | 7 | 7 | 100% |
| driver_license_number | 2 | 7 | 29% |
| credit_card_security_code | 3 | 5 | 60% |
