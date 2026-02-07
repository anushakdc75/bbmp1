import pandas as pd

rows = [
    {"text": "garbage not cleared in ward 12", "category": "Garbage", "solution": "Use BBMP Sahaaya and attach photo", "department": "Solid Waste Management", "location": "Ward 12", "resolved_status": "yes"},
    {"text": "water supply issue", "category": "Water", "solution": "Register BWSSB complaint and check valve timing", "department": "BWSSB", "location": "Ward 12", "resolved_status": "yes"},
    {"text": "pothole near school", "category": "Road", "solution": "Roads wing inspection and pothole filling", "department": "BBMP Roads", "location": "Ward 18", "resolved_status": "no"},
]
pd.DataFrame(rows).to_csv("../data/bbmp_reddit_data.csv", index=False)
print("created ../data/bbmp_reddit_data.csv")
