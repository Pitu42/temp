import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("CaseStudy.csv")
print(df.info())

df = df[(df["Departure Week"] > df["Departure Week"].min()) & (df["Departure Week"] < df["Departure Week"].max())]


grouped_df = df.groupby(["Receipt City", "Delivery City", "Departure Week"], as_index=False)["Total Units"].sum()

grouped_df['Diff'] = grouped_df.groupby(['Receipt City', 'Delivery City'])['Total Units'].transform(lambda x: x.iloc[-1] - x.iloc[0])

grouped_diff = grouped_df[grouped_df["Diff"] < 0]
declined_shipment = grouped_diff[['Receipt City', 'Delivery City', "Diff"]].drop_duplicates().sort_values("Diff")
dss = declined_shipment.head(400) # declined shipment sample

# Merge with the main DataFrame
df_dss = df.merge(dss, on=["Receipt City", "Delivery City"], how="inner")

# Analyze value counts and ratios
features_to_compare = ["Receipt Country", "Receipt Cluster", "Receipt Region", "Delivery Country", "Delivery Cluster", "Delivery Region"]
for column in features_to_compare:
    counts_df = df[column].value_counts()
    counts_df_dss = df_dss[column].value_counts()
    counts_df_dss = counts_df_dss.reindex(counts_df.index, fill_value=0)
    ratio = (counts_df_dss / counts_df).dropna().sort_values(ascending=False)
    print(f"Ratios for column {column}:")
    print(ratio)
    print("\n")

# Group by and calculate total units for Delivery Region and Delivery Cluster
region_cluster_sum = df.groupby(['Departure Week', 'Delivery Region', 'Delivery Cluster'])['Total Units'].sum().reset_index()
total_per_region = df.groupby(['Departure Week', 'Delivery Region'])['Total Units'].sum().reset_index()

# Merge the dataframes to get total units per region into the region_cluster_sum
region_cluster_sum = region_cluster_sum.merge(total_per_region, on=['Departure Week', 'Delivery Region'], suffixes=('', '_Total'))

# Calculate the proportion of each cluster within the region
region_cluster_sum['Proportion'] = region_cluster_sum['Total Units'] / region_cluster_sum['Total Units_Total']

# Get unique Delivery Regions
unique_regions = region_cluster_sum['Delivery Region'].unique()

for region in unique_regions:
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=region_cluster_sum[region_cluster_sum['Delivery Region'] == region], x='Departure Week', y='Proportion', hue='Delivery Cluster', marker='o')
    plt.title(f'Composition of Clusters within {region} Over Time')
    plt.xlabel('Departure Week')
    plt.ylabel('Proportion of Total Units')
    plt.legend(title='Delivery Cluster', bbox_to_anchor=(0, 0.5), loc='upper left')
    plt.savefig(f'{region}RC.png')
    plt.show()



cluster_country_sum = df.groupby(['Departure Week', 'Delivery Cluster', 'Delivery Country'])['Total Units'].sum().reset_index()


total_per_cluster = df.groupby(['Departure Week', 'Delivery Cluster'])['Total Units'].sum().reset_index()


cluster_country_sum = cluster_country_sum.merge(total_per_cluster, on=['Departure Week', 'Delivery Cluster'], suffixes=('', '_Total'))


cluster_country_sum['Proportion'] = cluster_country_sum['Total Units'] / cluster_country_sum['Total Units_Total']


unique_clusters = cluster_country_sum['Delivery Cluster'].unique()

# Cluster inside region
for cluster in unique_clusters:
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=cluster_country_sum[cluster_country_sum['Delivery Cluster'] == cluster], x='Departure Week', y='Proportion', hue='Delivery Country', marker='o')
    plt.title(f'Composition of Countries within {cluster} Over Time')
    plt.xlabel('Departure Week')
    plt.ylabel('Proportion of Total Units')
    plt.legend(title='Delivery Country', bbox_to_anchor=(0, 0.5), loc='center left')
    plt.savefig(f'{cluster}CC.png')
    plt.show()
