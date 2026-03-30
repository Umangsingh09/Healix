# ai_engine/tasks/medical_tasks.py
from crewai import Task


EXTRACTION_TEMPLATE = """
Analyze the following patient input and extract all available medical information.

PATIENT INPUT:
{patient_input}

Return ONLY a valid JSON object with these exact fields (use null for missing data):
{{
  "patient_age": <integer or null>,
  "patient_gender": "<string or null>",
  "chief_complaint": "<one clear sentence summarizing the main complaint>",
  "symptoms": ["<symptom1>", "<symptom2>"],
  "symptom_duration": "<string describing duration>",
  "severity_indicators": ["<any red flag symptoms>"],
  "vital_signs": {{
    "blood_pressure": null,
    "heart_rate": null,
    "temperature": null,
    "spo2": null,
    "respiratory_rate": null
  }},
  "medical_history": ["<relevant history if mentioned>"],
  "current_medications": ["<medications if mentioned>"],
  "allergies": ["<allergies if mentioned>"]
}}

Return ONLY the JSON object. No explanation, no markdown, no backticks.
"""

TRIAGE_TEMPLATE = """
Using ESI (Emergency Severity Index) protocols, determine the triage level for this patient.

EXTRACTED PATIENT DATA:
{extracted_data}

Triage Level Criteria:
- CRITICAL: Immediate life-saving intervention required (airway, breathing, circulation threat)
- HIGH: High-risk situation, severe pain/distress, needs assessment within 10 minutes
- MEDIUM: Urgent, two or more resources needed, can wait up to 30 minutes
- LOW: Simple exam/prescription, minimal resources, can wait hours

Return ONLY a valid JSON object:
{{
  "triage_level": "<CRITICAL|HIGH|MEDIUM|LOW>",
  "esi_level": <1|2|3|4>,
  "confidence": <0.0-1.0>,
  "primary_concern": "<main clinical concern driving this level>",
  "red_flags": ["<specific symptoms or findings that elevated the triage level>"],
  "response_window_minutes": <integer>
}}

Return ONLY the JSON object. No explanation, no markdown, no backticks.
"""

MEDICAL_KNOWLEDGE_TEMPLATE = """
Based on the patient's symptoms and data, provide the top 3 differential diagnoses.

PATIENT DATA:
{extracted_data}

TRIAGE ASSESSMENT:
{triage_data}

For each diagnosis, consider:
- Symptom match score
- Patient demographics (age, gender)
- Symptom duration and progression
- Red flag indicators

Return ONLY a valid JSON object:
{{
  "conditions": [
    {{
      "name": "<condition name>",
      "icd_10": "<ICD-10 code>",
      "probability": <0.0-1.0>,
      "supporting_symptoms": ["<symptom1>", "<symptom2>"],
      "against_symptoms": ["<anything making this less likely>"],
      "urgency_note": "<brief clinical note>"
    }}
  ],
  "rule_out_immediately": ["<conditions that MUST be ruled out first>"]
}}

Return ONLY the JSON object. No explanation, no markdown, no backticks.
"""

RECOMMENDATION_TEMPLATE = """
Generate a clinical action plan for this patient.

PATIENT DATA: {extracted_data}
TRIAGE LEVEL: {triage_data}
POSSIBLE CONDITIONS: {medical_data}

Return ONLY a valid JSON object:
{{
  "immediate_actions": ["<action within first 5 minutes>"],
  "diagnostic_tests": [
    {{
      "test": "<test name>",
      "rationale": "<why this test>",
      "priority": "<STAT|URGENT|ROUTINE>"
    }}
  ],
  "specialist_referrals": ["<specialist type if needed>"],
  "medications_to_consider": [
    {{
      "drug": "<drug name>",
      "dose": "<dose>",
      "rationale": "<why>"
    }}
  ],
  "monitoring": ["<what to monitor continuously>"],
  "disposition": "<ED_RESUS|ED_FAST_TRACK|OBSERVATION|WAITING_ROOM|DISCHARGE>"
}}

Return ONLY the JSON object. No explanation, no markdown, no backticks.
"""

EXPLANATION_TEMPLATE = """
You are writing the XAI (Explainable AI) rationale for a clinical triage decision.

FULL CONTEXT:
Patient Data: {extracted_data}
Triage Decision: {triage_data}
Conditions: {medical_data}
Recommendations: {recommendation_data}

Write a clear, concise clinical explanation (3-5 sentences) that:
1. States the primary reason for the triage level
2. Names the 2-3 specific symptoms most responsible for the decision
3. Explains why the top condition was ranked highest
4. Notes any important caveats or uncertainties

Return ONLY a valid JSON object:
{{
  "summary": "<2-3 sentence patient summary for handoff>",
  "triage_rationale": "<explanation of WHY this triage level was chosen>",
  "key_factors": ["<factor 1>", "<factor 2>", "<factor 3>"],
  "confidence_note": "<any caveats about the AI's confidence>",
  "clinician_alert": "<anything a clinician should double-check immediately or null>"
}}

Return ONLY the JSON object. No explanation, no markdown, no backticks.
"""


def create_all_tasks(agents, patient_input):
    """Build the full 5-task pipeline."""

    extraction_task = Task(
        description=EXTRACTION_TEMPLATE.format(patient_input=patient_input),
        agent=agents['extraction'],
        expected_output="JSON object with structured patient data",
    )

    triage_task = Task(
        description=TRIAGE_TEMPLATE.format(extracted_data="{extraction_task_output}"),
        agent=agents['triage'],
        expected_output="JSON object with triage level, ESI level, confidence",
        context=[extraction_task],
    )

    medical_task = Task(
        description=MEDICAL_KNOWLEDGE_TEMPLATE.format(
            extracted_data="{extraction_task_output}",
            triage_data="{triage_task_output}",
        ),
        agent=agents['medical'],
        expected_output="JSON object with top 3 differential diagnoses",
        context=[extraction_task, triage_task],
    )

    recommendation_task = Task(
        description=RECOMMENDATION_TEMPLATE.format(
            extracted_data="{extraction_task_output}",
            triage_data="{triage_task_output}",
            medical_data="{medical_task_output}",
        ),
        agent=agents['recommendation'],
        expected_output="JSON object with diagnostic tests, actions, disposition",
        context=[extraction_task, triage_task, medical_task],
    )

    explanation_task = Task(
        description=EXPLANATION_TEMPLATE.format(
            extracted_data="{extraction_task_output}",
            triage_data="{triage_task_output}",
            medical_data="{medical_task_output}",
            recommendation_data="{recommendation_task_output}",
        ),
        agent=agents['explanation'],
        expected_output="JSON object with XAI rationale",
        context=[extraction_task, triage_task, medical_task, recommendation_task],
    )

    return [extraction_task, triage_task, medical_task, recommendation_task, explanation_task]


# SECURITY AUDIT: This file contains potential security issues
# Please review and implement proper security measures
# Issues detected: general_security_review
