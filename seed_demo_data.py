import os
import django
from datetime import timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healix.settings')
django.setup()

from patients.models import Patient

def seed_data():
    print("Clearing existing patients...")
    Patient.objects.all().delete()

    patients_data = [
        {
            "name": "Marcus Chen",
            "age": 45,
            "symptoms": "Severe crushing chest pain radiating down left arm, shortness of breath, sweating profusely.",
            "risk_level": "Critical",
            "triage_level": "Critical",
            "ai_analysis": {
                "triage": {"level": "Critical"}, 
                "explanation": "Symptoms strongly suggest Acute Myocardial Infarction (heart attack). Immediate intervention required."
            },
            "status": "In ER"
        },
        {
            "name": "Sarah Jenkins",
            "age": 28,
            "symptoms": "High fever (103F), stiff neck, severe headache, photophobia.",
            "risk_level": "Critical",
            "triage_level": "Critical",
            "ai_analysis": {
                "triage": {"level": "Critical"}, 
                "explanation": "Classic meningitis presentation. Requires immediate lumbar puncture and IV antibiotics."
            },
            "status": "Pending Doctor"
        },
        {
            "name": "Elias Thorne",
            "age": 62,
            "symptoms": "Sudden onset of facial drooping on right side, slurred speech, weakness in right arm.",
            "risk_level": "High",
            "triage_level": "High",
            "ai_analysis": {
                "triage": {"level": "High"},
                "explanation": "Possible ischemic stroke. Needs urgent CT scan to evaluate for tPA eligibility."
            },
            "status": "Pending Imaging"
        },
        {
            "name": "Olivia Martinez",
            "age": 19,
            "symptoms": "Sharp pain in lower right abdomen, nausea, vomiting, fever of 100.5F for last 6 hours.",
            "risk_level": "High",
            "triage_level": "High",
            "ai_analysis": {
                "triage": {"level": "High"},
                "explanation": "High suspicion of acute appendicitis. Surgical consult recommended."
            },
            "status": "Waiting"
        },
        {
            "name": "David Wallace",
            "age": 35,
            "symptoms": "Persistent cough for 3 weeks, mild fever, fatigue. Spitting up some yellowish phlegm.",
            "risk_level": "Medium",
            "triage_level": "Medium",
            "ai_analysis": {
                "triage": {"level": "Medium"},
                "explanation": "Symptoms consistent with bronchitis or mild pneumonia. Recommend chest X-ray and antibiotics."
            },
            "status": "Waiting"
        },
        {
            "name": "Emily Carter",
            "age": 41,
            "symptoms": "Twisted ankle while jogging. Cannot bear weight. Swollen and bruised.",
            "risk_level": "Medium",
            "triage_level": "Medium",
            "ai_analysis": {
                "triage": {"level": "Medium"},
                "explanation": "Possible severe sprain or fracture. Needs X-ray imaging, but vitals are stable."
            },
            "status": "Waiting"
        },
        {
            "name": "Liam Bennett",
            "age": 24,
            "symptoms": "Sore throat, runny nose, dry cough for 2 days. No fever.",
            "risk_level": "Low",
            "triage_level": "Low",
            "ai_analysis": {
                "triage": {"level": "Low"},
                "explanation": "Classic viral upper respiratory infection symptoms. Supportive care and rest advised."
            },
            "status": "Waiting"
        },
        {
            "name": "Sophia Patel",
            "age": 30,
            "symptoms": "Mild rash on forearms after using a new laundry detergent. Itchy but no breathing issues.",
            "risk_level": "Low",
            "triage_level": "Low",
            "ai_analysis": {
                "triage": {"level": "Low"},
                "explanation": "Localized allergic contact dermatitis. Non-urgent."
            },
            "status": "Waiting"
        }
    ]

    from triage.models import TriageResult
    
    print("Clearing existing triage results...")
    TriageResult.objects.all().delete()

    print("Seeding new patient and triage data for hackathon demo...")
    now = timezone.now()
    for idx, data in enumerate(patients_data):
        # Extract fields for Patient model
        patient_fields = {k: v for k, v in data.items() if k != 'explanation'} 
        patient = Patient.objects.create(**patient_fields)
        
        # Offset creation times
        created_at = now - timedelta(minutes=15 * (len(patients_data) - idx))
        patient.created_at = created_at
        patient.save()

        # Create a TriageResult for this patient
        analysis = data.get('ai_analysis', {})
        triage_level = analysis.get('triage', {}).get('level', data['risk_level'])
        explanation = analysis.get('explanation', '')
        
        TriageResult.objects.create(
            patient=patient,
            symptoms_input=data['symptoms'],
            risk_level=triage_level,
            recommendation="Immediate follow-up scheduled." if triage_level in ['Critical', 'High'] else "Scheduled for routine assessment.",
            explanation=explanation,
            confidence_score=0.92 + (idx * 0.01),
            processing_time_ms=4500 + (idx * 200),
            analyzed_at=created_at + timedelta(seconds=120)
        )
        
        print(f"Created patient & triage: {patient.name} - {patient.risk_level}")

    print("\nSuccessfully seeded database with realistic clinical data!")

if __name__ == "__main__":
    seed_data()
