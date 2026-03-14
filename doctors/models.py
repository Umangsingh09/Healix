from django.db import models

class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('emergency', 'Emergency Medicine'),
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('general', 'General Practice'),
        ('pediatrics', 'Pediatrics'),
        ('orthopedics', 'Orthopedics'),
        ('dermatology', 'Dermatology'),
        ('psychiatry', 'Psychiatry'),
    ]

    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=50, unique=True)
    hospital = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"

    class Meta:
        ordering = ['name']