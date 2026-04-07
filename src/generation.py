from __future__ import annotations

from pathlib import Path

from src.retrieval import TOPIC_QUERIES, retrieve_for_topic


def build_study_guide(base_dir: str | Path) -> dict:
    sections = []
    all_sources = []

    for topic, query in TOPIC_QUERIES.items():
        sources = retrieve_for_topic(base_dir, query, top_k=2)
        all_sources.extend(sources)
        primary = sources[0]

        if topic == "course_objectives":
            section_title = "Course Objectives"
            summary = primary["content"]
        elif topic == "weekly_plan":
            section_title = "Weekly Plan"
            summary = primary["content"]
        elif topic == "deliverables":
            section_title = "Key Deliverables"
            summary = primary["content"]
        elif topic == "study_strategy":
            section_title = "Suggested Study Strategy"
            summary = primary["content"]
        else:
            section_title = "Evaluation Focus"
            summary = primary["content"]

        sections.append(
            {
                "section_key": topic,
                "section_title": section_title,
                "summary": summary,
                "source_doc_id": primary["doc_id"],
                "source_section": primary["section_title"],
                "similarity": primary["similarity"],
            }
        )

    study_checklist = [
        "Review the weekly structure before starting each module.",
        "Track required deliverables and keep code reproducible.",
        "Practice explaining metric choice and model trade-offs.",
        "Reserve time for revision before deadlines.",
        "Prepare a concise explanation of the final project and its limitations.",
    ]

    return {
        "title": "Study Guide Generated from Syllabus Materials",
        "sections": sections,
        "study_checklist": study_checklist,
        "source_count": len(all_sources),
        "limitation_note": (
            "This study guide is grounded only in the local course corpus bundled with the MVP. "
            "A production implementation should track course version, academic term, and instructor updates."
        ),
    }
