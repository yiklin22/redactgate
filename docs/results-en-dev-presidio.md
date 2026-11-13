# redactgate on Gretel synthetic_pii_finance_multilingual, dev (500 documents, Microsoft Presidio, default analyzer)

- Personal-data spans masked (>=80% of characters): **742/1409 = 52.7%**
- Characters of personal data masked: 16851/27553 = 61.2%
- Documents with at least one labelled personal value left unmasked: 321/500 = 64.2%
- Masked characters inside a labelled span (precision lower bound): 27.0%
- Time: 14 s, 29 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 449 | 621 | 72% |
| company (not personal; masked only as ORG/any) | 20 | 590 | 3% |
| street_address | 62 | 394 | 16% |
| date (not personal; masked only as ORG/any) | 153 | 168 | 91% |
| phone_number | 55 | 80 | 69% |
| email | 43 | 47 | 91% |
| time (not personal; masked only as ORG/any) | 25 | 42 | 60% |
| first_name | 21 | 29 | 72% |
| swift_bic_code | 1 | 22 | 5% |
| date_of_birth | 18 | 18 | 100% |
| api_key | 1 | 15 | 7% |
| local_latlng | 2 | 15 | 13% |
| last_name | 9 | 15 | 60% |
| credit_card_number | 6 | 15 | 40% |
| customer_id | 5 | 13 | 38% |
| bank_routing_number | 13 | 13 | 100% |
| iban | 12 | 13 | 92% |
| user_name | 3 | 12 | 25% |
| password | 0 | 11 | 0% |
| ssn | 5 | 11 | 45% |
| passport_number | 10 | 10 | 100% |
| ipv6 | 10 | 10 | 100% |
| account_pin | 6 | 9 | 67% |
| bban | 0 | 9 | 0% |
| date_time (not personal; masked only as ORG/any) | 3 | 9 | 33% |
| employee_id | 0 | 8 | 0% |
| ipv4 | 7 | 7 | 100% |
| driver_license_number | 4 | 7 | 57% |
| credit_card_security_code | 0 | 5 | 0% |
