# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# import requests
# import json
# import os

# API_KEY = os.environ.get("OPENROUTER_API_KEY")
# API_URL = "https://openrouter.ai/api/v1/chat/completions"
# MODEL = "perplexity/sonar-reasoning-pro"
# INSTRUCTION = (
#     "Is this related with Marketing, if YES then revert with best possible answer "
#     "ELSE return with NO and add some quote which can explain user that this tool "
#     "has been developed to address only Marketing related topics."
# )

# @csrf_exempt
# def index(request):
#     response_text = None
#     if request.method == "POST":
#         prompt = request.POST.get("prompt")
#         if prompt:
#             full_prompt = f"{prompt}\n\n{INSTRUCTION}"
#             headers = {
#                 "Authorization": f"Bearer {API_KEY}",
#                 "Content-Type": "application/json"
#             }
#             payload = {
#                 "model": MODEL,
#                 "messages": [
#                     {"role": "system", "content": "You are a smart assistant."},
#                     {"role": "user", "content": full_prompt}
#                 ],
#                 "temperature": 0.7
#             }
#             try:
#                 res = requests.post(API_URL, headers=headers, json=payload)
#                 if res.status_code == 200:
#                     response_text = res.json()["choices"][0]["message"]["content"].strip()
#                 else:
#                     response_text = "❌ API returned error."
#             except Exception as e:
#                 response_text = "❌ Something went wrong."
#         else:
#             response_text = "❗ Please enter a prompt."
#     return render(request, "index.html", {"response_text": response_text})


# @csrf_exempt
# def marketing_api(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             prompt = data.get("prompt")
#             if not prompt:
#                 return JsonResponse({"error": "Prompt is missing"}, status=400)

#             full_prompt = f"{prompt}\n\n{INSTRUCTION}"
#             headers = {
#                 "Authorization": f"Bearer {API_KEY}",
#                 "Content-Type": "application/json"
#             }
#             payload = {
#                 "model": MODEL,
#                 "messages": [
#                     {"role": "system", "content": "You are a smart assistant."},
#                     {"role": "user", "content": full_prompt}
#                 ],
#                 "temperature": 0.7
#             }
#             res = requests.post(API_URL, headers=headers, json=payload)
#             if res.status_code == 200:
#                 result = res.json()["choices"][0]["message"]["content"].strip()
#                 return JsonResponse({"response": result}, status=200)
#             else:
#                 return JsonResponse({"error": "API Error"}, status=500)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Only POST allowed"}, status=405)

import requests
import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Constants
API_KEY = os.environ.get("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "perplexity/sonar-reasoning-pro"

INSTRUCTION = (
    "You are a strict assistant that only responds to marketing-related queries.\n"
    "If the user's question is about marketing, respond with the best possible answer.\n"
    "If the question is not about marketing, do not answer it directly.\n"
    "Instead, say: 'NO. This tool only answers marketing-related questions.'\n"
    "Then generate a thoughtful or motivational quote inspired by the user's prompt.\n"
    "Ensure the quote is relevant to the topic or emotion in the prompt, but never answer non-marketing questions directly."
)

EXAMPLES = (
    "Examples:\n"
    "Q: What is SEO?\nA: SEO, or Search Engine Optimization, is a digital marketing strategy...\n"
    "Q: What is the capital of India?\nA: NO. This tool only answers marketing-related questions.\n"
    "Q: Who won the cricket match yesterday?\nA: NO. This tool only answers marketing-related questions.\n"
)

@csrf_exempt
def index(request):
    response_text = None
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        if prompt:
            full_prompt = f"{EXAMPLES}\nUser Question: {prompt}\n\n{INSTRUCTION}"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a strict and intelligent assistant who ONLY responds to marketing-related queries. "
                            "If a query is unrelated to marketing, respond with 'NO. This tool only answers marketing-related questions.'"
                        )
                    },
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": 0.5
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


@csrf_exempt
def marketing_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt")
            if not prompt:
                return JsonResponse({"error": "Prompt is missing"}, status=400)

            full_prompt = f"{EXAMPLES}\nUser Question: {prompt}\n\n{INSTRUCTION}"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a strict and intelligent assistant who ONLY responds to marketing-related queries. "
                            "If a query is unrelated to marketing, respond with 'NO. This tool only answers marketing-related questions.'"
                        )
                    },
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": 0.5
            }

            res = requests.post(API_URL, headers=headers, json=payload)
            if res.status_code == 200:
                result = res.json()["choices"][0]["message"]["content"].strip()
                return JsonResponse({"response": result}, status=200)
            else:
                print("API Error:", res.status_code, res.text)
                return JsonResponse({"error": "API Error"}, status=500)

        except Exception as e:
            print("Exception:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)

