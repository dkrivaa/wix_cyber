import pandas as pd
from io import BytesIO
import subprocess

from scenarioData import get_data


def test():
    data_dict = get_data()
    df = pd.DataFrame([data_dict])
    df.to_excel('myfile.xlsx', index=False)


if __name__ == '__main__':
    test()



