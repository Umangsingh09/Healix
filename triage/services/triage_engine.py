class TriageEngine:
    CRITICAL_KEYWORDS = [
        "chest pain", "stroke", "seizures", "unconsciousness", "severe breathlessness",
        "heart attack", "cardiac arrest", "loss of consciousness", "severe bleeding"
    ]

    HIGH_RISK_KEYWORDS = [
        "sweating", "breathlessness", "severe pain", "bleeding heavily"
    ]

    MEDIUM_RISK_KEYWORDS = [
        "fever", "headache", "nausea", "vomiting", "dizziness",
        "abdominal pain", "difficulty breathing"
    ]

    LOW_RISK_KEYWORDS = [
        "cough", "sore throat", "runny nose", "mild pain",
        "fatigue", "minor injury"
    ]

    RECOMMENDATIONS = {
        'Critical': "Emergency symptoms detected. Immediate medical help required.",
        'High': "Immediate medical attention required. Call emergency services.",
        'Medium': "See a doctor within 24 hours.",
        'Low': "Monitor symptoms, rest and hydrate. Consult a doctor if symptoms worsen."
    }

    @staticmethod
    def analyze_symptoms(symptoms):
        symptoms_lower = symptoms.lower()

        if any(keyword in symptoms_lower for keyword in TriageEngine.CRITICAL_KEYWORDS):
            risk_level = 'Critical'
        elif any(keyword in symptoms_lower for keyword in TriageEngine.HIGH_RISK_KEYWORDS):
            risk_level = 'High'
        elif any(keyword in symptoms_lower for keyword in TriageEngine.MEDIUM_RISK_KEYWORDS):
            risk_level = 'Medium'
        else:
            risk_level = 'Low'

        recommendation = TriageEngine.RECOMMENDATIONS[risk_level]

        return risk_level, recommendation