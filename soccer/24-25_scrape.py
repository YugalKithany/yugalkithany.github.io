import pandas as pd

# Load the fourth sheet (sheet index starts at 0, so 3 = 4th sheet)
xl_file = pd.ExcelFile("La_Liga_Interactive_Table_2024-25_NM_20250526.xlsx")
df = xl_file.parse(sheet_name=4)

# Preview actual column names to verify structure
print(df.columns.tolist())

# Extract columns by position (if names are messy or missing)
df_cleaned = df.iloc[:, [0, 1, 9, 12]].copy()  # A = 0, J = 9, M = 12
df_cleaned.columns = ["matchday", "date", "home_team", "away_team"]

# Optional: clean up matchday formatting (e.g., remove headers or NaNs)
df_cleaned = df_cleaned[df_cleaned["matchday"].apply(lambda x: str(x).isdigit())]

# Add placeholder date if needed (customize later if actual dates are available)
# df_cleaned["date"] = "2024-08-15"  # Replace or update as needed

# Reorder columns
final_df = df_cleaned[["matchday", "date", "home_team", "away_team"]]

# Save to CSV
final_df.to_csv("laliga_2024_25_schedule.csv", index=False)

print("✅ Fixture CSV saved as laliga_2024_25_schedule.csv")
