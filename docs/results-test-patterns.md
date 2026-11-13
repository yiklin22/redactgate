# redactgate on Gretel synthetic_pii_finance_multilingual, test (2891 documents, patterns only)

- Personal-data spans masked (>=80% of characters): **4516/8205 = 55.0%**
- Characters of personal data masked: 98944/156229 = 63.3%
- Documents with at least one labelled personal value left unmasked: 1677/2891 = 58.0%
- Masked characters inside a labelled span (precision lower bound): 65.1%
- Time: 2 s, 1 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 984 | 3489 | 28% |
| company (not personal; masked only as ORG/any) | 351 | 3476 | 10% |
| street_address | 1782 | 2194 | 81% |
| date (not personal; masked only as ORG/any) | 7 | 923 | 1% |
| phone_number | 411 | 480 | 86% |
| email | 308 | 330 | 93% |
| time (not personal; masked only as ORG/any) | 0 | 211 | 0% |
| first_name | 16 | 159 | 10% |
| date_of_birth | 95 | 126 | 75% |
| employee_id | 44 | 114 | 39% |
| swift_bic_code | 112 | 112 | 100% |
| customer_id | 38 | 94 | 40% |
| bban | 89 | 93 | 96% |
| ssn | 74 | 85 | 87% |
| credit_card_number | 77 | 83 | 93% |
| last_name | 14 | 82 | 17% |
| bank_routing_number | 33 | 81 | 41% |
| account_pin | 31 | 80 | 39% |
| credit_card_security_code | 41 | 76 | 54% |
| passport_number | 42 | 76 | 55% |
| iban | 67 | 69 | 97% |
| driver_license_number | 35 | 68 | 51% |
| ipv4 | 62 | 62 | 100% |
| ipv6 | 60 | 61 | 98% |
| local_latlng | 53 | 58 | 91% |
| api_key | 21 | 54 | 39% |
| password | 20 | 47 | 43% |
| date_time (not personal; masked only as ORG/any) | 0 | 38 | 0% |
| user_name | 7 | 32 | 22% |
