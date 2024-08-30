import pandas as pd

from scenarioData import get_data

data_dict = get_data()
print(data_dict)

df = pd.DataFrame(data_dict)

print('made dataframe', df)






