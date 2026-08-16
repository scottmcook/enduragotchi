import os
from fastapi import FastAPI
from garminconnect import Garmin
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
email = os.getenv("GARMIN_EMAIL")
password = os.getenv("GARMIN_PASSWORD")

app = FastAPI()

@app.get("/api/runs/latest")
def get_latest_run():
    try:
        client = Garmin(email, password)
        token_dir = "./.garmin_tokens"
        
        # 1. Ensure the directory actually exists
        os.makedirs(token_dir, exist_ok=True)
        
        # 2. Try to login with cached tokens first
        try:
            client.login(token_dir)
        except Exception:
            # 3. If no tokens exist (first run), login normally and save them
            client.login()
            client.garth.dump(token_dir)
            
        # Fetch today's activities (0 is the start index, 1 is the limit)
        activities = client.get_activities(0, 1) 
        
        # Format the data for Enduragotchi
        if activities:
            latest_run = activities[0]
            return {
                "distance": latest_run.get("distance"),
                "duration": latest_run.get("duration"),
                "elevation_gain": latest_run.get("elevationGain")
            }
        return {"error": "No recent runs found"}
        
    except Exception as e:
        return {"error": str(e)}