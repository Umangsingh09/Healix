from rest_framework import serializers
from .models import TriageResult

class TriageAnalyzeSerializer(serializers.Serializer):
    symptoms = serializers.CharField(required=True, min_length=3, max_length=1000)
    patient_id = serializers.IntegerField(required=False, allow_null=True)
    user_uid = serializers.CharField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_null=True)
    age = serializers.IntegerField(required=False, allow_null=True)
    
    def validate_symptoms(self, value):
        if not value.strip():
            raise serializers.ValidationError("Symptoms description cannot be empty.")
        return value.strip()

class TriageResultSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    
    class Meta:
        model = TriageResult
        fields = [
            'id', 'risk_level', 'recommendation', 'explanation', 
            'symptoms_input', 'analyzed_at', 'patient', 'patient_name',
            'possible_conditions', 'key_symptoms', 'confidence_score',
            'processing_time_ms'
        ]

# SECURITY AUDIT: This file contains potential security issues
# Please review and implement proper security measures
# Issues detected: general_security_review
