from src.main.jsonreader import file_path_extractor, JsonReader
from typing import Iterable
import pytest


def test_jsonreader():
    reader = JsonReader("example/input1.jsonl")
    assert reader.file_path == "example/input1.jsonl"


def test_files_path_extractor():
    assert file_path_extractor(
        ["main.py", "test_file.jsonl"]) == "test_file.jsonl"
    assert file_path_extractor(
        ["main.py", "test_file.jsonl", "test_file2.jsonl"]) \
        == "test_file.jsonl"


def test_no_path_to_file():
    with pytest.raises(Exception) as exp:
        file_path_extractor(["main.py"])
    assert str(exp.value) == "No valid path was provided"


def test_wrong_type_arguments():
    with pytest.raises(Exception) as exp:
        file_path_extractor("test")
    assert str(
        exp.value) == "A list of arguements was expected. Got <class 'str'> instead."


def test_file_not_existent():
    with pytest.raises(Exception) as exp:
        reader = JsonReader("random_name.jsonl")
        for line in reader:
            pass
    assert str(exp.value) == 'The file "random_name.jsonl" does not exist.'


def test_not_valid_json_file():
    with pytest.raises(ValueError) as exp:
        reader = JsonReader("example/input4.jsonl")
        for line in reader:
            pass
    assert str(exp.value) == 'Not a valid json file.: line 1 column 1 (char 0)'


def test_corrupted_json_file():
    with pytest.raises(ValueError) as exp:
        reader = JsonReader("example/input5.jsonl")
        for line in reader:
            pass
    assert str(exp.value) == 'Not a valid json file.: line 1 column 74 (char 73)'


def test_iterable():
    reader = JsonReader("random_name.jsonl")
    assert isinstance(reader, Iterable)


def test_valid_file():
    reader = JsonReader("example/input1.jsonl")
    _ = [line for line in reader]
