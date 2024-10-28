import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("CaseStudy.csv")
features = ["Departure Week", "Receipt Country", "Receipt Cluster", "Receipt Region", "Delivery Country", "Delivery Cluster", "Delivery Region", "Total Units"]
df = df[features]

unique_regions = df['Receipt Region'].unique()

for region in unique_regions:
    df_region = df[df["Receipt Region"] == region]
    plt.figure(figsize=(12, 6))

    sns.lineplot(data=df_region, x='Departure Week', y='Total Units', hue="Delivery Region", marker='o', ci=None)


    for delivery_region in df_region['Delivery Region'].unique():
        df_region_delivery = df_region[df_region['Delivery Region'] == delivery_region]

    plt.title(f"Total Units Over Time from {region}")
    plt.xlabel('Departure Week')
    plt.ylabel('Total Units (thousands)')
    plt.legend(title='Delivery Region', bbox_to_anchor=(0, 0.5), loc='upper left')
    plt.savefig(f'{region}TC.png')
    plt.show()

