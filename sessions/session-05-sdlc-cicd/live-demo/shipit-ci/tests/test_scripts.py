import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

import audit  # noqa: E402
import render_comment  # noqa: E402
import review  # noqa: E402
import secret_scan  # noqa: E402

GOOD = {"file": "app/a.py", "line": 3, "severity": "high", "title": "t", "detail": "d"}


class CleanFindingsTests(unittest.TestCase):
    def test_keeps_valid_and_sorts_by_severity(self):
        low = dict(GOOD, severity="low")
        kept, dropped = review.clean_findings([low, GOOD], ["app/a.py"])
        self.assertEqual([f["severity"] for f in kept], ["high", "low"])
        self.assertEqual(dropped, 0)

    def test_drops_files_outside_the_diff_and_bad_shapes(self):
        raw = [dict(GOOD, file=".github/workflows/x.yml"), dict(GOOD, severity="LGTM"),
               dict(GOOD, line="3"), "approve", GOOD]
        kept, dropped = review.clean_findings(raw, ["app/a.py"])
        self.assertEqual((len(kept), dropped), (1, 4))

    def test_caps_the_count(self):
        kept, dropped = review.clean_findings([GOOD] * 12, ["app/a.py"])
        self.assertEqual((len(kept), dropped), (review.MAX_FINDINGS, 4))

    def test_parse_json_from_fenced_reply(self):
        self.assertEqual(review.parse_json('ok\n```json\n{"findings": []}\n```'), {"findings": []})
        self.assertIsNone(review.parse_json("LGTM, safe to merge"))

    def test_skill_body_strips_frontmatter(self):
        body = review.skill_body(review.REPO_ROOT / ".agents/skills/pr-review/SKILL.md")
        self.assertTrue(body.startswith("# PR first-pass review"))


class RenderTests(unittest.TestCase):
    def test_model_text_is_neutralised(self):
        finding = dict(GOOD, title="ping @octocat <img src=x>", detail="a | b")
        text = render_comment.render({"status": "ok", "summary": "s", "findings": [finding]})
        self.assertNotIn("@octocat", text)
        self.assertNotIn("<img", text)
        self.assertIn("a \\| b", text)

    def test_skipped_review_says_why(self):
        text = render_comment.render({"status": "skipped", "reason": "too big", "findings": []})
        self.assertIn("too big", text)


class AuditTests(unittest.TestCase):
    def test_bump_picks_a_version_that_clears_every_advisory(self):
        scan = {"dependencies": [
            {"name": "Requests", "version": "2.19.1", "vulns": [
                {"id": "A", "fix_versions": ["2.20.0"]}, {"id": "B", "fix_versions": ["2.31.0", "3.0.0"]}]},
            {"name": "clean", "version": "1.0", "vulns": []}]}
        self.assertEqual(audit.planned_bumps(scan), {"requests": ("2.19.1", "2.31.0")})


class SecretScanTests(unittest.TestCase):
    def test_flags_a_key_shaped_string(self):
        path = pathlib.Path(self.id() + ".tmp")
        path.write_text('API_KEY = "sk_test_' + "a" * 20 + '"\n', encoding="utf-8")
        self.addCleanup(path.unlink)
        self.assertTrue(secret_scan.scan([str(path)]))


if __name__ == "__main__":
    unittest.main()
