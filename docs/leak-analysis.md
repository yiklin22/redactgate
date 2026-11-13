# Why documents still leak (dev splits only)

Dev = first 500 English and first 200 German, French, Spanish, Italian and
Dutch documents of the train split. The test split was not looked at for any
of this.

Before the change, 553 of the 1,500 dev documents had at least one labelled
personal value left unmasked (110 of 500 English). Each missed value was put
in one group (a document can be in several):

| cause | English docs | all six, docs | all six, values |
|---|---|---|---|
| ID numbers, PINs, routing numbers etc. without a label word next to them (18 different label types; the largest, employee IDs, is 31 docs) | 38 | 233 | 304 |
| **address only partly matched or missed** | 22 | 180 | 227 |
| template placeholder labelled as data ("[Address]", "[Your Name]") | 12 | 80 | 173 |
| name not found at all (CSV cells, roles such as "supervisor", usernames) | 14 | 71 | 180 |
| name partly masked (first word missed) | 7 | 61 | 97 |
| **name tagged as an organisation by the NER model** | 26 | 55 | 109 |
| title ("Mr.", "Dr.") outside the mask; the name itself is masked | 5 | 14 | 22 |

Addresses were the largest single cause. Looking at them:

- Spanish and Italian street types missing from the pattern list ("Cuesta",
  "Pasadizo", "Callejón", "Cañada", "Rambla", "Incrocio", "Borgo",
  "Canale", "Stretto") and Dutch/Swedish suffixes ("-pad", "-baan",
  "-torget", "-gränd", "-stigen").
- "Roggestr. 5/5": the word boundary after "str." never matched.
- "Rue de l'Espoir": the article "l'" was not accepted.
- English postal addresses over several lines ("123 Main Street" /
  "Toronto, ON M5J 1K1" / "Canada"): only the street line was masked.

## Change 1 (kept): address patterns

Added those street types, fixed the "str." boundary and "l'", read on into
the city/postcode/country lines, and kept a US street name on one line.
A word ending in a street type ("Spring", "ring") now needs a house number
next to it (not a year), which it did not before.

| dev split | values masked, before -> after | docs with any leak | precision lower bound |
|---|---|---|---|
| English | 85.1% -> 86.9% | 22.0% -> 20.0% | 64.6% -> 65.5% |
| German | 68.4% -> 74.0% | 44.5% -> 38.0% | 61.1% -> 61.6% |
| French | 69.8% -> 74.5% | 43.0% -> 36.0% | 75.4% -> 74.9% |
| Spanish | 67.1% -> 71.3% | 48.0% -> 41.0% | 64.1% -> 64.6% |
| Italian | 71.0% -> 75.2% | 42.5% -> 37.5% | 74.1% -> 74.1% |
| Dutch | 65.6% -> 69.6% | 43.5% -> 38.0% | 58.9% -> 61.6% |

Leaking dev documents: 553 -> 481. Pattern matching costs 1.12 ms per
document instead of 1.03 ms.

## Change 2 (tried, not kept): names tagged as organisations

The model tags some full names as ORG ("Manon Legros", "TRACI V. LEE"),
and ORG is not masked. Relabelling a two- to four-word capitalised ORG with
no company word in it ("Inc", "Bank", "Société", "Gruppo", ...), no
possessive, no CamelCase and no short acronym as PERSON, on top of change 1:

| dev split | values masked | docs with any leak | precision lower bound |
|---|---|---|---|
| English | 86.9% -> 87.7% | 20.0% -> 18.2% | 65.5% -> 65.2% |
| German | 74.0% -> 74.8% | 38.0% -> 37.5% | 61.6% -> 60.2% |
| French | 74.5% -> 75.2% | 36.0% -> 35.0% | 74.9% -> 72.8% |
| Spanish | 71.3% -> 72.6% | 41.0% -> 41.0% | 64.6% -> 62.9% |
| Italian | 75.2% -> 76.1% | 37.5% -> 37.0% | 74.1% -> 73.4% |
| Dutch | 69.6% -> 70.9% | 38.0% -> 37.0% | 61.6% -> 59.0% |

It lowered the precision lower bound on every split (company names such as
"Virgin Galactic", "Horizon Éducation", "Charité Berlin", "Europäische Zentralbank" were masked as people),
so it was dropped. A list of first names, or a model that separates people
from companies better, would be needed.
