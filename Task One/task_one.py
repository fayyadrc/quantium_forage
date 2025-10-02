import pandas as pd

# Task: Process Soul Foods morsel transaction data
# 1. Remove all products besides 'Pink Morsels'
# 2. Create new field called 'Sales' = quantity * price
# 3. Keep date and region fields
# Output columns: Sales, Date, Region

# Read the three CSV files
df1 = pd.read_csv("data/daily_sales_data_0.csv")
df2 = pd.read_csv("data/daily_sales_data_1.csv")
df3 = pd.read_csv("data/daily_sales_data_2.csv")

# Combine all three dataframes
merged_df = pd.concat([df1, df2, df3], ignore_index=True)

# Filter for pink morsels only
pink_df = merged_df[merged_df["product"] == "pink morsel"].copy()

# Clean the price field (remove dollar sign) and convert to float
pink_df["price"] = pink_df["price"].str.replace("$", "").astype(float)

# Calculate sales (quantity * price)
pink_df["Sales"] = pink_df["quantity"] * pink_df["price"]

# Select and rename the required columns
final_df = pink_df[["Sales", "date", "region"]].copy()
final_df.rename(columns={"date": "Date", "region": "Region"}, inplace=True)

# Save the final output
final_df.to_csv("soul_foods_pink_morsel_sales.csv", index=False)




