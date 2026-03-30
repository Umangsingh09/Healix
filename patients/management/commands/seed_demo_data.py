# patients/management/commands/seed_demo_data.py
"""
Run: python manage.py seed_demo_data
Creates 8 realistic demo patients with triage results so the
dashboard looks populated for hackathon demos.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random


DEMO_PATIENTS = [
    {
        "name": "Raj Sharma",
        "age": 58,
        "symptoms": "Chest pain, sweating, dizziness, left arm pain",
        "risk_level": "Critical",
        "triage": {
            "risk_level": "Critical",
            "recommendation": "🚨 IMMEDIATE EMERGENCY CARE REQUIRED. Call 112 immediately. 12-lead ECG, troponin, IV access, aspirin 325mg. Cardiology consult stat.",
            "possible_conditions": ["Acute Myocardial Infarction", "Unstable Angina", "Aortic Dissection"],
            "key_symptoms": ["chest pain", "sweating", "left arm pain"],
            "confidence_score": 0.92,
            "explanation": "Classic ACS triad in 58M — chest pain radiating to left arm with diaphoresis for 2h exceeds ESI Level 1 threshold. Age and symptom cluster are primary escalators.",
            "processing_time_ms": 4,
        }
    },
    {
        "name": "Priya Mehta",
        "age": 34,
        "symptoms": "Severe throbbing headache, nausea, photophobia, neck stiffness",
        "risk_level": "Critical",
        "triage": {
            "risk_level": "Critical",
            "recommendation": "🚨 Rule out meningitis immediately. CT head, lumbar puncture if no contraindication, blood cultures, IV ceftriaxone. Neuro consult.",
            "possible_conditions": ["Bacterial Meningitis", "Subarachnoid Hemorrhage", "Severe Migraine"],
            "key_symptoms": ["severe headache", "neck stiffness", "photophobia"],
            "confidence_score": 0.88,
            "explanation": "Neck stiffness with severe headache and photophobia is a meningism triad. Cannot rule out meningitis or SAH — must be treated as critical until imaging confirms otherwise.",
            "processing_time_ms": 5,
        }
    },
    {
        "name": "Anita Desai",
        "age": 71,
        "symptoms": "Difficulty breathing, wheezing, acute confusion, SpO2 low",
        "risk_level": "High",
        "triage": {
            "risk_level": "High",
            "recommendation": "⚠️ Urgent respiratory assessment. Oxygen therapy, nebulised salbutamol, ABG, CXR. Monitor SpO2 continuously. ICU bed on standby.",
            "possible_conditions": ["Acute COPD Exacerbation", "Pneumonia", "Pulmonary Embolism"],
            "key_symptoms": ["breathlessness", "wheezing", "confusion"],
            "confidence_score": 0.85,
            "explanation": "Acute breathlessness with confusion in 71F with known COPD history. Confusion suggests hypoxia-driven altered mentation — escalated to HIGH urgency.",
            "processing_time_ms": 6,
        }
    },
    {
        "name": "Vikram Singh",
        "age": 45,
        "symptoms": "Severe abdominal pain, right lower quadrant, fever 38.9°C, nausea",
        "risk_level": "High",
        "triage": {
            "risk_level": "High",
            "recommendation": "⚠️ Surgical assessment required. FBC, CRP, LFT, urine culture. Abdominal ultrasound or CT abdomen. NPO in case of surgical intervention.",
            "possible_conditions": ["Appendicitis", "Mesenteric Adenitis", "Ovarian Torsion"],
            "key_symptoms": ["right lower quadrant pain", "fever", "nausea"],
            "confidence_score": 0.81,
            "explanation": "RLQ pain with fever and nausea in 45M is highly suspicious for appendicitis. Alvarado score estimation warrants urgent surgical review.",
            "processing_time_ms": 5,
        }
    },
    {
        "name": "Sunita Patel",
        "age": 29,
        "symptoms": "Severe migraine, vomiting, unable to tolerate light, known migraine history",
        "risk_level": "Medium",
        "triage": {
            "risk_level": "Medium",
            "recommendation": "📋 IV antiemetics (metoclopramide), sumatriptan if not contraindicated. Dark quiet room. IV fluids for hydration. CT head only if atypical features.",
            "possible_conditions": ["Migraine with Aura", "Tension Headache", "Cluster Headache"],
            "key_symptoms": ["severe headache", "vomiting", "photophobia"],
            "confidence_score": 0.78,
            "explanation": "Known migraine patient presenting with typical severe migraine features. No meningism signs. Classified MEDIUM — urgent but stable with known diagnosis.",
            "processing_time_ms": 4,
        }
    },
    {
        "name": "Anil Verma",
        "age": 22,
        "symptoms": "Ankle pain, swelling, bruising after sports fall, unable to weight bear",
        "risk_level": "Medium",
        "triage": {
            "risk_level": "Medium",
            "recommendation": "📋 Ottawa Ankle Rules assessment. X-ray if indicated. RICE protocol. Analgesia (ibuprofen + paracetamol). Crutches if unable to weight bear.",
            "possible_conditions": ["Ankle Sprain (Grade II/III)", "Lateral Malleolus Fracture", "Syndesmotic Injury"],
            "key_symptoms": ["ankle pain", "swelling", "inability to weight bear"],
            "confidence_score": 0.82,
            "explanation": "Young male with acute ankle injury post-sports, unable to weight bear. Ottawa rules applicable — X-ray warranted to rule out fracture before discharge.",
            "processing_time_ms": 3,
        }
    },
    {
        "name": "Kavya Reddy",
        "age": 8,
        "symptoms": "Mild fever 37.8°C, runny nose, mild sore throat, sneezing, 2 days duration",
        "risk_level": "Low",
        "triage": {
            "risk_level": "Low",
            "recommendation": "✅ Viral URTI likely. Symptomatic management — paracetamol/ibuprofen for fever, fluids, rest. No antibiotics indicated. Return if fever >39°C or symptoms worsen after 5 days.",
            "possible_conditions": ["Common Cold (Rhinovirus)", "Upper Respiratory Tract Infection", "Influenza (mild)"],
            "key_symptoms": ["mild fever", "runny nose", "sore throat"],
            "confidence_score": 0.88,
            "explanation": "Child with classic viral URTI symptoms, low-grade fever, no red flags. Classified LOW — routine care appropriate. No respiratory distress or signs of secondary bacterial infection.",
            "processing_time_ms": 3,
        }
    },
    {
        "name": "Ramesh Kumar",
        "age": 52,
        "symptoms": "Lower back pain, chronic, worsened after lifting, no neurological symptoms",
        "risk_level": "Low",
        "triage": {
            "risk_level": "Low",
            "recommendation": "✅ Mechanical back pain likely. NSAIDs + muscle relaxant. Heat therapy. Physiotherapy referral. Urgent MRI only if red flag symptoms develop (bladder/bowel involvement, saddle anaesthesia).",
            "possible_conditions": ["Mechanical Lower Back Pain", "Lumbar Muscle Strain", "Lumbar Disc Prolapse (mild)"],
            "key_symptoms": ["lower back pain", "worsened after lifting"],
            "confidence_score": 0.85,
            "explanation": "52M with acute-on-chronic mechanical back pain post-exertion. No neurological deficit, no bladder/bowel symptoms. Classified LOW — no emergency intervention required.",
            "processing_time_ms": 4,
        }
    },
]


class Command(BaseCommand):
    help = 'Seed the database with realistic demo patients and triage results for hackathon demo'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing demo data first')

    def handle(self, *args, **options):
        from patients.models import Patient

        # Try importing triage model
        try:
            from triage.models import TriageResult
            has_triage = True
        except ImportError:
            has_triage = False
            self.stdout.write(self.style.WARNING('Triage app not found — only creating patients'))

        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Patient.objects.all().delete()
            if has_triage:
                TriageResult.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared.'))

        self.stdout.write(self.style.MIGRATE_HEADING('\n[+] Seeding Healix demo data...\n'))

        created_patients = 0
        created_triage   = 0

        for i, data in enumerate(DEMO_PATIENTS):
            # Stagger created_at so queue shows different times
            offset_minutes = random.randint(i * 8, i * 15 + 20)
            created_time   = timezone.now() - timedelta(minutes=offset_minutes)

            # Create patient
            patient, created = Patient.objects.get_or_create(
                name=data['name'],
                defaults={
                    'age':        data['age'],
                    'symptoms':   data['symptoms'],
                    'risk_level': data['risk_level'],
                }
            )

            if not created:
                patient.age        = data['age']
                patient.symptoms   = data['symptoms']
                patient.risk_level = data['risk_level']
                patient.save()

            if created:
                created_patients += 1

            risk_icon = { 'Critical': '[!]', 'High': '[?]', 'Medium': '[-]', 'Low': '[+]' }
            icon = risk_icon.get(data['risk_level'], '•')
            self.stdout.write(f"  {icon}  {data['name']:20} [{data['risk_level']:8}]  age {data['age']}")

            # Create triage result
            if has_triage:
                t_data = data['triage']
                tr, t_created = TriageResult.objects.get_or_create(
                    patient=patient,
                    symptoms_input=data['symptoms'],
                    defaults={
                        'risk_level':          t_data['risk_level'],
                        'recommendation':      t_data['recommendation'],
                        'possible_conditions': t_data['possible_conditions'],
                        'key_symptoms':        t_data['key_symptoms'],
                        'confidence_score':    t_data['confidence_score'],
                        'explanation':         t_data['explanation'],
                        'processing_time_ms':  t_data['processing_time_ms'],
                    }
                )
                if t_created:
                    created_triage += 1

        from patients.models import HealthPassport
        for patient in Patient.objects.all():
            HealthPassport.objects.get_or_create(patient=patient)
        self.stdout.write(self.style.SUCCESS('[OK] Passports created for all patients'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'[OK] Created {created_patients} patients, {created_triage} triage records'))
        self.stdout.write(self.style.SUCCESS('[OK] Dashboard is now populated and ready for demo'))
        self.stdout.write('')
        self.stdout.write('  Risk breakdown:')
        self.stdout.write('    [!] Critical : 2 patients')
        self.stdout.write('    [?] High     : 2 patients')
        self.stdout.write('    [-] Medium   : 2 patients')
        self.stdout.write('    [+] Low      : 2 patients')
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('  -> Open http://127.0.0.1:8000/dashboard/doctor/ to see it live\n'))


# SECURITY AUDIT: This file contains potential security issues
# Please review and implement proper security measures
# Issues detected: general_security_review
