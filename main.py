from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Railway Saathi API", version="1.0.0")

# Allow frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Train data ----
trains = [
    {"train_no":"12561","name":"Swatantrata Senani Express","source":"Patna","destination":"Delhi","departure":"06:15","arrival":"22:30","duration_hrs":16.25,"sleeper_fare":380,"days_run":"Mon Wed Fri Sun"},
    {"train_no":"12310","name":"Patna Rajdhani Express","source":"Patna","destination":"Delhi","departure":"18:05","arrival":"08:35","duration_hrs":14.5,"sleeper_fare":550,"days_run":"Daily"},
    {"train_no":"12566","name":"Bihar Sampark Kranti","source":"Patna","destination":"Delhi","departure":"11:30","arrival":"05:15","duration_hrs":17.75,"sleeper_fare":420,"days_run":"Tue Thu Sat"},
    {"train_no":"13414","name":"Farakka Express","source":"Patna","destination":"Delhi","departure":"14:45","arrival":"10:20","duration_hrs":19.5,"sleeper_fare":355,"days_run":"Daily"},
    {"train_no":"12141","name":"Mumbai LTT Express","source":"Patna","destination":"Mumbai","departure":"08:00","arrival":"08:30","duration_hrs":24.5,"sleeper_fare":490,"days_run":"Mon Thu"},
]

# ---- Logic ----
def predict_waitlist(waitlist_number: int, days_until_travel: int):
    if waitlist_number <= 20 and days_until_travel >= 10:
        return "Safe to book — waitlist likely to clear"
    elif waitlist_number <= 40 and days_until_travel >= 7:
        return "Risky — check again in 2-3 days"
    elif waitlist_number <= 60 and days_until_travel >= 14:
        return "Maybe — high waitlist but travel is far away"
    else:
        return "Avoid — waitlist too high, book alternate train"

# ---- API Endpoints ----
@app.get("/")
def home():
    return {"message": "Railway Saathi API is running! 🚂", "version": "1.0.0"}

@app.get("/search")
def search_trains(source: str, destination: str):
    matching = [
        t for t in trains
        if t["source"].lower() == source.lower()
        and t["destination"].lower() == destination.lower()
    ]

    matching.sort(key=lambda t: t["sleeper_fare"])

    if not matching:
        return {"found": False, "trains": [], "message": "No trains found for this route"}

    savings = matching[-1]["sleeper_fare"] - matching[0]["sleeper_fare"] if len(matching) > 1 else 0

    return {
        "found": True,
        "count": len(matching),
        "route": f"{source} → {destination}",
        "savings_vs_expensive": savings,
        "trains": matching
    }

@app.get("/waitlist")
def check_waitlist(waitlist_number: int, days_until_travel: int):
    prediction = predict_waitlist(waitlist_number, days_until_travel)
    return {
        "waitlist_number": waitlist_number,
        "days_until_travel": days_until_travel,
        "prediction": prediction
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Railway Saathi"}