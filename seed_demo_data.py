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
            "risk_level": "CRITICAL",
            "triage_level": "CRITICAL",
            "ai_analysis": {
                "triage": {"level": "CRITICAL"}, 
                "explanation": "Symptoms strongly suggest Acute Myocardial Infarction (heart attack). Immediate intervention required."
            },
            "status": "In ER"
        },
        {
            "name": "Sarah Jenkins",
            "age": 28,
            "symptoms": "High fever (103F), stiff neck, severe headache, photophobia.",
            "risk_level": "CRITICAL",
            "triage_level": "CRITICAL",
            "ai_analysis": {
                "triage": {"level": "CRITICAL"}, 
                "explanation": "Classic meningitis presentation. Requires immediate lumbar puncture and IV antibiotics."
            },
            "status": "Pending Doctor"
        },
        {
            "name": "Elias Thorne",
            "age": 62,
            "symptoms": "Sudden onset of facial drooping on right side, slurred speech, weakness in right arm.",
            "risk_level": "HIGH",
            "triage_level": "HIGH",
            "ai_analysis": {
                "triage": {"level": "HIGH"},
                "explanation": "Possible ischemic stroke. Needs urgent CT scan to evaluate for tPA eligibility."
            },
            "status": "Pending Imaging"
        },
        {
            "name": "Olivia Martinez",
            "age": 19,
            "symptoms": "Sharp pain in lower right abdomen, nausea, vomiting, fever of 100.5F for last 6 hours.",
            "risk_level": "HIGH",
            "triage_level": "HIGH",
            "ai_analysis": {
                "triage": {"level": "HIGH"},
                "explanation": "High suspicion of acute appendicitis. Surgical consult recommended."
            },
            "status": "Waiting"
        },
        {
            "name": "David Wallace",
            "age": 35,
            "symptoms": "Persistent cough for 3 weeks, mild fever, fatigue. Spitting up some yellowish phlegm.",
            "risk_level": "MEDIUM",
            "triage_level": "MEDIUM",
            "ai_analysis": {
                "triage": {"level": "MEDIUM"},
                "explanation": "Symptoms consistent with bronchitis or mild pneumonia. Recommend chest X-ray and antibiotics."
            },
            "status": "Waiting"
        },
        {
            "name": "Emily Carter",
            "age": 41,
            "symptoms": "Twisted ankle while jogging. Cannot bear weight. Swollen and bruised.",
            "risk_level": "MEDIUM",
            "triage_level": "MEDIUM",
            "ai_analysis": {
                "triage": {"level": "MEDIUM"},
                "explanation": "Possible severe sprain or fracture. Needs X-ray imaging, but vitals are stable."
            },
            "status": "Waiting"
        },
        {
            "name": "Liam Bennett",
            "age": 24,
            "symptoms": "Sore throat, runny nose, dry cough for 2 days. No fever.",
            "risk_level": "LOW",
            "triage_level": "LOW",
            "ai_analysis": {
                "triage": {"level": "LOW"},
                "explanation": "Classic viral upper respiratory infection symptoms. Supportive care and rest advised."
            },
            "status": "Waiting"
        },
        {
            "name": "Sophia Patel",
            "age": 30,
            "symptoms": "Mild rash on forearms after using a new laundry detergent. Itchy but no breathing issues.",
            "risk_level": "LOW",
            "triage_level": "LOW",
            "ai_analysis": {
                "triage": {"level": "LOW"},
                "explanation": "Localized allergic contact dermatitis. Non-urgent."
            },
            "status": "Waiting"
        }
    ]

    print("Seeding new patient data for hackathon demo...")
    now = timezone.now()
    for idx, data in enumerate(patients_data):
        patient = Patient.objects.create(**data)
        # Offset creation times to make the queue look realistic
        patient.created_at = now - timedelta(minutes=15 * (len(patients_data) - idx))
        patient.save()
        print(f"Created patient: {patient.name} - {patient.triage_level}")

    print("\nSuccessfully seeded database with realistic hackathon data!")

if __name__ == "__main__":
    seed_data()
