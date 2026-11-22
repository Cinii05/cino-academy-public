"""Private release archive inventory and privacy tests; zero external services."""
import hashlib
import json
import re
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / "plugin.json").read_text("utf-8-sig"))
ZIP = ROOT / "dist" / f"cino-academy-{META['version']}-review-candidate.zip"
SKILLS = {"cino-academy", "cino-essay-planner", "cino-literature-scout",
          "cino-literature-synthesiser", "cino-reference-auditor", "cino-writing-master"}


class PrivateArchiveSafety(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.z = zipfile.ZipFile(ZIP)
        cls.names = cls.z.namelist()

    @classmethod
    def tearDownClass(cls):
        cls.z.close()

    def test_no_duplicate_or_traversing_paths(self):
        self.assertEqual(len(self.names), len(set(self.names)))
        for p in self.names:
            self.assertNotIn("\\", p)
            self.assertFalse(p.startswith("/") or p.startswith("../") or "/../" in p)
            self.assertFalse(p.startswith(".") or p.startswith(".."))

    def test_allowlisted_files_only(self):
        for p in self.names:
            self.assertTrue(p in {"plugin.json", "assets/icon.svg"}
                            or (p.startswith("skills/") and p.endswith(".md")), p)

    def test_all_six_skills_and_minimal_metadata(self):
        found = {x.split("/")[1] for x in self.names if re.fullmatch(r"skills/[^/]+/SKILL.md", x)}
        self.assertEqual(found, SKILLS)
        self.assertEqual(META["version"], "1.3.0")
        self.assertNotIn("mcpServers", META)

    def test_no_user_samples_or_account_material(self):
        words = ("voiceprofile.json", "downloads/", "personal-coursework",
                 "/onedrive/documents/", "student-id", ".env.", "api_key=", "private-marking")
        for path in self.names:
            self.assertFalse(any(w in path.lower() for w in words), path)
            s = self.z.read(path).decode("utf-8")
            self.assertFalse(any(w in s.lower() for w in words), path)

    def test_credential_shapes_not_present(self):
        patterns = [r"ghp_[A-Za-z0-9]{30,}", r"sk-[A-Za-z0-9]{20,}",
                    r"AKIA[A-Z0-9]{16}", r"-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----"]
        for path in self.names:
            s = self.z.read(path).decode("utf-8")
            for pattern in patterns:
                self.assertIsNone(re.search(pattern, s), (path, pattern))

    def test_no_executable_payloads_or_symlink(self):
        for info in self.z.infolist():
            mode = (info.external_attr >> 16) & 0o170000
            self.assertNotEqual(mode, 0o120000, info.filename)
            self.assertLess(info.file_size, 500000, info.filename)
            self.assertFalse(info.filename.lower().endswith((".py", ".exe", ".sh", ".ps1",
                                                              ".bat", ".js", ".dll")))

    def test_no_untrusted_setup_commands_in_package(self):
        for path in self.names:
            s = self.z.read(path).decode("utf-8")
            for s_bad in ("curl | bash", "wget | bash", "curl -fsSL", "pip install -r",
                          "ignore all previous instructions", "disable safety checks"):
                self.assertNotIn(s_bad, s.casefold(), path)

    def test_metadata_private_publication_does_not_claim_connected_services(self):
        s = META["extensions"]["com.openai"]["interface"]["longDescription"].lower()
        self.assertIn("no built-in", s)
        self.assertTrue(META["extensions"]["com.openai"]["interface"]["privacyPolicyURL"].startswith("https://"))
        self.assertTrue(META["extensions"]["com.openai"]["interface"]["termsOfServiceURL"].startswith("https://"))

    def test_references_are_bundled(self):
        needed = ["ASSIGNMENT-CARD.md", "EVIDENCE-LEDGER.md", "ARGUMENT-WORKSHOP.md",
                  "REVISION-RECEIPT.md", "FIRST-CLASS-STYLE-LAB.md",
                  "ACADEMIC-VOICE-QA.md", "VOICE-LEARNING.md"]
        for f in needed:
            self.assertTrue(any(p.endswith("/" + f) for p in self.names), f)

    def test_archive_integrity_and_report_hash(self):
        self.assertIsNone(self.z.testzip())
        receipt = json.loads((ROOT / "RELEASE.json").read_text("utf-8"))
        self.assertEqual(receipt["public_zip_sha256"], hashlib.sha256(ZIP.read_bytes()).hexdigest())

    def test_portable_package_cannot_claim_live_check(self):
        for p in ["skills/cino-reference-auditor/SKILL.md",
                  "skills/cino-academy/references/EVIDENCE-LEDGER.md"]:
            t = self.z.read(p).decode("utf-8").lower()
            self.assertIn("not", t)
            self.assertIn("tool", t)


if __name__ == "__main__":
    unittest.main()
