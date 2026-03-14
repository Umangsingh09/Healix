from rest_framework import serializers
from .models import TriageResult

class TriageAnalyzeSerializer(serializers.Serializer):
    symptoms = serializers.CharField(required=True, min_length=3, max_length=1000)
    patient_id = serializers.IntegerField(required=False, allow_null=True)
    
    def validate_symptoms(self, value):
        if not value.strip():
            raise serializers.ValidationError("Symptoms description cannot be empty.")
        return value.strip()

class TriageResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriageResult
        fields = ['risk_level', 'recommendation']