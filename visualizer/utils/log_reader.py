import os
from pathlib import Path
import game.config as gc
import json


# Takes the logs and puts them in a dictionary
def logs_to_dict(log_dir: str | None) -> dict:
    """
    Takes the given log directory and puts them into a dictionary.
    :param log_dir:
    :return: dict
    """
    temp: dict = {}
    for file in Path(gc.LOGS_DIR if log_dir is None else log_dir).glob('*.json'):
        with open(file, 'r') as f:
            temp[file.stem] = json.load(f)
    return temp
