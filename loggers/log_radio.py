import argparse 
import datetime 
import json
import pandas as pd 


stations_log = "logs/stations_log.csv"  # "actual" log
stations_listened = "logs/stations_listened.csv"  # for stats (no duplicates)
encoding = "utf-8"


def log_radio(location: str, latitude: str, longitude: str, station: str, url: str):
    """ log current radio to the station log file """
    now = datetime.datetime.now()

    # log radio to log file 
    with open(stations_log, 'a', encoding=encoding) as f:
        f.write(f"{station}, {location}, {latitude}, {longitude}, {now}, {url} \n")

    # add statistics to stats file 
    columns = ["name", "location", "latitude", "longitude", "date", "count", "url"]
    try:
        stats = pd.read_csv(stations_listened, dtype={'date': str})
        stats.fillna({"date": ""}, inplace=True)

    except (FileNotFoundError, pd.errors.EmptyDataError):
        stats = pd.DataFrame(columns=columns)
    
    index_in_stats = stats[(stats['name'] == station) & (stats['location']==location)].index
    if len(index_in_stats)==0:  # congrats, new station !
        new_row = pd.DataFrame.from_dict({"name": station, "location": location,"latitude": latitude, "longitude":longitude,"date":now,"count":1,"url": url})
        stats = pd.concat([stats, new_row], ignore_index=True)

    else:
        index = index_in_stats[0]  # assuming unique
        stats.at[index, 'count'] += 1
        stats.loc[index, 'date'] += f", {now}"

    stats.to_csv(stations_listened, index=False, columns=columns)


def log_radio_test(location: str, latitude: str, longitude: str, station: str, url: str):
    """ write something in the file, then read back and display content """

    log_radio(location=location, 
            latitude=latitude, 
            longitude=longitude,
            station=station, 
            url=url,
            )
    
    with open(stations_log, encoding=encoding) as f:
        data = f.read()
    
    print(f"contents of {stations_log}: \n{data}")


def reset_file():
    with open(stations_log, 'w', encoding=encoding) as f:
        f.write("radio, location, latitude, longitude, date, url\n")


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r",
        "--reset",
        action=argparse.BooleanOptionalAction,
        help="reset stations log file",
    )
    args = parser.parse_args()
    return args 


def main(): 
    args = parse_args()

    if args.reset:
        print(f"are you sure you want to reset {stations_log} ? There is no coming back !! [y/N]")
        ans = input()
        if ans.lower()=='y':
            reset_file()
            print(f"{stations_log} has been reset.")

        else:
            print('Aborting.')

    else: # simple test 
        log_radio_test(location="Marseille, FR", latitude=42, longitude=-42, station="radiojul 113.13 FM", url="radio.com")


if __name__ == "__main__": 
    main()