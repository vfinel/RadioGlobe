import argparse
import datetime
import os
import sys

import pandas as pd

sys.path.append(".")
from get_radio_url import load_database


stations_log = "logs/stations_log.csv"  # "actual" log
stations_listened = "logs/stations_listened.csv"  # for stats (no duplicates)
columns_listened = ["name", "location", "latitude", "longitude", "count", "url", "date"]
encoding = "utf-8"


def log_radio(location: str, latitude: str, longitude: str, station: str, url: str):
    """log current radio to the station log file"""
    now = datetime.datetime.now()

    # create file if it does not exist yet
    if not os.path.isfile(stations_log):
        with open(stations_log, "w", encoding=encoding) as f:
            f.write("radio, location, latitude, longitude, date, url\n")

    # log radio to log file
    with open(stations_log, "a", encoding=encoding) as f:
        f.write(f"{station}, {location}, {latitude}, {longitude}, {now}, {url} \n")

    # add statistics to stats file
    try:
        stats = pd.read_csv(stations_listened, dtype={"date": str})
        stats.fillna({"date": ""}, inplace=True)

    except (FileNotFoundError, pd.errors.EmptyDataError):
        stats = pd.DataFrame(columns=columns_listened)

    index_in_stats = stats[
        (stats["name"] == station) & (stats["location"] == location)
    ].index
    if len(index_in_stats) == 0:  # congrats, new station !
        new_row = pd.DataFrame(
            {
                "name": station,
                "location": location,
                "latitude": latitude,
                "longitude": longitude,
                "count": 1,
                "url": url,
                "date": now,
            },
            index=[0],
        )
        stats = pd.concat([stats, new_row], ignore_index=True)

    else:
        index = index_in_stats[0]  # assuming unique
        stats.at[index, "count"] += 1
        stats.loc[index, "date"] += f", {now}"

    stats.to_csv(stations_listened, index=False, columns=columns_listened)


def log_radio_test(
    location: str, latitude: str, longitude: str, station: str, url: str
):
    """write something in the file, then read back and display content"""

    log_radio(
        location=location,
        latitude=latitude,
        longitude=longitude,
        station=station,
        url=url,
    )

    with open(stations_log, encoding=encoding) as f:
        data = f.read()

    print(f"contents of {stations_log}: \n{data}")


def reset_file():
    with open(stations_log, "w", encoding=encoding) as f:
        f.write("radio, location, latitude, longitude, date, url\n")

    stats = pd.DataFrame(columns=columns_listened)
    stats.to_csv(stations_listened, index=False, columns=columns_listened)


def make_listening_stats():
    db = load_database("stations.json")
    stats = pd.read_csv(stations_listened)

    # remove radios that can be streamed from several locations
    db.drop_duplicates(subset="url", inplace=True)

    ratio = stats.shape[0] / db.shape[0]

    print(f"There are (at least) {db.shape[0]} stations in the world")
    print(f"you listened to {stats.shape[0]} stations...")
    print(f"that is {100 * ratio:.2f}% of the world's radios !")


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r",
        "--reset",
        action=argparse.BooleanOptionalAction,
        help="reset stations log file",
    )

    parser.add_argument(
        "-s",
        "--stats",
        action=argparse.BooleanOptionalAction,
        help="compute your listening stats",
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if args.reset:
        print(
            f"are you sure you want to reset {stations_log} ? There is no coming back !! [y/N]"
        )
        ans = input()
        if ans.lower() == "y":
            reset_file()
            print(f"{stations_log} has been reset.")

        else:
            print("Aborting.")

    elif args.stats:
        make_listening_stats()

    else:  # simple test
        log_radio_test(
            location="Marseille, FR",
            latitude=42,
            longitude=-42,
            station="radiojul 113.13 FM",
            url="radio.com",
        )


if __name__ == "__main__":
    main()
