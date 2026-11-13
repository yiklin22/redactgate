from redactgate.detect import detect, find_patterns
from redactgate.redact import redact, restore

TEXT = ("Please wire $4,500 to Maria Gonzalez (maria.g@example.com, +1 (415) 555-0132) at "
        "441 Julie Squares, South Karen. Card 4111 1111 1111 1111, CVV: 737. "
        "IBAN GB82 WEST 1234 5698 7654 32, routing number 021000021, SWIFT: DEUTDEFF. "
        "Passport No. X12345678. Password: hunter22! DOB: 04/12/1985. Server 192.168.1.20. "
        "Meeting at 12:30:45 on 2023-10-15. Dear Ms. Gonzalez, thank you.")


def labels(text):
    return {(s.label, text[s.start:s.end]) for s in detect(text, use_model=False)}


def test_patterns_find_each_kind():
    found = labels(TEXT)
    for item in [("EMAIL", "maria.g@example.com"), ("PHONE", "+1 (415) 555-0132"), ("CARD", "4111 1111 1111 1111"),
                 ("CVV", "737"), ("IBAN", "GB82 WEST 1234 5698 7654 32"), ("ROUTING", "021000021"),
                 ("SWIFT", "DEUTDEFF"), ("ID", "X12345678"), ("SECRET", "hunter22!"), ("DOB", "04/12/1985"),
                 ("IP", "192.168.1.20"), ("ADDRESS", "441 Julie Squares, South Karen"), ("PERSON", "Gonzalez")]:
        assert item in found, item


def test_times_dates_and_amounts_are_left_alone():
    masked = {v for _, v in labels(TEXT)}
    assert not any(x in v for v in masked for x in ("12:30:45", "2023-10-15", "4,500"))


def test_validators_reject_lookalikes():
    kinds = {s.label for s in find_patterns("Order 4111 1111 1111 1112 and ref GB82 WEST 1234 5698 7654 33.")}
    assert "CARD" not in kinds and "IBAN" not in kinds


def test_same_value_same_placeholder_and_restore():
    text = "Contact Ms. Ana Lima at ana@lima.pt. Ana Lima will sign. Write to ana@lima.pt."
    red, mapping = redact(text, use_model=False)
    assert "ana@lima.pt" not in red and "Ana Lima" not in red
    assert red.count("[EMAIL_1]") == 2 and red.count("[PERSON_1]") == 2
    assert restore("Reply sent to [PERSON_1] at [EMAIL_1]; [PERSON_9] unknown.", mapping) == \
        "Reply sent to Ana Lima at ana@lima.pt; [PERSON_9] unknown."


def test_password_like_tokens_but_not_message_syntax():
    kinds = labels("Use the code k8P*X^qbXnmihh!4^Y to log in. Field :73:/Bank/9876543210/DEF follows.")
    assert ("SECRET", "k8P*X^qbXnmihh!4^Y") in kinds
    assert not any(v.startswith(":73:") for _, v in kinds)


def test_address_pieces_join():
    t = "Bitte an Schnellstraße 12, 45678 Berlin senden."
    red, _ = redact(t, use_model=False)
    assert red == "Bitte an [ADDRESS_1] senden."


def test_surname_points_to_the_full_name_and_bare_placeholders_restore():
    text = "Refund Ms. Ana Lima for order 5531. Dear Ms. Lima, sorry. Ana Lima can call us."
    red, mapping = redact(text, use_model=False)
    assert red.count("[PERSON_1]") == 2 and "[PERSON_1_LAST]" in red
    assert restore("Dear Ms. PERSON_1_LAST, we refunded [PERSON_1].", mapping) == "Dear Ms. Lima, we refunded Ana Lima."


def test_keyed_secrets_and_ids():
    found = labels("APIKey: dE216e301cc66D901cbfAeBFF10e1FbD. The new password will be: Rqe9zC)mbj+72EECE) "
                   "User Name: thart. Employee ID: Jp-58502. The account pin is 598145. "
                   "Bank Routing Number (for direct deposit): 336648287.")
    for item in [("SECRET", "dE216e301cc66D901cbfAeBFF10e1FbD"), ("SECRET", "Rqe9zC)mbj+72EECE)"), ("ID", "thart"),
                 ("ID", "Jp-58502"), ("SECRET", "598145"), ("ROUTING", "336648287")]:
        assert item in found, item
    # CamelCase field names and ordinary words after "user" are left alone.
    assert labels("<StatementBeginBalance>1200</StatementBeginBalance> The user workstation was updated.") == set()


def test_more_street_forms_and_multiline_addresses():
    found = labels("Ship to 25 Old Street\n  London, EC4A 3EG\n  UK\n\nThen Roggestr. 5/5, 20095 Hamburg; "
                   "7 Cuesta Rico Agudo, Las Palmas and 12 Rue de l'Espoir, 75010 Paris. Atelier: Skogstorget 608.")
    for item in [("ADDRESS", "25 Old Street\n  London, EC4A 3EG\n  UK"), ("ADDRESS", "Roggestr. 5/5, 20095 Hamburg"),
                 ("ADDRESS", "7 Cuesta Rico Agudo, Las Palmas"), ("ADDRESS", "12 Rue de l'Espoir, 75010 Paris"),
                 ("ADDRESS", "Skogstorget 608")]:
        assert item in found, item
    # A word that merely ends in a street type, with no house number, is not an address.
    assert labels("In Spring we reviewed the Boxing ring budget. Spring 2023 was good.") == set()


def test_address_patterns_leave_ordinary_text_alone():
    # Street-type words after a heading or count, and words ending in "pad".
    assert labels("Version 2 Canale Today. Section 4 Borgo Notes. Launchpad 3 is live. Needs 3 Vial Samples.") == set()
    # The line after a street is only taken when it looks like a city/postcode line.
    for text, address in [("Invoice: 10 Oak Street\nTotal, Tax, Net\nThanks", "10 Oak Street"),
                          ("Pay 12 Main Street\nThanks, Anna", "12 Main Street"),
                          ("Pay 12 Main Street\nThanks, JD", "12 Main Street"),
                          ("Ship to 123 Main Street\nAnytown, CA 12345\nThank you", "123 Main Street\nAnytown, CA 12345"),
                          ("Ship to 1 Main Street\nVienna, Austria\n\nThanks", "1 Main Street\nVienna, Austria")]:
        assert {v for k, v in labels(text) if k == "ADDRESS"} == {address}, text


def test_name_before_a_house_number_keeps_the_address():
    assert ("ADDRESS", "12 rue de Paris, 75001 Paris") in labels("Jean Dupont 12 rue de Paris, 75001 Paris")
    assert ("ADDRESS", "12 Borgo Pio, 00193 Roma") in labels("Ship to Anna 12 Borgo Pio, 00193 Roma")
