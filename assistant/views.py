# from django.shortcuts import render
# import requests

# # Helper function to classify if the question is marketing-related
# def is_marketing_related(prompt):
#     headers = {
#         "Authorization": "Bearer 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",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "model": "perplexity/sonar-reasoning-pro",
#         "messages": [
#             {
#                 "role": "system",
#                 "content": (
#                     "You are a strict classifier. Only respond with one word: YES or NO. "
#                     "If the input is about marketing, advertising, digital marketing, SEO, branding, customer acquisition, "
#                     "or promotion, respond with YES. Otherwise respond with NO."
#                 )
#             },
#             {
#                 "role": "user",
#                 "content": f"Is this marketing related? '{prompt}'"
#             }
#         ],
#         "temperature": 0  # Low temperature ensures predictable answers
#     }

#     try:
#         response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
#         if response.status_code == 200:
#             result = response.json()
#             answer = result['choices'][0]['message']['content'].strip().lower()
#             return answer == "yes"
#         return False
#     except Exception as e:
#         print("Error in classification:", e)
#         return False


# # Main view for the chat assistant
# # def index(request):
# #     response_text = None
# #     if request.method == "POST":
# #         prompt = request.POST.get('prompt')

# #         if is_marketing_related(prompt):
# #             headers = {
# #                 "Authorization": "Bearer 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",
# #                 "Content-Type": "application/json"
# #             }

# #             data = {
# #                 "model": "perplexity/sonar-reasoning-pro",
# #                 "messages": [
# #                     {
# #                         "role": "system",
# #                         "content": "You are a helpful and expert marketing assistant. Answer only in the context of marketing."
# #                     },
# #                     {
# #                         "role": "user",
# #                         "content": prompt
# #                     }
# #                 ],
# #                 "temperature": 0.7
# #             }

# #             try:
# #                 response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
# #                 if response.status_code == 200:
# #                     result = response.json()
# #                     ai_answer = result["choices"][0]["message"]["content"]
# #                     response_text = (
# #                         "✅ Yes, this is a great marketing-related question!\n\n" + ai_answer
# #                     )
# #                 else:
# #                     response_text = f"❌ Error {response.status_code}: {response.text}"
# #             except Exception as e:
# #                 response_text = f"⚠️ Exception occurred: {str(e)}"
# #         else:
# #             response_text = "❌ This question is not related to marketing."

# #     return render(request, "index.html", {"response_text": response_text})


# def index(request):
#     response_text = None
#     if request.method == "POST":
#         prompt = request.POST.get('prompt')

#         if is_marketing_related(prompt):
#             headers = {
#                 "Authorization": "Bearer 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",
#                 "Content-Type": "application/json"
#             }

#             data = {
#                 "model": "perplexity/sonar-reasoning-pro",
#                 "messages": [
#                     {
#                         "role": "system",
#                         "content": "You are a helpful and expert marketing assistant. Answer only in the context of marketing."
#                     },
#                     {
#                         "role": "user",
#                         "content": prompt
#                     }
#                 ],
#                 "temperature": 0.7
#             }

#             try:
#                 response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
#                 if response.status_code == 200:
#                     result = response.json()
#                     response_text = result["choices"][0]["message"]["content"]
#                 else:
#                     response_text = ""  # No response if error
#             except Exception as e:
#                 response_text = ""
#         else:
#             response_text = "This assistant only handles marketing queries"  # Don't return anything if not marketing related

#     return render(request, "index.html", {"response_text": response_text})


import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def marketing_api(request):
    if request.method == "POST":
        try:
            # Check Content-Type header
            if request.content_type == 'application/json':
                body = json.loads(request.body)
                prompt = body.get("prompt")
            else:
                prompt = request.POST.get("prompt")

            if not prompt:
                return JsonResponse({"error": "No prompt provided."}, status=400)

            # Classification and response
            if is_marketing_related(prompt):
                answer = generate_marketing_response(prompt)
                return JsonResponse({"response": answer, "type": "marketing"})
            else:
                quote = generate_stylish_quote(prompt)
                return JsonResponse({"response": quote, "type": "quote"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method is allowed."}, status=405)



API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Helper: Check if prompt is marketing-related
def is_marketing_related(prompt):
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
        "model": "perplexity/sonar-reasoning-pro",
        "messages": [
            {
                "role": "system",
                "content": "Respond only with YES or NO. If the input is about marketing, advertising, SEO, digital marketing, branding, or promotion, respond with YES. Otherwise respond with NO."
            },
            {
                "role": "user",
                "content": f"Is this marketing related? '{prompt}'"
            }
        ],
        "temperature": 0
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"].strip().lower()
            return answer == "yes"
    except Exception as e:
        print("Classification error:", e)
    return False

# Generate marketing response
def generate_marketing_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "perplexity/sonar-reasoning-pro",
        "messages": [
            {"role": "system", "content": "You are a helpful and expert marketing assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return "✅ Yes, this is a marketing-related question!\n\n" + response.json()["choices"][0]["message"]["content"]
    return "❌ Error generating marketing answer."

# Generate stylish quote if not marketing
def generate_stylish_quote(prompt):
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
        "model": "perplexity/sonar-reasoning-pro",
        "messages": [
            {"role": "system", "content": "You are a quote generator. Return a stylish and inspirational quote based on the user's query."},
            {"role": "user", "content": f"Give me a stylish quote based on: '{prompt}'"}
        ],
        "temperature": 0.9
    }

    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return "💡 This isn't a marketing question, but here's a quote for you:\n\n" + response.json()["choices"][0]["message"]["content"]
    return "❌ Error generating quote."

# Django view
def index(request):
    response_text = None
    if request.method == "POST":
        prompt = request.POST.get('prompt')

        if prompt:
            if is_marketing_related(prompt):
                response_text = generate_marketing_response(prompt)
            else:
                response_text = generate_stylish_quote(prompt)


    return render(request, "index.html", {"response_text": response_text})
