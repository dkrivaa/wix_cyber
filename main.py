import json

import pandas as pd
from io import BytesIO
import subprocess

from scenarioData import get_data


def test():
    data_dict = get_data()
    print(json.dumps(data_dict))


if __name__ == '__main__':
    test()



