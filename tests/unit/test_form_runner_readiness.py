from tests.selenium.form_runner import expected_variant_from_url


def test_expected_variant_defaults_to_golden():
    assert expected_variant_from_url("https://example.test/") == "golden"


def test_expected_variant_reads_valid_mutant_query_before_fragment():
    url = "https://example.test/?variant=M18#loan"
    assert expected_variant_from_url(url) == "M18"


def test_expected_variant_rejects_unknown_variant():
    url = "https://example.test/?variant=M99"
    assert expected_variant_from_url(url) == "golden"
