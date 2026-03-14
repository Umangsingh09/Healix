# ai_engine/crew/triage_crew.py
import json
import time
from crewai import Crew, Process, LLM
from ..agents.medical_agents import (
    get_extraction_agent,
    get_triage_agent,
    get_medical_knowledge_agent,
    get_recommendation_agent,
    get_explanation_agent,
)
from ..tasks.medical_tasks import create_all_tasks
from django.conf import settings


def _safe_json(raw: str) -> dict:
    """Strip markdown fences and parse JSON safely."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    cleaned = cleaned.strip().strip("`").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"raw": raw, "parse_error": True}


def build_crew(llm):
    agents = {
        'extraction':     get_extraction_agent(llm),
        'triage':         get_triage_agent(llm),
        'medical':        get_medical_knowledge_agent(llm),
        'recommendation': get_recommendation_agent(llm),
        'explanation':    get_explanation_agent(llm),
    }
    return agents


def run_triage(patient_input: str) -> dict:
    """
    Run the full 5-agent pipeline.
    Returns a structured dict with all outputs.
    """
    start = time.time()

    llm = LLM(
        model=getattr(settings, 'HEALIX_LLM_MODEL', 'gpt-4o-mini'),
        api_key=getattr(settings, 'OPENAI_API_KEY', None),
        temperature=0.2,
    )

    agents = build_crew(llm)
    tasks = create_all_tasks(agents, patient_input)

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        memory=True,                  # shared crew memory
        max_rpm=10,
    )

    result = crew.kickoff()

    # Parse each task output
    outputs = result.tasks_output if hasattr(result, 'tasks_output') else []
    raw_outputs = [str(t.raw) for t in outputs] if outputs else ['{}'] * 5

    extracted   = _safe_json(raw_outputs[0]) if len(raw_outputs) > 0 else {}
    triage      = _safe_json(raw_outputs[1]) if len(raw_outputs) > 1 else {}
    medical     = _safe_json(raw_outputs[2]) if len(raw_outputs) > 2 else {}
    recommend   = _safe_json(raw_outputs[3]) if len(raw_outputs) > 3 else {}
    explanation = _safe_json(raw_outputs[4]) if len(raw_outputs) > 4 else {}

    elapsed_ms = int((time.time() - start) * 1000)

    return {
        "success": True,
        "processing_time_ms": elapsed_ms,
        "model_used": getattr(settings, 'HEALIX_LLM_MODEL', 'gpt-4o-mini'),
        "patient_data": extracted,
        "triage": triage,
        "conditions": medical,
        "recommendations": recommend,
        "explanation": explanation,
        # Convenience top-level fields for the frontend
        "triage_level": triage.get("triage_level", "UNKNOWN"),
        "summary": explanation.get("summary", ""),
        "triage_rationale": explanation.get("triage_rationale", ""),
    }
