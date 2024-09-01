import json
import os

import pandas as pd
from io import BytesIO
import subprocess

from scenarioData import get_data


def test():
    data_dict = get_data()
    github_token = os.getenv('ACCESS_TOKEN')
    print(github_token[:5])
    print(json.dumps(data_dict))


if __name__ == '__main__':
    test()



