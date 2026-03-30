# api/views.py
import json
import time
import asyncio
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["POST"])
def triage_api(request):
    """Standard triage endpoint — returns complete JSON result."""
    try:
        body = json.loads(request.body)
        patient_input = body.get("patient_input", "").strip()
        if not patient_input:
            return JsonResponse({"error": "patient_input is required"}, status=400)

        # Import here to avoid circular imports
        from ai_engine.crew.triage_crew import run_triage
        result = run_triage(patient_input)
        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({"error": str(e), "success": False}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def triage_stream(request):
    """
    SSE streaming endpoint — yields agent progress events in real time.
    Frontend connects and gets live updates as each agent completes.
    """
    try:
        body = json.loads(request.body)
        patient_input = body.get("patient_input", "").strip()
        if not patient_input:
            return JsonResponse({"error": "patient_input is required"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    def event_stream():
        stages = [
            ("extracting",    "🔍 Extracting symptoms and patient data...",  15),
            ("triaging",      "🚨 Determining urgency level...",              20),
            ("diagnosing",    "🧬 Identifying possible conditions...",        25),
            ("recommending",  "📋 Generating action plan...",                 20),
            ("explaining",    "💡 Building XAI explanation...",               15),
        ]

        def sse(data: dict) -> str:
            return f"data: {json.dumps(data)}\n\n"

        # Emit stage-start events
        for stage_id, message, _ in stages:
            yield sse({"type": "stage_start", "stage": stage_id, "message": message})
            time.sleep(0.05)

        # Run the actual crew
        try:
            from ai_engine.crew.triage_crew import run_triage
            result = run_triage(patient_input)

            # Emit stage-complete events
            stage_data = {
                "extracting":   result.get("patient_data", {}),
                "triaging":     result.get("triage", {}),
                "diagnosing":   result.get("conditions", {}),
                "recommending": result.get("recommendations", {}),
                "explaining":   result.get("explanation", {}),
            }
            for stage_id, _, __ in stages:
                yield sse({
                    "type": "stage_complete",
                    "stage": stage_id,
                    "data": stage_data.get(stage_id, {}),
                })

            # Final complete event
            yield sse({"type": "complete", "result": result})

        except Exception as e:
            yield sse({"type": "error", "message": str(e)})

    response = StreamingHttpResponse(
        event_stream(),
        content_type='text/event-stream',
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response


@require_http_methods(["GET"])
def health_check(request):
    """Simple health check endpoint."""
    return JsonResponse({
        "status": "ok",
        "service": "Healix AI Triage Engine",
        "version": "1.0.0",
    })


# SECURITY AUDIT: This file contains potential security issues
# Please review and implement proper security measures
# Issues detected: general_security_review
