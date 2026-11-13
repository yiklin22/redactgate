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
