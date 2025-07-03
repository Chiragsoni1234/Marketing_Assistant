from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import json
import os

API_KEY = os.environ.get("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "perplexity/sonar-reasoning-pro"
INSTRUCTION = (
    "Is this related with Marketing, if YES then revert with best possible answer "
    "ELSE return with NO and add some quote which can explain user that this tool "
    "has been developed to address only Marketing related topics."
)

@csrf_exempt
def index(request):
    response_text = None
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        if prompt:
            full_prompt = f"{prompt}\n\n{INSTRUCTION}"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are a smart assistant."},
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": 0.7
            }
            try:
                res = requests.post(API_URL, headers=headers, json=payload)
                if res.status_code == 200:
                    response_text = res.json()["choices"][0]["message"]["content"].strip()
                else:
                    response_text = "❌ API returned error."
            except Exception as e:
                response_text = "❌ Something went wrong."
        else:
            response_text = "❗ Please enter a prompt."
    return render(request, "index.html", {"response_text": response_text})


@csrf_exempt
def marketing_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt")
            if not prompt:
                return JsonResponse({"error": "Prompt is missing"}, status=400)

            full_prompt = f"{prompt}\n\n{INSTRUCTION}"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are a smart assistant."},
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": 0.7
            }
            res = requests.post(API_URL, headers=headers, json=payload)
            if res.status_code == 200:
                result = res.json()["choices"][0]["message"]["content"].strip()
                return JsonResponse({"response": result}, status=200)
            else:
                return JsonResponse({"error": "API Error"}, status=500)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)
