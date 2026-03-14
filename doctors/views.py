from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Doctor
from .serializers import DoctorSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctors(request):
    """Get all doctors"""
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_doctor(request):
    """Recommend doctor based on risk level"""
    risk_level = request.GET.get('risk_level', '').lower()

    if not risk_level:
        return Response({"error": "risk_level parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Doctor recommendation logic based on risk level
    recommendations = {
        'critical': {
            'specialization': 'emergency',
            'message': 'Immediate emergency room visit required',
            'urgency': 'Critical - Call emergency services (911)'
        },
        'high': {
            'specialization': 'cardiology',  # or neurology depending on symptoms
            'message': 'Urgent specialist consultation needed',
            'urgency': 'High - See specialist within 24 hours'
        },
        'medium': {
            'specialization': 'general',
            'message': 'Schedule appointment with general physician',
            'urgency': 'Medium - See doctor within 1 week'
        },
        'low': {
            'specialization': 'general',
            'message': 'Home care and monitoring recommended',
            'urgency': 'Low - Self-care with follow-up if needed'
        }
    }

    if risk_level not in recommendations:
        return Response({"error": "Invalid risk level"}, status=status.HTTP_400_BAD_REQUEST)

    rec = recommendations[risk_level]

    # Find available doctors of the recommended specialization
    doctors = Doctor.objects.filter(
        specialization=rec['specialization'],
        is_available=True
    )[:5]  # Limit to 5 recommendations

    serializer = DoctorSerializer(doctors, many=True)

    response_data = {
        'risk_level': risk_level,
        'recommendation': rec,
        'available_doctors': serializer.data
    }

    logger.info(f"Doctor recommendation for risk level {risk_level}: {len(doctors)} doctors found")
    return Response(response_data)
