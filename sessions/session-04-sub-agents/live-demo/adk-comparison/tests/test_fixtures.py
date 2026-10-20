import json
import re

from fixtures.make_fixtures import generate


def test_generation_is_deterministic(tmp_path):
    generate(tmp_path / "a")
    generate(tmp_path / "b")
    for relative in ("shipit/tests/output.log", "shipit/app/payments.py", "expected.json"):
        assert (tmp_path / "a" / relative).read_bytes() == (tmp_path / "b" / relative).read_bytes()


def test_log_has_about_1500_lines_and_two_real_failures(tmp_path):
    generate(tmp_path)
    log = (tmp_path / "shipit/tests/output.log").read_text().splitlines()
    assert 1400 <= len(log) <= 1600
    failing = {m.group(1) for line in log if (m := re.match(r"^tests/\S+::(\w+) FAILED$", line))}
    assert failing == {"test_refund_rounding", "test_webhook_retry"}


def test_planted_security_issues(tmp_path):
    generate(tmp_path)
    code = (tmp_path / "shipit/app/payments.py").read_text()
    assert code.count("sk_test_FAKE_DO_NOT_USE") == 1
    assert len(re.findall(r'f"SELECT', code)) == 1
    assert "amount_pence: int" in code and "retries: int = 3" in code


def test_readme_drifts_from_code(tmp_path):
    generate(tmp_path)
    readme = (tmp_path / "shipit/README.md").read_text()
    assert "Amount in pounds" in readme
    assert "`retries` defaults to 5" in readme


def test_expected_json_matches_generated_files(tmp_path):
    generate(tmp_path)
    expected = json.loads((tmp_path / "expected.json").read_text())
    assert len(expected) == 6
    for finding in expected:
        assert {"id", "category", "file", "keywords", "min_match"} <= finding.keys()
        assert 2 <= len(finding["keywords"]) <= 3
        text = (tmp_path / "shipit" / finding["file"]).read_text()
        assert finding["evidence"] in text, finding["id"]


def test_expected_json_is_outside_the_agent_sandbox(tmp_path):
    generate(tmp_path)
    assert not (tmp_path / "shipit" / "expected.json").exists()
