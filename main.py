import json
import os

import pandas as pd
from io import BytesIO

from scenarioData import get_data


def test():
    data_dict = get_data()
    print(data_dict.insurancePrice)


if __name__ == '__main__':
    test()



