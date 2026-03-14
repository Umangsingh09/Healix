from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from .serializers import TriageAnalyzeSerializer, TriageResultSerializer
from .models import TriageResult
from .services.triage_engine import TriageEngine
from patients.models import Patient
import logging

logger = logging.getLogger(__name__)

class AnalyzeTriageView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = TriageAnalyzeSerializer(data=request.data)
        if serializer.is_valid():
            symptoms = serializer.validated_data['symptoms']
            patient_id = serializer.validated_data.get('patient_id')
            patient = None
            if patient_id:
                try:
                    patient = Patient.objects.get(id=patient_id)
                except Patient.DoesNotExist:
                    logger.warning(f"Patient not found for triage: ID {patient_id}")
                    return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    logger.error(f"Error retrieving patient {patient_id} for triage: {str(e)}")
                    return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            risk_level, recommendation = TriageEngine.analyze_symptoms(symptoms)

            # Save to database
            try:
                triage_result = TriageResult.objects.create(
                    symptoms=symptoms,
                    risk_level=risk_level,
                    recommendation=recommendation,
                    patient=patient
                )
                logger.info(f"Triage analysis completed: Risk={risk_level}, Patient={patient.name if patient else 'Anonymous'}")
            except Exception as e:
                logger.error(f"Error saving triage result: {str(e)}")
                return Response({"error": "Failed to save triage result"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Return response
            if risk_level == 'Critical':
                logger.warning(f"Critical triage result: {recommendation}")
                alert_data = {
                    "risk_level": risk_level,
                    "alert": "Emergency symptoms detected - Immediate medical attention required",
                    "recommended_action": recommendation,
                    "emergency_contact": "Call emergency services (911) immediately",
                    "triage_id": triage_result.id
                }
                return Response(alert_data, status=status.HTTP_200_OK)
            else:
                return Response({
                    "risk_level": risk_level,
                    "recommendation": recommendation,
                    "triage_id": triage_result.id
                }, status=status.HTTP_200_OK)
        
        logger.warning(f"Invalid triage request data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
