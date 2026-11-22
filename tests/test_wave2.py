"""Cino Academy second-wave offline and optional local PDF integration tests."""
from __future__ import annotations
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import source_audit
import marker_calibration
import research_memory
import eval_academy

class SourceVerificationTests(unittest.TestCase):
    PAGES = ["Study participants included 125 students. The intervention was associated with 20% higher satisfaction.",
             "Limitations include self-report and selection bias. No randomized control was used."]

    def case(self, **overrides):
        return dict({"claim_id":"Q1","claim_text":"20% reported higher satisfaction",
                     "quoted_passage":"The intervention was associated with 20% higher satisfaction.",
                     "pdf_page":1}, **overrides)

    def test_locate_real_quote_and_preserve_unverified_support(self):
        out = source_audit.audit_claim(self.case(),self.PAGES)
        self.assertEqual(out["quote_check"], "EXACT_QUOTE_LOCATED")
        self.assertEqual(out["actual_pdf_pages"], [1])
        self.assertEqual(out["claim_support_state"], "UNVERIFIED")
        self.assertEqual(out["publication_attribution"], "NOT_VERIFIED")

    def test_quote_wrong_pdf_page_detected(self):
        x=self.case()
        x["pdf_page"]=2
        self.assertEqual(source_audit.audit_claim(x,self.PAGES)["quote_check"],
                         "QUOTE_ON_OTHER_PDF_PAGE")

    def test_invented_quote_does_not_become_support(self):
        x=self.case()
        x["quoted_passage"]="It proved 99% of people improved"
        a=source_audit.audit_claim(x,self.PAGES)
        self.assertEqual(a["quote_check"],"QUOTE_NOT_LOCATED")
        self.assertEqual(a["claim_support_state"],"UNVERIFIED")

    def test_claim_number_not_in_quote_requires_review(self):
        x=self.case()
        x["claim_text"]="The intervention increased satisfaction by 35%."
        r=source_audit.audit_claim(x,self.PAGES)
        self.assertEqual(r["numeric_check"],"REVIEW_REQUIRED")
        self.assertEqual(r["numbers_in_claim_not_in_supplied_quote"],["35%"])

    def test_absent_quote_does_not_invent_an_evidence_locator(self):
        x=self.case()
        x["quoted_passage"]=""
        r=source_audit.audit_claim(x,self.PAGES)
        self.assertEqual(r["quote_check"],"NO_QUOTE_TO_CHECK")
        self.assertEqual(r["actual_pdf_pages"],[])

    def test_scanned_pdf_text_requirement_no_ocr_guess(self):
        r=source_audit.audit_claim(self.case(),["",""])
        self.assertEqual(r["quote_check"],"NO_EXTRACTABLE_TEXT")
        self.assertEqual(r["claim_support_state"],"UNVERIFIED")

    def test_invalid_declared_page_rejected(self):
        x=self.case()
        x["pdf_page"]=3
        with self.assertRaises(source_audit.SourceAuditError):
            source_audit.audit_claim(x,self.PAGES)

    def test_duplicate_ids_and_missing_manifest_rejected(self):
        # Validate before expensive source extraction on duplicate IDs.
        with self.assertRaises(source_audit.SourceAuditError):
            source_audit.audit_document({"pdf":"anything.pdf","claims":[self.case(),self.case()]})

    def test_actual_local_pdf_extraction_when_preinstalled(self):
        try:
            import pypdf
            from reportlab.pdfgen import canvas
        except ImportError:
            self.skipTest("Optional local pypdf/reportlab not installed in CI")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"synthetic-study.pdf"
            c=canvas.Canvas(str(p))
            c.drawString(50,750, "Trial participants reported 20 percent higher satisfaction.")
            c.showPage()
            c.drawString(50,750, "This small study used voluntary responses.")
            c.save()
            report=source_audit.audit_document({
                "pdf":str(p), "claims":[{
                    "claim_id":"Q01","claim_text":"Trial participants reported 20 percent higher satisfaction.",
                    "quoted_passage":"Trial participants reported 20 percent higher satisfaction.", "pdf_page":1
                }]
            })
            self.assertEqual(report["pdf_page_count"],2)
            self.assertEqual(report["results"][0]["actual_pdf_pages"],[1])
            self.assertEqual(report["results"][0]["quote_check"],"EXACT_QUOTE_LOCATED")
            self.assertEqual(report["pdf_sha256"],hashlib.sha256(p.read_bytes()).hexdigest())

class MarkerCalibrationTests(unittest.TestCase):
    def sample(self, **overrides):
        x={"sample_id":"fake01","human_feedback_verified":True,
           "human_findings":[{"criterion":"brief_compliance","severity":"material"},
                             {"criterion":"critical_evaluation","severity":"material"}],
           "academy_findings":[{"criterion":"brief_compliance","severity":"material"},
                                {"criterion":"structure","severity":"minor"}]}
        x.update(overrides);return x

    def test_finds_missing_material_and_false_positives(self):
        c=marker_calibration.compare_sample(self.sample())
        self.assertEqual((c["true_positives"],c["false_positives"],c["false_negatives"]),(1,1,1))
        self.assertEqual(c["material_misses"],["critical_evaluation"])
        self.assertEqual(c["unmatched_academy_flags"],["structure"])

    def test_refuses_unverified_marker_labels(self):
        with self.assertRaises(ValueError):
            marker_calibration.compare_sample(self.sample(human_feedback_verified=False))

    def test_checks_severity_not_just_label_presence(self):
        x=self.sample(academy_findings=[{"criterion":"brief_compliance","severity":"minor"}])
        r=marker_calibration.compare_sample(x)
        self.assertEqual(r["severity_mismatches"],["brief_compliance"])

    def test_duplicate_or_unknown_category_rejected(self):
        with self.assertRaises(ValueError):
            marker_calibration.compare_sample(self.sample(human_findings=[
                {"criterion":"reflection","severity":"material"},
                {"criterion":"reflection","severity":"minor"}]))
        with self.assertRaises(ValueError):
            marker_calibration.compare_sample(self.sample(academy_findings=[
                {"criterion":"predict_grade","severity":"material"}]))

    def test_calibration_returns_true_counts_not_marks(self):
        r=marker_calibration.calibrate({"samples":[self.sample()]})
        self.assertEqual(r["sample_count"],1)
        self.assertAlmostEqual(r["precision"],0.5)
        self.assertAlmostEqual(r["recall"],0.5)
        self.assertNotIn("predicted_grade",r)

class ResearchMemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.db=research_memory.connect(Path(self.tmp.name)/"sources.db")
        self.card={"card_id":"S1-page2", "module_id":"M1","source_id":"S1",
                   "title":"Synthetic paper","locator":"PDF page 2","excerpt":"The research found a small association.",
                   "note":"Student note: sample too small.","origin_chain":"same-study",
                   "access_level":"PARTIAL_TEXT_INSPECTED","support_state":"UNVERIFIED"}
    def tearDown(self):
        self.db.close();self.tmp.cleanup()

    def test_add_and_search_is_module_scoped(self):
        research_memory.add_card(self.db,self.card)
        self.assertEqual(len(research_memory.search_cards(self.db,"sample","M1")),1)
        self.assertEqual(research_memory.search_cards(self.db,"sample","M2"),[])
        with self.assertRaises(ValueError):
            research_memory.search_cards(self.db,"sample","")

    def test_duplicate_needs_explicit_replace(self):
        research_memory.add_card(self.db,self.card)
        with self.assertRaises(ValueError):
            research_memory.add_card(self.db,self.card)
        updated=dict(self.card,note="Changed after source check")
        research_memory.add_card(self.db,updated,replace=True)
        self.assertEqual(research_memory.search_cards(self.db,"Changed","M1")[0]["note"],
                         "Changed after source check")

    def test_unverified_excerpt_cannot_be_declared_supported(self):
        with self.assertRaises(ValueError):
            research_memory.add_card(self.db,dict(self.card,support_state="SUPPORTED"))

    def test_file_sha_invalidation(self):
        pdf=Path(self.tmp.name)/"source.txt"
        pdf.write_text("source edition one",encoding="utf-8")
        record=dict(self.card,source_path=str(pdf))
        research_memory.add_card(self.db,record)
        self.assertEqual(research_memory.refresh_stale(self.db,module_id="M1"),[])
        pdf.write_text("source edition two",encoding="utf-8")
        self.assertEqual(research_memory.refresh_stale(self.db,module_id="M1"),["S1-page2"])
        self.assertEqual(research_memory.search_cards(self.db,"Synthetic","M1")[0]["stale"],1)

    def test_existing_hash_mismatch_cannot_be_silently_accepted(self):
        file=Path(self.tmp.name)/"evidence.txt"
        file.write_text("original",encoding="utf-8")
        with self.assertRaises(ValueError):
            research_memory.add_card(self.db,dict(self.card,source_path=str(file),source_sha256="a"*64))

    def test_source_no_full_paper_import(self):
        with self.assertRaises(ValueError):
            research_memory.add_card(self.db,dict(self.card,excerpt="a"*1201))

class BenchmarkHarnessTests(unittest.TestCase):
    def outcome(self,passed=True):
        return {"human_verified":True,"reviewer_id":"human-reviewer-synthetic",
                "response_sha256":"a"*64,"ratings":{k:passed for k in eval_academy.DIMENSIONS}}

    def test_all_three_genuinely_labelled_arms_required(self):
        case={"case_id":"C1","frozen_input_sha256":"b"*64,"outcomes":{
            "no_plugin":self.outcome(False),"academy_v1_3":self.outcome(True),
            "academy_candidate":self.outcome(True)}}
        r=eval_academy.score_suite({"cases":[case]})
        self.assertEqual(r["case_count"],1)
        self.assertEqual(r["arms"]["no_plugin"]["pass_rates"]["reasoning"],0)
        self.assertEqual(r["arms"]["academy_candidate"]["pass_rates"]["reasoning"],1)

    def test_unverified_model_self_marking_blocked(self):
        case={"case_id":"C1","frozen_input_sha256":"b"*64,"outcomes":{
            "no_plugin":self.outcome(False),"academy_v1_3":self.outcome(True),
            "academy_candidate":self.outcome(True)}}
        case["outcomes"]["academy_candidate"]["human_verified"]=False
        with self.assertRaises(eval_academy.BenchmarkError):
            eval_academy.score_suite({"cases":[case]})

    def test_missing_arm_or_unfrozen_input_fails(self):
        case={"case_id":"C1","frozen_input_sha256":"b"*64,"outcomes":{
            "no_plugin":self.outcome(False)}}
        with self.assertRaises(eval_academy.BenchmarkError):
            eval_academy.score_suite({"cases":[case]})
        case["frozen_input_sha256"]=""
        with self.assertRaises(eval_academy.BenchmarkError):
            eval_academy.score_suite({"cases":[case]})

class RoutingContractTests(unittest.TestCase):
    def test_frozen_twelve_case_benchmark_inventory(self):
        cases=json.loads((ROOT/"tests/fixtures/wave2_blind_tasks.json").read_text("utf-8"))
        self.assertEqual(len(cases["cases"]),12)
        self.assertEqual(len({x["case_id"] for x in cases["cases"]}),12)
        self.assertTrue(all(x["model_outputs"]=="NOT_RUN" for x in cases["cases"]))
        self.assertTrue(all(x["prompt"] and x["gold_checks"] for x in cases["cases"]))

    def test_four_capabilities_referenced_by_academy(self):
        root=(ROOT/"skills/cino-academy")
        a=(root/"SKILL.md").read_text(encoding="utf-8")
        for f in ("SOURCE-AUDIT-RUNTIME.md","MARKER-CALIBRATION.md",
                  "RESEARCH-MEMORY-RUNTIME.md","BENCHMARK-PROTOCOL.md"):
            self.assertTrue((root/"references"/f).is_file(),f)
            self.assertIn(f,a)
    def test_reflection_check_remains_provenance_bounded(self):
        a=(ROOT/"skills/cino-academy/references/MARKER-CALIBRATION.md").read_text("utf-8")
        for required in ("Initial assumption", "Changed judgement","Own-case application",
                         "current assignment","not a fake"):
            self.assertIn(required.lower(),a.lower())

if __name__ == "__main__":
    unittest.main()
