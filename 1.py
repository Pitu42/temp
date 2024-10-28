import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# read csv
df = pd.read_csv("CaseStudy.csv")

# delete first and last week -> incomplete data
df = df[(df["Departure Week"] > df["Departure Week"].min()) & (df["Departure Week"] < df["Departure Week"].max())]

#Tabular information over volumen over week
units_per_week = df.groupby("Departure Week", group_keys=True)[["Total Units", "Full TEU", "Total MTs", "Sum of LiveReeferUnits"]].sum()
units_per_week.to_excel("1.xlsx")
print(units_per_week)

# plot
plt.figure(figsize=(12, 6))
sns.lineplot(x='Departure Week', y='Total Units', data=units_per_week)
plt.title('Total Units Over Time')
plt.xlabel('Departure Week')
plt.ylabel('Total Units')
plt.show()
