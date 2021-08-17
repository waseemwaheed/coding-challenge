import json


def file_path_extractor(arguments: list) -> str:
    """Extracts the json file path from command line arguments 

    Arguments
    ----------
    arguments : list
        list of arguments passed to main.py in command line

    Raises
    ------
    TypeError
        if the wrong type of arguments was passed
    FileNotFoundError
        if no valid path was provided
    """

    if not isinstance(arguments, list):
        raise TypeError(
            f"A list of arguements was expected. Got {type(arguments)} instead.")

    if len(arguments) < 2:
        raise FileNotFoundError("No valid path was provided")

    return arguments[1]


class JsonReader:
    """
    A class that reading json files line by line

    ...

    Parameters
    ----------
    file_path : str
        path to json file to be read
    """

    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def __iter__(self) -> dict:
        try:
            with open(self.file_path) as json_file:
                for json_line in json_file:
                    yield json.loads(json_line)

        except FileNotFoundError:
            raise FileNotFoundError(
                f'The file "{self.file_path}" does not exist.')

        except json.decoder.JSONDecodeError as exp:
            raise json.JSONDecodeError(
                "Not a valid json file.", self.file_path, exp.pos)
