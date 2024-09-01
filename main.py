import json
import os

import pandas as pd
from io import BytesIO

from scenarioData import get_data


def test():
    data_dict = get_data()
    access_token = os.getenv('ACCESS_TOKEN')
    print(access_token[0:5])
    print(json.dumps(data_dict))


if __name__ == '__main__':
    test()



