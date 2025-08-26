print("[DEBUG] Starting live_sports_mcp.py load...")
from mcp.server.fastmcp import FastMCP
import requests
print("[DEBUG] Imports complete.")

mcp = FastMCP("Live_Sports_Coach")
print("[DEBUG] FastMCP instance created.")

# - here i fetch live game stats ----
@mcp.tool()
def fetch_live_stats(sport: str, game_id: str) -> dict:
    print(f"[DEBUG] fetch_live_stats called with sport={sport}, game_id={game_id}")
    """
    Fetch live stats from a public API (replace with actual API endpoints).
    Returns key stats in a standard format.
    """
    # API call here 
    # response = requests.get(f"https://api.sportsdata.io/{sport}/games/{game_id}/stats", headers={"Ocp-Apim-Subscription-Key": "YOUR_KEY"})
    # stats = response.json()
    
    # ex data
    stats = {
        "home_score": 78,
        "away_score": 74,
        "time_remaining": "02:35",
        "turnovers": 12,
        "shots_made": 32,
        "shots_attempted": 80,
    }
    print("[DEBUG] fetch_live_stats returning stats.")
    return stats

# --  here it predicts win probability ----
@mcp.tool()
def predict_win_probability(stats: dict) -> dict:
    print(f"[DEBUG] predict_win_probability called with stats={stats}")
    """
    Simple predictive model based on score differential and time remaining.
    """
    home_score = stats.get("home_score", 0)
    away_score = stats.get("away_score", 0)
    time_remaining = stats.get("time_remaining", "0:00")
    minutes, seconds = map(int, time_remaining.split(":"))
    total_seconds = minutes * 60 + seconds

    score_diff = home_score - away_score
    print("[DEBUG] predict_win_probability calculated score_diff.")
    # Basic heuristic: closer game late = 50/50, bigger lead = higher probability
    prob = min(max(0.5 + 0.005 * score_diff - 0.0005 * total_seconds, 0), 1)

    return {"home_win_probability": round(prob, 2), "away_win_probability": round(1 - prob, 2)}
    print("[DEBUG] predict_win_probability returning result.")

# - heres the Training / improvement tips ----
@mcp.resource("live_training://{skill}")
def live_training_plan(skill: str) -> str:
    plans = {
        "shooting": "Work on high-pressure free throws and contested 3-point shots.",
        "passing": "Focus on fast break decision-making drills and pick-and-roll passing.",
        "defense": "Practice closing out quickly and blocking/rebounding under fatigue."
    }
    return plans.get(skill.lower(), "No training plan available.")

# ---- prompt is strategy suggestion for current situation ----
@mcp.prompt()
def real_time_strategy(sport: str, stats: dict, situation: str) -> str:
    """
    Suggest the best play based on current stats and game situation.
    """
    return (
        f"As a coach for a {sport} team, analyze the following stats: {stats} "
        f"and current situation: '{situation}'. Recommend an optimal strategy "
        "and explain reasoning in plain language."
    )

if __name__ == "__main__":
    print("[DEBUG] About to call mcp.run()")
    mcp.run()
    print("[DEBUG] mcp.run() returned")
print("[DEBUG] live_sports_mcp.py loaded successfully.")
# This code sets up a FastMCP server for a live sports coaching application.
