from django.db import models

class TriageResult(models.Model):
    RISK_LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    symptoms = models.TextField()
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES)
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Triage: {self.symptoms[:50]} - {self.risk_level}"
