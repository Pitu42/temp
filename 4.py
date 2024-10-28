import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("CaseStudy.csv")

features = ["Departure Week", "Receipt Country", "Receipt Cluster", "Receipt Region", "Delivery Country", "Delivery Cluster", "Delivery Region", "Total Units"]
df = df[features]

corridor_volume = df.groupby(['Receipt Region', 'Delivery Region'])['Total Units'].sum().reset_index()

top_corridor = corridor_volume.loc[corridor_volume['Total Units'].idxmax()]

print("Top Corridor:")
print(top_corridor)
top_corridor_data = df[(df['Receipt Region'] == top_corridor['Receipt Region']) &
                       (df['Delivery Region'] == top_corridor['Delivery Region'])]
print(top_corridor_data)
plt.figure(figsize=(12, 6))
sns.lineplot(data=top_corridor_data, x='Departure Week', y='Total Units', marker='o', ci=None)
sns.regplot(data=top_corridor_data, x='Departure Week', y='Total Units', scatter=False, color='red', label="Trend Line", ci=None)
plt.title(f"Total Units Over Time from {top_corridor['Delivery Region']} to {top_corridor['Receipt Region']}")
plt.xlabel('Departure Week')
plt.ylabel('Total Units (thousens)')
plt.show()

