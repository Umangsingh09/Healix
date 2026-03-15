from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Patient
from .serializers import PatientSerializer, TriageHistorySerializer
from triage.models import TriageResult
import logging

logger = logging.getLogger(__name__)


class PatientPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# GET all patients (Class-based for remote compatibility)
class PatientListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PatientSerializer
    pagination_class = PatientPagination
    queryset = Patient.objects.all().order_by('-created_at')


# GET all patients (Function-based)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patients(request):
    patients = Patient.objects.all().order_by('-created_at')
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)

# GET patients for logged-in user (For Patients)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_patients(request):
    user_uid = request.query_params.get('user_uid')
    if not user_uid:
        return Response({"error": "user_uid required"}, status=status.HTTP_400_BAD_REQUEST)
    
    patients = Patient.objects.filter(user_uid=user_uid).order_by('-created_at')
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)
def health_agent(request):
    return render(request, 'patients/health_agent.html')

# POST create patient
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_patient(request):
    logger.info(f"Attempting to create patient: {request.data.get('name')}")
    serializer = PatientSerializer(data=request.data)

    if serializer.is_valid():
        try:
            patient = serializer.save()
            # Create passport automatically
            from .models import HealthPassport
            HealthPassport.objects.get_or_create(patient=patient)
            
            logger.info(f"Successfully created patient {patient.name} (ID: {patient.id}) and generated passport.")
            return Response({
                "status": "success",
                "patient_id": patient.id,
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error during patient creation process: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    logger.warning(f"Patient creation failed: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET single patient
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient(request, pk):
    try:
        patient = Patient.objects.get(id=pk)
        logger.info(f"Retrieved patient: {patient.name} (ID: {pk})")
    except Patient.DoesNotExist:
        logger.warning(f"Patient not found: ID {pk}")
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error retrieving patient {pk}: {str(e)}")
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializer = PatientSerializer(patient)
    return Response(serializer.data)


# PUT/PATCH update patient
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_patient(request, pk):
    try:
        patient = Patient.objects.get(id=pk)
    except Patient.DoesNotExist:
        logger.warning(f"Patient not found for update: ID {pk}")
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error retrieving patient {pk} for update: {str(e)}")
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Enable partial updates for PATCH requests
    partial = request.method == 'PATCH'
    serializer = PatientSerializer(instance=patient, data=request.data, partial=partial)
    
    if serializer.is_valid():
        serializer.save()
        logger.info(f"Updated patient: {patient.name} (ID: {pk})")
        return Response(serializer.data)
    
    logger.warning(f"Invalid data for patient update (ID: {pk}): {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE patient
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_patient(request, pk):
    try:
        patient = Patient.objects.get(id=pk)
        patient_name = patient.name
        patient.delete()
        logger.info(f"Deleted patient: {patient_name} (ID: {pk})")
        return Response({"message": "Patient deleted successfully"})
    except Patient.DoesNotExist:
        logger.warning(f"Patient not found for deletion: ID {pk}")
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error deleting patient {pk}: {str(e)}")
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# GET patient triage history
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_triage_history(request, pk):
    try:
        patient = Patient.objects.get(id=pk)
    except Patient.DoesNotExist:
        logger.warning(f"Patient not found for triage history: ID {pk}")
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error retrieving patient {pk} for triage history: {str(e)}")
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    triage_results = TriageResult.objects.filter(patient=patient).order_by('-created_at')
    serializer = TriageHistorySerializer(triage_results, many=True)
    logger.info(f"Retrieved triage history for patient: {patient.name} (ID: {pk}), {len(triage_results)} results")
    return Response(serializer.data)