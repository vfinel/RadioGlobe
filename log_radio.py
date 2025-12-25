import argparse 
import datetime 

filename = "stations_log.csv"
encoding = "utf-8"


def log_radio(location: str, latitude: str, longitude: str, station: str, url: str):
    """ log current radio to the station log file """
    now = datetime.datetime.now()
    with open(filename, 'a', encoding=encoding) as f:
        f.write(f"{station}, {location}, {latitude}, {longitude}, {now}, {url} \n")


def log_radio_test(location: str, latitude: str, longitude: str, station: str, url: str):
    """ write something in the file, then read back and display content """

    log_radio(location=location, 
            latitude=latitude, 
            longitude=longitude,
            station=station, 
            url=url,
            )
    
    with open(filename, encoding=encoding) as f:
        data = f.read()
    
    print(data)


def reset_file():
    with open(filename, 'w', encoding=encoding) as f:
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
        print(f"are you sure you want to reset {filename} ? There is no coming back !! [y/N]")
        ans = input()
        if ans.lower()=='y':
            reset_file()
            print(f"{filename} has been reset.")

        else:
            print('Aborting.')

    else: # simple test 
        log_radio_test(location="Marseille", latitude=42, longitude=-42, station="radiojul 113.13 FM", url="radio.com")


if __name__ == "__main__": 
    main()