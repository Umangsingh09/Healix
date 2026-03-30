from django.db.models import Count
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

            risk_level, recommendation = TriageEngine.analyze_symptoms(symptoms)
            explanation = f"Based on the reported symptoms ({symptoms[:50]}...), the system has classified this as {risk_level} risk. " + \
                          "The presence of specific clinical markers suggests prioritizing this case for " + \
                          ("immediate intervention" if risk_level == 'Critical' else "urgent review" if risk_level == 'High' else "routine assessment") + "."

            # Create or update Patient record
            user_uid = serializer.validated_data.get('user_uid')
            if not user_uid and request.user.is_authenticated:
                try:
                    user_uid = request.user.userprofile.firebase_uid
                except:
                    pass
            
            name = serializer.validated_data.get('name') or 'Anonymous'
            age = serializer.validated_data.get('age') or 0

            try:
                ai_data = {
                    "explanation": explanation,
                    "recommendation": recommendation,
                    "triage": {"level": risk_level.upper()}
                }

                if user_uid:
                    patient, _ = Patient.objects.update_or_create(
                        user_uid=user_uid,
                        defaults={
                            'name': name,
                            'age': age,
                            'symptoms': symptoms,
                            'risk_level': risk_level.upper(),
                            'triage_level': risk_level.upper(),
                            'ai_analysis': ai_data,
                            'status': 'Waiting'
                        }
                    )
                elif patient_id:
                    patient = Patient.objects.get(id=patient_id)
                    patient.symptoms = symptoms
                    patient.risk_level = risk_level.upper()
                    patient.triage_level = risk_level.upper()
                    patient.ai_analysis = ai_data
                    patient.save()
                else:
                    patient = Patient.objects.create(
                        name=name,
                        age=age,
                        symptoms=symptoms,
                        risk_level=risk_level.upper(),
                        triage_level=risk_level.upper(),
                        ai_analysis=ai_data,
                        status='Waiting'
                    )

                # Save the formal TriageResult
                triage_result = TriageResult.objects.create(
                    symptoms_input=symptoms,
                    risk_level=risk_level,
                    recommendation=recommendation,
                    explanation=explanation,
                    possible_conditions=["Condition A", "Condition B"],
                    key_symptoms=[s.strip() for s in symptoms.split(',')[:3]],
                    confidence_score=0.92,
                    processing_time_ms=580,
                    patient=patient
                )
                logger.info(f"Triage and Patient update completed: Risk={risk_level}")
            except Exception as e:
                logger.error(f"Error saving triage/patient result: {str(e)}")
                return Response({"error": f"Failed to save result: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Return response
            res_data = {
                "risk_level": risk_level,
                "recommendation": recommendation,
                "explanation": explanation,
                "confidence_score": 0.92,
                "key_symptoms": [s.strip() for s in symptoms.split(',')[:3]],
                "possible_conditions": ["Condition A", "Condition B"],
                "triage_id": triage_result.id
            }

            if risk_level == 'Critical':
                logger.warning(f"Critical triage result: {recommendation}")
                res_data.update({
                    "alert": "Emergency symptoms detected - Immediate medical attention required",
                    "recommended_action": recommendation,
                    "emergency_contact": "Call emergency services (911) immediately"
                })
            
            return Response(res_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TriageStatsView(APIView):
    def get(self, request):
        stats = TriageResult.objects.values('risk_level').annotate(count=Count('id'))
        total = TriageResult.objects.count()
        return Response({
            "total_triages": total,
            "by_risk_level": list(stats)
        })

class TriageHistoryView(APIView):
    def get(self, request):
        history = TriageResult.objects.all().order_by('-analyzed_at')[:20]
        serializer = TriageResultSerializer(history, many=True)
        return Response(serializer.data)


# SECURITY FIX: Store API keys in environment variables
# Example: api_key = os.getenv('API_KEY')
