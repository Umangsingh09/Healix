from django.shortcuts import render

def home(request):
    return render(request, 'landing/index.html')

def qr_scanner(request):
    return render(request, 'features/qr_scanner.html')

def my_passport(request):
    return render(request, 'patients/my_passport.html')

from django.http import JsonResponse
from patients.models import Patient, HealthPassport
from triage.models import TriageResult

def passport_view(request, uid):
    try:
        # HLX-000042 → patient id 42
        raw_id = uid.upper().replace('HLX-', '').lstrip('0')
        patient_id = int(raw_id) if raw_id else 0
        patient = Patient.objects.get(id=patient_id)
        
        try:
            from triage.models import TriageResult
            history = list(TriageResult.objects.filter(
                patient=patient).order_by('-analyzed_at')[:10])
            latest = history[0] if history else None
        except:
            history, latest = [], None

        return JsonResponse({
            'uid': uid,
            'patient': {
                'id': patient.id,
                'name': patient.name,
                'age': patient.age,
                'risk_level': patient.risk_level,
                'symptoms': patient.symptoms,
            },
            'latest_triage': {
                'date': latest.analyzed_at.isoformat(),
                'risk_level': latest.risk_level,
                'conditions': latest.possible_conditions or [],
                'recommendation': str(latest.recommendation or '')[:150],
                'confidence_score': float(latest.confidence_score or 0),
            } if latest else None,
            'history_count': len(history),
        })
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Patient not found — run seed_demo_data'}, status=404)
    except (ValueError, Exception) as e:
        return JsonResponse({'error': f'Invalid passport ID: {str(e)}'}, status=400)
    except HealthPassport.DoesNotExist:
        # FALLBACK FOR DEMO / GUEST EXPLORER
        if uid == 'HLX-000042':
            return JsonResponse({
                'uid': 'HLX-000042',
                'patient': {
                    'id': 42,
                    'name': 'Guest Explorer',
                    'age': 28,
                    'risk': 'Low',
                    'symptoms': 'Demo exploration for hackathon',
                },
                'latest_triage': {
                    'date': '2026-03-15T08:00:00',
                    'risk': 'Low',
                    'conditions': ['Perfect Health'],
                    'recommendation': 'Everything looks great! Continue using Healix for preventive care.',
                    'confidence': 0.99,
                },
                'history_count': 1,
                'issued': '2026-03-15T08:00:00',
            })
        return JsonResponse({'error': 'Passport not found'}, status=404)

def passport_page(request, uid):
    """Renders the full health profile page when QR is scanned"""
    return render(request, 'features/passport_profile.html', {'uid': uid})


# SECURITY AUDIT: This file contains potential security issues
# Please review and implement proper security measures
# Issues detected: general_security_review
