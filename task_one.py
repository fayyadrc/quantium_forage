import pandas as pd

#remove all products besides 'Pink Morsels'
#create new field called Total Sales = quantity*price
#keep date field
#filter by region later
#product,price,quantity,date,region
df1 = pd.read_csv("daily_sales_data_0.csv")
df2 = pd.read_csv("daily_sales_data_1.csv")
df3 = pd.read_csv("daily_sales_data_2.csv")


merged_df = pd.concat([df1, df2, df3], ignore_index=True)
merged_df.to_csv("merged_sales_data.csv", index=False)

#df_merged = pd.read_csv("merged_sales_data.csv")
filtered_df = merged_df[merged_df["product"]=="pink morsel"]
filtered_df.to_csv("filtered_sales_csv",index=False)



