from rest_framework import serializers
from .models import Patient
from triage.models import TriageResult

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
    
    def validate_age(self, value):
        if value <= 0:
            raise serializers.ValidationError("Age must be a positive integer.")
        if value > 150:
            raise serializers.ValidationError("Age must be realistic (less than 150).")
        return value
    
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value.strip()

class TriageHistorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = TriageResult
        fields = ['symptoms', 'risk_level', 'recommendation', 'created_at']