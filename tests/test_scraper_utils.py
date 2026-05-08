from app.scrapers.g1 import _parse_g1_date


def test_parse_g1_date_returns_datetime_for_valid_date():
    parsed = _parse_g1_date("Fri, 08 May 2026 12:00:00 -0300")
    assert parsed is not None
    assert parsed.year == 2026


def test_parse_g1_date_returns_none_for_invalid_date():
    assert _parse_g1_date("invalid-date") is None
