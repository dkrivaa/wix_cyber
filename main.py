import pandas as pd
from io import BytesIO

from scenarioData import get_data


def test():
    data_dict = get_data()
    print(data_dict)
    return data_dict

# df = pd.DataFrame([data_dict])
#
# df.to_excel('test.xlsx', index=False)


if __name__ == '__main__':
    test()



