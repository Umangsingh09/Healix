from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer


# GET all patients
@api_view(['GET'])
def get_patients(request):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


# POST create patient
@api_view(['POST'])
def create_patient(request):
    serializer = PatientSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


# GET single patient
@api_view(['GET'])
def get_patient(request, pk):
    patient = Patient.objects.get(id=pk)
    serializer = PatientSerializer(patient)
    return Response(serializer.data)


# PUT update patient
@api_view(['PUT'])
def update_patient(request, pk):
    patient = Patient.objects.get(id=pk)
    serializer = PatientSerializer(instance=patient, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


# DELETE patient
@api_view(['DELETE'])
def delete_patient(request, pk):
    patient = Patient.objects.get(id=pk)
    patient.delete()

    return Response("Patient deleted successfully")