"""
Unit tests for scripts/discover_new.py

Run with:
  pytest tests/test_discover_new.py -v
"""

import discover_new as dn


def _candidate(**overrides):
    base = {
        "source": "arxiv",
        "kind": "paper",
        "title": "Open Robot Manipulation Policy",
        "url": "https://arxiv.org/abs/2601.00001",
        "published": "2026-01-01",
        "summary": "A robot learning method for manipulation with imitation learning.",
        "links": ["https://arxiv.org/abs/2601.00001"],
    }
    base.update(overrides)
    return dn.Candidate(**base)


def test_extract_urls_deduplicates_and_strips_punctuation():
    urls = dn.extract_urls("See https://example.com, and https://github.com/a/b.")
    assert urls == ["https://example.com", "https://github.com/a/b"]


def test_classify_url():
    assert dn.classify_url("https://github.com/org/repo") == "github"
    assert dn.classify_url("https://huggingface.co/datasets/org/data") == "hf_dataset"
    assert dn.classify_url("https://huggingface.co/org/model") == "hf_model"
    assert dn.classify_url("https://arxiv.org/abs/1234.56789") == "paper"
    assert dn.classify_url("https://project.example") == "project"


def test_assess_relevance_high_for_robotics_terms():
    relevance, reasons = dn.assess_relevance(
        "Robot Manipulation with Vision Language Action Models",
        "We train a robot policy for dexterous manipulation.",
    )
    assert relevance == "high"
    assert any("physical-ai keywords" in reason for reason in reasons)


def test_assess_relevance_low_for_autonomous_driving_only():
    relevance, reasons = dn.assess_relevance(
        "End-to-End Autonomous Driving Dataset",
        "A traffic and lane detection benchmark for self driving.",
    )
    assert relevance == "low"
    assert any("exclusion keywords" in reason for reason in reasons)


def test_find_duplicate_matches_by_url():
    candidate = _candidate(links=["https://github.com/example/robot"])
    matches = dn.find_duplicate_matches(candidate, [
        {
            "_file": "models.yaml",
            "id": "robot",
            "name": "Other",
            "github_url": "https://github.com/example/robot",
            "paper_url": "",
            "hf_url": "",
            "project_url": "",
        }
    ])
    assert matches == ["models.yaml:robot URL match"]


def test_find_duplicate_matches_by_name():
    candidate = _candidate(title="Open Robot Manipulation Policy")
    matches = dn.find_duplicate_matches(candidate, [
        {
            "_file": "models.yaml",
            "id": "open-robot-manipulation-policy",
            "name": "Open Robot Manipulation Policy",
            "github_url": "",
            "paper_url": "",
            "hf_url": "",
            "project_url": "",
        }
    ])
    assert matches == ["models.yaml:open-robot-manipulation-policy name match"]


def test_decide_recommendation_rejects_duplicates():
    candidate = _candidate()
    candidate.relevance = "high"
    candidate.duplicate_matches = ["models.yaml:x URL match"]
    candidate.checks = [
        dn.LinkCheck(
            url="https://github.com/example/robot",
            kind="github",
            status="available",
        )
    ]
    recommendation, reasons = dn.decide_recommendation(candidate)
    assert recommendation == "reject"
    assert "duplicate" in reasons[0]


def test_decide_recommendation_needs_review_without_public_links():
    candidate = _candidate()
    candidate.relevance = "high"
    recommendation, reasons = dn.decide_recommendation(candidate)
    assert recommendation == "needs_review"
    assert "no verified public" in reasons[0]


def test_evaluate_candidates_no_verify_marks_links_not_checked(monkeypatch):
    monkeypatch.setattr(dn, "load_yaml_entries", lambda: [])
    candidate = _candidate(links=[
        "https://arxiv.org/abs/2601.00001",
        "https://github.com/example/robot",
    ])

    result = dn.evaluate_candidates([candidate], verify_links=False)

    assert result[0].checks[0].status == "not_checked"
    assert result[0].checks[0].kind == "github"


def test_candidate_review_payload_contains_expected_contract():
    candidate = _candidate()
    payload = dn.candidate_review_payload(candidate)
    assert payload["paper_url"] == "https://arxiv.org/abs/2601.00001"
    assert "expected_json" in payload
    assert "autonomous-driving-only" in payload["question"]


def test_run_llm_review_command_parses_json():
    candidate = _candidate()
    review = dn.run_llm_review_command(
        candidate,
        "python3 -c \"import json; print(json.dumps({'decision':'needs_review','reason':'ok'}))\"",
    )
    assert review["status"] == "ok"
    assert review["decision"] == "needs_review"


def test_run_llm_review_command_handles_invalid_json():
    candidate = _candidate()
    review = dn.run_llm_review_command(candidate, "python3 -c \"print('not json')\"")
    assert review["status"] == "error"
    assert "invalid JSON" in review["reason"]


def test_evaluate_candidates_runs_llm_review_command(monkeypatch):
    monkeypatch.setattr(dn, "load_yaml_entries", lambda: [])
    candidate = _candidate()
    result = dn.evaluate_candidates(
        [candidate],
        verify_links=False,
        llm_review_command="python3 -c \"import json; print(json.dumps({'decision':'reject','reason':'paper only'}))\"",
    )
    assert result[0].llm_review["status"] == "ok"
    assert result[0].llm_review["decision"] == "reject"


def test_render_markdown_states_no_issues_created():
    candidate = _candidate()
    candidate.relevance = "high"
    candidate.recommendation = "needs_review"
    candidate.llm_review = {"status": "ok", "decision": "needs_review", "reason": "official link unclear"}
    report = dn.render_markdown([candidate])
    assert "No GitHub issues were created" in report
    assert "Open Robot Manipulation Policy" in report
    assert "LLM decision" in report
