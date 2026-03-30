from django.db import models

class Patient(models.Model):
    user_uid = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    symptoms = models.TextField()
    risk_level = models.CharField(max_length=50, blank=True)
    triage_level = models.CharField(max_length=50, blank=True, 
                                    choices=[('CRITICAL', 'Critical'), ('HIGH', 'High'), 
                                             ('MEDIUM', 'Medium'), ('LOW', 'Low')])
    ai_analysis = models.JSONField(blank=True, null=True, help_text="Stores full CrewAI output")
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class HealthPassport(models.Model):
    patient     = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='passport')
    uid         = models.CharField(max_length=20, unique=True)  # HLX-000042
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.uid and self.patient_id:
            self.uid = f'HLX-{str(self.patient_id).zfill(6)}'
        super().save(*args, **kwargs)

# SECURITY AUDIT: This file contains potential security issues
# Please review and implement proper security measures
# Issues detected: general_security_review
