import pandas as pd
import json

# Load the stations JSON data
# json_path = r"C:\Users\v.finel\Desktop\stations.json"
json_path = r"stations.json"
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Flatten JSON into a DataFrame for lookup
data_list = [(loc, radio['name'], radio['url'])
             for loc in data.keys()
             for radio in data[loc]['urls']]

stations_df = pd.DataFrame.from_records(data_list, columns=['location', 'name', 'url'])
print('stations: \n{stations_df.head()}')

# Load the CSV file
csv_path = 'get_radio_url.csv'
csv_df = pd.read_csv(csv_path)

# # Clean up whitespace in column names and values
# csv_df.columns = [col.strip() for col in csv_df.columns]
# csv_df['location'] = csv_df['location'].str.strip()
# csv_df['name'] = csv_df['name'].str.strip()

print(csv_df.head())

# Fill missing URLs
for idx, row in csv_df.iterrows():
    if pd.isna(row['url']) or not str(row['url']).strip():
        # Try to find a match in the stations DataFrame
        # print(f"looking for '{row['name']}' in '{row['location']}'")
        query_loc = row['location'].lower().replace(' ', '')
        query_name = row['name'].lower()
        match = stations_df[(stations_df['name'].str.lower() == query_name) & (stations_df['name'].str.lower() == query_name)]
        # print(match)
        if not match.empty:
            csv_df.at[idx, 'url'] = match.iloc[0]['url']
            print(f"Filled URL for {row['name']} in {row['location']}")

# Write the completed data back to the CSV file
csv_df.to_csv(csv_path, index=False)
print('Completed missing URLs and updated get_radio_url.csv')