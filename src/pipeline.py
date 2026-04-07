from __future__ import annotations

import json
from pathlib import Path

from src.generation import build_study_guide
from src.sample_data import ensure_corpus


def run_pipeline(base_dir: str | Path) -> dict:
    base_path = Path(base_dir)
    dataset = ensure_corpus(base_path)
    study_guide = build_study_guide(base_path)

    processed_dir = base_path / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    report_path = processed_dir / "study_guide_report.json"
    report_path.write_text(json.dumps(study_guide, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "dataset_source": "syllabus_study_guide_local_sample",
        "public_dataset_reference": dataset["reference_path"],
        "document_count": 8,
        "section_count": len(study_guide["sections"]),
        "checklist_item_count": len(study_guide["study_checklist"]),
        "top_section_source": study_guide["sections"][0]["source_doc_id"],
        "report_artifact": str(report_path),
    }
    return summary
