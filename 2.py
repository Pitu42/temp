import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# read csv
df = pd.read_csv("CaseStudy.csv")

# delete first and last week -> incomplete data
df = df[(df["Departure Week"] > df["Departure Week"].min()) & (df["Departure Week"] < df["Departure Week"].max())]

#2 - dds -> Ports with declined volumen

# Group by and calculate the total units
grouped_df = df.groupby(["Receipt City", "Delivery City", "Departure Week"], as_index=False)["Total Units"].sum()

# Calculate the difference between the last week and the first week
grouped_df['Diff'] = grouped_df.groupby(['Receipt City', 'Delivery City'])['Total Units'].transform(lambda x: x.iloc[-1] - x.iloc[0])

# Filter for negative differences
grouped_diff = grouped_df[grouped_df["Diff"] < 0]
declined_shipment = grouped_diff[['Receipt City', 'Delivery City', "Diff"]].drop_duplicates().sort_values("Diff")
dss = declined_shipment.head(400) # declined shipment sample
print(declined_shipment)
print(dss)
dss.to_excel("2.xlsx")
