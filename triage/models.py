from django.db import models

class TriageResult(models.Model):
    RISK_LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    symptoms_input = models.TextField(null=True, blank=True)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES)
    recommendation = models.TextField()
    explanation = models.TextField(blank=True, null=True)
    possible_conditions = models.JSONField(default=list, blank=True)
    key_symptoms = models.JSONField(default=list, blank=True)
    confidence_score = models.FloatField(default=0.0)
    processing_time_ms = models.IntegerField(default=0)
    analyzed_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Triage: {self.symptoms_input[:50] if self.symptoms_input else 'No symptoms'} - {self.risk_level}"
