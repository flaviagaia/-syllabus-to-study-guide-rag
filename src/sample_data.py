from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd


PUBLIC_DATASET_REFERENCE = {
    "dataset_name": "Syllabus and course-material style corpus",
    "dataset_reference": "Local education corpus for study-guide generation workflows.",
    "dataset_note": (
        "This project uses a deterministic local syllabus corpus to demonstrate grounded study-guide generation "
        "without depending on external document stores or online APIs."
    ),
}


def _atomic_write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", suffix=".csv", delete=False, dir=path.parent, encoding="utf-8") as tmp_file:
        temp_path = Path(tmp_file.name)
    try:
        df.to_csv(temp_path, index=False)
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _atomic_write_json(payload: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", suffix=".json", delete=False, dir=path.parent, encoding="utf-8") as tmp_file:
        temp_path = Path(tmp_file.name)
    try:
        temp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _build_corpus() -> pd.DataFrame:
    rows = [
        {
            "doc_id": "SG-1001",
            "module": "Module 1",
            "title": "Course Syllabus",
            "section_title": "Course Goals",
            "content": (
                "The course introduces students to data science workflows, reproducibility, model evaluation, "
                "and communication of findings. By the end of the term, students should be able to design, "
                "evaluate, and explain an applied machine learning solution."
            ),
        },
        {
            "doc_id": "SG-1002",
            "module": "Module 1",
            "title": "Course Calendar",
            "section_title": "Weekly Structure",
            "content": (
                "Weeks one through three focus on Python, data preparation, and exploratory analysis. "
                "Weeks four through six cover supervised learning, validation, and interpretation. "
                "The final weeks focus on project delivery and communication."
            ),
        },
        {
            "doc_id": "SG-1003",
            "module": "Module 2",
            "title": "Assignment Guide",
            "section_title": "Deliverables",
            "content": (
                "Students must submit one notebook, one short written reflection, and one slide deck. "
                "The notebook should contain reproducible code, documented assumptions, and final conclusions."
            ),
        },
        {
            "doc_id": "SG-1004",
            "module": "Module 2",
            "title": "Reading Notes",
            "section_title": "Evaluation Metrics",
            "content": (
                "Students should understand the difference between accuracy, precision, recall, F1, and ROC-AUC. "
                "Metric choice depends on the business objective and on whether class imbalance is relevant."
            ),
        },
        {
            "doc_id": "SG-1005",
            "module": "Module 3",
            "title": "Project Rubric",
            "section_title": "What Strong Work Looks Like",
            "content": (
                "Strong projects explain problem framing, justify modeling choices, report limitations, and include testing. "
                "High-scoring submissions also discuss trade-offs and communicate findings clearly to non-technical audiences."
            ),
        },
        {
            "doc_id": "SG-1006",
            "module": "Module 3",
            "title": "FAQ",
            "section_title": "Time Management",
            "content": (
                "Students are encouraged to review materials at the start of each week, block one session for implementation, "
                "and reserve one session for revision and reflection before submission deadlines."
            ),
        },
        {
            "doc_id": "SG-1007",
            "module": "Module 4",
            "title": "Capstone Brief",
            "section_title": "Presentation Expectations",
            "content": (
                "The final presentation should explain the problem, the data, the method, the result, and the limitation in under seven minutes. "
                "Slides should prioritize clarity over volume."
            ),
        },
        {
            "doc_id": "SG-1008",
            "module": "Module 4",
            "title": "Office Hours Policy",
            "section_title": "Support Model",
            "content": (
                "Students should use office hours for conceptual blockers, feedback on project framing, and clarification on rubric expectations. "
                "Private questions are reserved for grade discussions and accommodation requests."
            ),
        },
    ]
    return pd.DataFrame(rows)


def ensure_corpus(base_dir: str | Path) -> dict[str, str]:
    base_path = Path(base_dir)
    corpus_path = base_path / "data" / "raw" / "syllabus_corpus.csv"
    reference_path = base_path / "data" / "raw" / "public_dataset_reference.json"

    corpus_df = _build_corpus()
    _atomic_write_csv(corpus_df, corpus_path)
    _atomic_write_json(PUBLIC_DATASET_REFERENCE, reference_path)

    return {
        "corpus_path": str(corpus_path),
        "reference_path": str(reference_path),
    }
