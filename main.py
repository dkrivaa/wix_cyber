import pandas as pd
from io import BytesIO
import subprocess

from scenarioData import get_data


def test():
    data_dict = get_data()
    print('this is the result: ', data_dict)


if __name__ == '__main__':
    test()



