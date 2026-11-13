# redactgate on Gretel synthetic_pii_finance_multilingual, test (2891 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **6900/8205 = 84.1%**
- Characters of personal data masked: 139620/156229 = 89.4%
- Documents with at least one labelled personal value left unmasked: 693/2891 = 24.0%
- Masked characters inside a labelled span (precision lower bound): 65.1%
- Time: 675 s, 233 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 2864 | 3489 | 82% |
| company (not personal; masked only as ORG/any) | 2988 | 3476 | 86% |
| street_address | 2024 | 2194 | 92% |
| date (not personal; masked only as ORG/any) | 7 | 923 | 1% |
| phone_number | 438 | 480 | 91% |
| email | 308 | 330 | 93% |
| time (not personal; masked only as ORG/any) | 0 | 211 | 0% |
| first_name | 128 | 159 | 81% |
| date_of_birth | 95 | 126 | 75% |
| employee_id | 59 | 114 | 52% |
| swift_bic_code | 112 | 112 | 100% |
| customer_id | 49 | 94 | 52% |
| bban | 89 | 93 | 96% |
| ssn | 74 | 85 | 87% |
| credit_card_number | 77 | 83 | 93% |
| last_name | 32 | 82 | 39% |
| bank_routing_number | 53 | 81 | 65% |
| account_pin | 41 | 80 | 51% |
| credit_card_security_code | 41 | 76 | 54% |
| passport_number | 43 | 76 | 57% |
| iban | 67 | 69 | 97% |
| driver_license_number | 35 | 68 | 51% |
| ipv4 | 62 | 62 | 100% |
| ipv6 | 60 | 61 | 98% |
| local_latlng | 53 | 58 | 91% |
| api_key | 49 | 54 | 91% |
| password | 30 | 47 | 64% |
| date_time (not personal; masked only as ORG/any) | 0 | 38 | 0% |
| user_name | 17 | 32 | 53% |
