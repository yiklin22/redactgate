# redactgate on Gretel synthetic_pii_finance_multilingual, test (448 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **880/1315 = 66.9%**
- Characters of personal data masked: 18878/24702 = 76.4%
- Documents with at least one labelled personal value left unmasked: 211/448 = 47.1%
- Masked characters inside a labelled span (precision lower bound): 71.4%
- Time: 55 s, 123 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 412 | 576 | 72% |
| company (not personal; masked only as ORG/any) | 295 | 425 | 69% |
| street_address | 250 | 349 | 72% |
| date (not personal; masked only as ORG/any) | 0 | 114 | 0% |
| phone_number | 53 | 63 | 84% |
| date_of_birth | 31 | 46 | 67% |
| email | 35 | 38 | 92% |
| time (not personal; masked only as ORG/any) | 0 | 36 | 0% |
| first_name | 21 | 27 | 78% |
| customer_id | 1 | 20 | 5% |
| employee_id | 2 | 18 | 11% |
| iban | 13 | 17 | 76% |
| bank_routing_number | 3 | 17 | 18% |
| credit_card_number | 2 | 15 | 13% |
| swift_bic_code | 15 | 15 | 100% |
| passport_number | 4 | 13 | 31% |
| account_pin | 2 | 13 | 15% |
| driver_license_number | 1 | 12 | 8% |
| ssn | 1 | 11 | 9% |
| bban | 7 | 11 | 64% |
| last_name | 6 | 11 | 55% |
| credit_card_security_code | 1 | 11 | 9% |
| ipv4 | 9 | 9 | 100% |
| local_latlng | 4 | 6 | 67% |
| user_name | 0 | 5 | 0% |
| api_key | 2 | 5 | 40% |
| password | 2 | 4 | 50% |
| ipv6 | 3 | 3 | 100% |
| date_time (not personal; masked only as ORG/any) | 0 | 2 | 0% |
