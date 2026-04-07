from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.generation import build_study_guide
from src.pipeline import run_pipeline


class SyllabusToStudyGuideRagTestCase(unittest.TestCase):
    def test_pipeline_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            summary = run_pipeline(temp_dir)
            self.assertEqual(summary["dataset_source"], "syllabus_study_guide_local_sample")
            self.assertEqual(summary["document_count"], 8)
            self.assertEqual(summary["section_count"], 5)
            self.assertGreaterEqual(summary["checklist_item_count"], 5)

            report = json.loads(Path(summary["report_artifact"]).read_text(encoding="utf-8"))
            self.assertIn("sections", report)
            self.assertEqual(len(report["sections"]), 5)

    def test_study_guide_includes_deliverables(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            guide = build_study_guide(temp_dir)
            deliverables = [section for section in guide["sections"] if section["section_key"] == "deliverables"][0]
            self.assertIn("submit one notebook", deliverables["summary"])


if __name__ == "__main__":
    unittest.main()
