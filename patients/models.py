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