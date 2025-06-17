import google.generativeai as genai
import json
import re

# Gemini API setup
genai.configure(api_key="AIzaSyCjH6n0pkmNa7BSJKxhiHURosfzOy5GKoQ")
model = genai.GenerativeModel("gemini-2.0-flash")

def process_user_message(message):
    prompt = f"""
You are a multilingual public safety chatbot for global residents. Understand the user's language, detect intent, respond helpfully, and extract structured data.

Respond ONLY in this exact JSON format:
{{
  "intent": "<intent>",
  "response": "<reply in user's language>",
  "data": {{
    "location": "<location or null>",
    "type": "<hazard type or null>",
    "severity": "<severity or null>",
    "date": "<date or null>"
  }}
}}

Supported intents:
- report_hazard
- ask_alert
- request_help
- smalltalk

### Examples:

User: "There’s a major fire in downtown Chicago"
Response:
{{
  "intent": "report_hazard",
  "response": "Thanks for reporting. Emergency teams are being alerted in downtown Chicago.",
  "data": {{
    "location": "downtown Chicago",
    "type": "fire",
    "severity": "high",
    "date": "today"
  }}
}}

User: "क्या आज बेंगलुरु में बारिश होगी?"
Response:
{{
  "intent": "ask_alert",
  "response": "मैं मौसम की जानकारी जांचता हूँ, कृपया प्रतीक्षा करें।",
  "data": {{
    "location": "बेंगलुरु",
    "type": "rain",
    "severity": null,
    "date": "today"
  }}
}}

User: "Hay una fuga de gas en la calle Bolívar"
Response:
{{
  "intent": "report_hazard",
  "response": "Gracias por informar. Se notificará a los servicios de emergencia.",
  "data": {{
    "location": "calle Bolívar",
    "type": "gas leak",
    "severity": "medium",
    "date": "today"
  }}
}}

User: "Help! I’m stuck on the highway with no phone signal"
Response:
{{
  "intent": "request_help",
  "response": "Emergency help is on its way. Please stay calm.",
  "data": {{
    "location": "highway",
    "type": null,
    "severity": "high",
    "date": "today"
  }}
}}

User: "यहाँ आग लगी है"
Response:
{{
  "intent": "report_hazard",
  "response": "कृपया सुरक्षित रहें। आपातकालीन सेवाओं को सूचित किया जा रहा है।",
  "data": {{
    "location": null,
    "type": "fire",
    "severity": "high",
    "date": "today"
  }}
}}

Now analyze this user input:
"{message}"
"""
    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            json_str = match.group(0)
            parsed = json.loads(json_str)
            return (
                parsed.get("intent", "unknown"),
                parsed.get("response", "Sorry, I couldn’t understand that."),
                parsed.get("data")
            )
        else:
            return "unknown", "🤖 I'm not sure how to help with that. Please rephrase or try again.", None
    except Exception as e:
        return "unknown", "⚠️ I'm facing technical issues. Please try again later.", None

