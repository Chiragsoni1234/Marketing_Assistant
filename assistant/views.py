
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import os

API_KEY = os.environ.get("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@csrf_exempt
def marketing_api(request):
    if request.method == "POST":
        try:
            # Support both JSON and form data
            if request.content_type == 'application/json':
                body = json.loads(request.body)
                prompt = body.get("prompt")
            else:
                prompt = request.POST.get("prompt")

            if not prompt:
                return JsonResponse({"error": "No prompt provided."}, status=400)

            # Determine response type
            if is_marketing_related(prompt):
                answer = generate_marketing_response(prompt)
                return JsonResponse({"response": answer, "type": "marketing"})
            else:
                quote = generate_stylish_quote(prompt)
                return JsonResponse({"response": quote, "type": "quote"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method is allowed."}, status=405)


# --- Classify prompt ---
def is_marketing_related(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "perplexity/sonar-reasoning-pro",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Respond only with YES or NO. "
                    "If the input is about any of the following topics, respond with YES:\n"
                    "- marketing\n"
                    "- digital marketing\n"
                    "- online marketing\n"
                    "- advertising\n"
                    "- paid ads\n"
                    "- Google Ads\n"
                    "- Facebook Ads\n"
                    "- Instagram Ads\n"
                    "- influencer marketing\n"
                    "- content marketing\n"
                    "- email marketing\n"
                    "- marketing campaigns\n"
                    "- product promotions\n"
                    "- SEO (search engine optimization)\n"
                    "- SEM (search engine marketing)\n"
                    "- keyword research\n"
                    "- backlinks\n"
                    "- social media marketing\n"
                    "- social media growth\n"
                    "- brand awareness\n"
                    "- brand management\n"
                    "- branding\n"
                    "- storytelling for marketing\n"
                    "- marketing strategy\n"
                    "- campaign optimization\n"
                    "- conversion rate\n"
                    "- conversion rate optimization (CRO)\n"
                    "- lead generation\n"
                    "- lead nurturing\n"
                    "- customer journey\n"
                    "- sales funnel\n"
                    "- funnel optimization\n"
                    "- CRM (customer relationship management)\n"
                    "- growth marketing\n"
                    "- growth hacking\n"
                    "- user acquisition\n"
                    "- customer acquisition cost (CAC)\n"
                    "- customer retention\n"
                    "- customer engagement\n"
                    "- remarketing\n"
                    "- retargeting\n"
                    "- email automation\n"
                    "- marketing automation\n"
                    "- PPC (pay per click)\n"
                    "- affiliate marketing\n"
                    "- referral marketing\n"
                    "- mobile marketing\n"
                    "- SMS marketing\n"
                    "- product launch strategy\n"
                    "- marketing metrics\n"
                    "- marketing KPIs\n"
                    "- marketing budget\n"
                    "- B2B marketing\n"
                    "- B2C marketing\n"
                    "- ecommerce marketing\n"
                    "- PR (public relations)\n"
                    "- online reputation\n"
                    "- performance marketing\n"
                    "- brand equity\n"
                    "- brand positioning\n"
                    "- value proposition\n"
                    "- competitive analysis\n"
                    "- influencer partnerships\n"
                    "- video marketing\n"
                    "- viral marketing\n"
                    "- website traffic growth\n"
                    "- analytics and metrics\n"
                    "- audience segmentation\n"
                    "- product-market fit\n"
                    "- go-to-market strategy\n"
                    "- omni-channel marketing\n"
                    "- landing page optimization\n"
                    "If the input is not related to any of these, respond with NO. Do not explain."
                )
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


# --- Generate marketing response ---
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
    else:
        print("❌ Marketing response error:", response.status_code, response.text)
        return "❌ Error generating marketing answer."


# --- Generate quote if not marketing ---
def generate_stylish_quote(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
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
    else:
        print("❌ Quote generation error:", response.status_code, response.text)
        return "❌ Error generating quote."


# --- Default HTML form-based view ---
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