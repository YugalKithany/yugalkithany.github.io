import pandas as pd

# Load the Excel file and select the correct sheet
df = pd.read_excel("la-liga-2025-UTC.xlsx", sheet_name=0)  # Update sheet_name if needed

# Clean column names
df.columns = df.columns.str.strip()

# Extract relevant columns
fixtures_df = df[["Round Number", "Date", "Home Team", "Away Team"]].copy()
fixtures_df.columns = ["matchday", "date", "home_team", "away_team"]

# Convert date to YYYY-MM-DD format
fixtures_df["date"] = pd.to_datetime(fixtures_df["date"]).dt.strftime("%Y-%m-%d")

# Sort by matchday and date
fixtures_df.sort_values(by=["matchday", "date"], inplace=True)

# Save to CSV
fixtures_df.to_csv("25-26_schedule.csv", index=False)

print("✅ CSV created: laliga_2025_26_schedule.csv")
