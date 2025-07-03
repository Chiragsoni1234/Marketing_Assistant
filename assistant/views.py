import requests
import os
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Constants
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
        user_prompt = request.POST.get("prompt")

        if user_prompt:
            full_prompt = f"{user_prompt}\n\n{INSTRUCTION}"

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are an intelligent assistant who follows instructions strictly."},
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
                    print("API error:", res.status_code, res.text)
            except Exception as e:
                response_text = "❌ Something went wrong."
                print("Request exception:", str(e))
        else:
            response_text = "❗ Please enter a prompt."

    return render(request, "index.html", {"response_text": response_text})
