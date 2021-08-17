from jsonreader import JsonReader, file_path_extractor
from ratetracker import ExchangeRatesData, alert_generator
import sys


def main(arguments: list) -> None:
    try:
        file_path = file_path_extractor(arguments)
        reader = JsonReader(file_path)
        alert_callback = alert_generator
        tracker = ExchangeRatesData([alert_callback])
        for line in reader:
            tracker.update(line)

    except Exception as e:
        sys.exit(e)


if __name__ == "__main__":
    main(sys.argv)
