# redactgate on Gretel synthetic_pii_finance_multilingual, test (2891 documents, patterns + NER model)

- Personal-data spans masked (>=80% of characters): **6715/8205 = 81.8%**
- Characters of personal data masked: 136258/156229 = 87.2%
- Documents with at least one labelled personal value left unmasked: 808/2891 = 27.9%
- Masked characters inside a labelled span (precision lower bound): 64.7%
- Time: 400 s, 138 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 2863 | 3489 | 82% |
| company (not personal; masked only as ORG/any) | 2988 | 3476 | 86% |
| street_address | 1933 | 2194 | 88% |
| date (not personal; masked only as ORG/any) | 7 | 923 | 1% |
| phone_number | 438 | 480 | 91% |
| email | 308 | 330 | 93% |
| time (not personal; masked only as ORG/any) | 0 | 211 | 0% |
| first_name | 128 | 159 | 81% |
| date_of_birth | 95 | 126 | 75% |
| employee_id | 44 | 114 | 39% |
| swift_bic_code | 112 | 112 | 100% |
| customer_id | 39 | 94 | 41% |
| bban | 89 | 93 | 96% |
| ssn | 74 | 85 | 87% |
| credit_card_number | 77 | 83 | 93% |
| last_name | 32 | 82 | 39% |
| bank_routing_number | 35 | 81 | 43% |
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
| user_name | 16 | 32 | 50% |
