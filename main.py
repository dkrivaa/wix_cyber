import pandas as pd
from io import BytesIO
import subprocess

from scenarioData import get_data


def test():
    data_dict = get_data()
    df = pd.DataFrame([data_dict])
    df.to_excel('myfile.xlsx', index=False)

    # Add the file to the staging area
    subprocess.run(['git', 'add', 'myfile.xlsx'], check=True)

    # Commit the file
    subprocess.run(['git', 'commit', '-m', 'Add myfile.xlsx'], check=True)

    # Push the changes to the repository
    subprocess.run(['git', 'push'], check=True)


if __name__ == '__main__':
    test()



# df = pd.DataFrame([data_dict])
#
# df.to_excel('test.xlsx', index=False)
