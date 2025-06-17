from fastapi import FastAPI
from chatbot.nlp_logic import process_user_message
from chatbot.database import store_report, get_user_reports, init_db, update_user_location
from chatbot.weather import fetch_weather_alert
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
init_db()

class UserInput(BaseModel):
    message: str
    user_id: str

class LocationInput(BaseModel):
    location: str
    user_id: str

@app.post("/chat")
async def chat_endpoint(user_input: UserInput):
    intent, response, data = process_user_message(user_input.message)

    if intent == "report_hazard" and data:
        store_report(user_input.user_id, data)

    elif intent == "ask_alert":
        location = data.get("location") if data else None
        if location:
            alert = fetch_weather_alert(location)
            if alert:
                response += f"\n🌧️ Weather Alert for {location}: {alert}"
            else:
                response += "\n⚠️ Unable to fetch real-time weather data right now."
        else:
            response += "\n⚠️ Please mention a valid location for weather info."

    elif intent == "unknown" or not intent:
        response = "🤖 I'm not sure how to help with that. Could you please try asking about hazards or weather alerts?"

    return {
        "response": response,
        "intent": intent,
        "data": data,
        "user_input": user_input.message
    }


@app.get("/reports/{user_id}")
async def get_reports(user_id: str):
    return get_user_reports(user_id)

@app.post("/location")
async def set_location(location_input: LocationInput):
    update_user_location(location_input.user_id, location_input.location)
    return {"message": "Location updated successfully."}

@app.get("/reports/all")
def all_reports():
    data = get_user_reports()
    print("Returning reports:", data)  # DEBUG
    return data

