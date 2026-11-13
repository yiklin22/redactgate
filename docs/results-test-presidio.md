# redactgate on Gretel synthetic_pii_finance_multilingual, test (2891 documents, Microsoft Presidio, default analyzer)

- Personal-data spans masked (>=80% of characters): **4322/8205 = 52.7%**
- Characters of personal data masked: 96790/156229 = 62.0%
- Documents with at least one labelled personal value left unmasked: 1862/2891 = 64.4%
- Masked characters inside a labelled span (precision lower bound): 29.1%
- Time: 79 s, 27 ms per document on CPU

| label | masked | total | rate |
|---|---|---|---|
| name | 2522 | 3489 | 72% |
| company (not personal; masked only as ORG/any) | 105 | 3476 | 3% |
| street_address | 255 | 2194 | 12% |
| date (not personal; masked only as ORG/any) | 858 | 923 | 93% |
| phone_number | 374 | 480 | 78% |
| email | 308 | 330 | 93% |
| time (not personal; masked only as ORG/any) | 149 | 211 | 71% |
| first_name | 105 | 159 | 66% |
| date_of_birth | 113 | 126 | 90% |
| employee_id | 46 | 114 | 40% |
| swift_bic_code | 3 | 112 | 3% |
| customer_id | 15 | 94 | 16% |
| bban | 4 | 93 | 4% |
| ssn | 69 | 85 | 81% |
| credit_card_number | 49 | 83 | 59% |
| last_name | 22 | 82 | 27% |
| bank_routing_number | 77 | 81 | 95% |
| account_pin | 48 | 80 | 60% |
| credit_card_security_code | 4 | 76 | 5% |
| passport_number | 75 | 76 | 99% |
| iban | 67 | 69 | 97% |
| driver_license_number | 33 | 68 | 49% |
| ipv4 | 62 | 62 | 100% |
| ipv6 | 60 | 61 | 98% |
| local_latlng | 2 | 58 | 3% |
| api_key | 1 | 54 | 2% |
| password | 0 | 47 | 0% |
| date_time (not personal; masked only as ORG/any) | 18 | 38 | 47% |
| user_name | 8 | 32 | 25% |
