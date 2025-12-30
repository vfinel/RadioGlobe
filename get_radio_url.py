from difflib import get_close_matches
import json
import pandas as pd
import traceback


def load_database(json_path: str) -> pd.DataFrame:
    """ Load the stations JSON data and return a pandas dataframe """

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Flatten JSON into a DataFrame 
    data_list = [(loc, radio['name'], radio['url'])
                for loc in data.keys()
                for radio in data[loc]['urls']]

    df = pd.DataFrame.from_records(data_list, columns=['location', 'name', 'url'])
    print(f"dataframe has columns: {df.columns}")
    print(f'stations database: \n{df.tail()}\n')
    return df 


def fill_missing_url_from_file(csv_path: str, database: pd.DataFrame):
    # Load the CSV file
    print('reading csv file')
    try:
        radios_to_find = pd.read_csv(csv_path)
    
    except Exception:
        error_msg = traceback.format_exc() 
        print(error_msg)
        if "pandas.errors.ParserError: Error tokenizing data" in error_msg:
            print("Unable to parse CSV file, please check that there is no extra spaces between fields.\n")
        
        exit()

    # # Clean up whitespace in column names and values
    # radios_to_find.columns = [col.strip() for col in radios_to_find.columns]
    # radios_to_find['location'] = radios_to_find['location'].str.strip()
    # radios_to_find['name'] = radios_to_find['name'].str.strip()

    print(f"\nradios to find: \n{radios_to_find.head()}")

    # find missing URLs 
    for idx, radio in radios_to_find.iterrows():
        if pd.isna(radio['url']) or not str(radio['url']).strip():
            match = find_radio_in_database(radio, database)
            if not match.empty:
                radios_to_find.at[idx, 'url'] = match.iloc[0]['url']

    # update csv file
    radios_to_find.to_csv(csv_path, index=False)
    print(f'\nupdated {csv_path}.')


def find_radio_in_database(radio: dict, database: pd.DataFrame):
    """ (Try to) find a match in the stations DataFrame """
    print(f"\nlooking for '{radio['name']}' in '{radio['location']}'")
    query_loc = radio['location'].lower().replace(' ', '')
    query_name = radio['name'].lower()
    match = database[(database['name'].str.lower() == query_name) & (database['name'].str.lower() == query_name)]
    if match.empty:
        print(f"\tunable to find radio")
        find_closest_matches(radio, database)

    else: 
        print('\tradio found !')

    return match


def find_closest_matches(radio: dict, database: pd.DataFrame):
    # TODO: loop / search only if name/location is not found as is 
    # clean names (because some contains floats)
    database_names = [str(name) for name in database['name']]
    close_names = set(get_close_matches(radio['name'], database_names))
    close_locations = set(get_close_matches(radio['name'], database['location']))
    print(f"\t{close_names=}")
    print(f"\t{close_locations=}")
    

def main():
    # database_path = r"C:\Users\v.finel\Desktop\stations.json"
    database_path = r"stations.json"
    csv_path = 'logs/favourite_globe_radios.csv'
    database = load_database(database_path)
    fill_missing_url_from_file(csv_path, database)
    

if __name__=='__main__': 
    main()