import pandas as pd
import json

filepath = r"C:\Users\v.finel\Desktop\stations.json"

# Read the JSON file
with open(filepath, 'r', encoding='utf-8') as f:
	data = json.load(f)

# # Load into a pandas DataFrame
# df = pd.DataFrame(data)


# create dataframe 
# https://stackoverflow.com/questions/13575090/construct-pandas-dataframe-from-items-in-nested-dictionary

data_dict = {(loc,radio['name']): radio['url'] 
                           for loc in data.keys() 
                           for radio in data[loc]['urls']}

# df = pd.DataFrame.from_dict(data_dict, orient='index')

data_list = [(loc,radio['name'],radio['url']) 
                           for loc in data.keys() 
                           for radio in data[loc]['urls']]

df = pd.DataFrame.from_records(data_list, columns=['location','name','url'])
	
# Display the DataFrame
print(f'{df.head()}')

# Example inputs
input_loc = 'Abuja,NG'
input_radio_name = "Cool FM 969" #"ABN Radio"

try:
    line = df[(df['location']==input_loc) & (df['name']==input_radio_name)]
    url = line['url'].values[0]
    print(f'{input_radio_name}, in {input_loc}, url is = {url}')

except KeyError:
    url = None
    print(f'no match for {input_loc=} and {input_radio_name=}')


print('exiting ')