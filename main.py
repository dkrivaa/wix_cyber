import json
import os
import subprocess
import pandas as pd
from io import BytesIO
import requests
import time


from scenarioData import get_data
from simulation import run_simulation


def test():
    data_dict = get_data()

    results = run_simulation(data_dict)

    df = pd.DataFrame(results, columns=[
        'month', 'customers', 'new customers', 'referred customers', 'lead customers',
        'existing customers', 'Risk assessment pakages sold', 'Risk assessment pakages sold to new customers',
        'Risk assessment pakages sold to referred customers', 'Risk assessment pakages sold to lead customers',
        'Risk assessment pakages sold to existing customers', 'SOC pakages sold',
        'SOC pakages sold to new customers', 'SOC pakages sold to referred customers',
        'SOC pakages sold to lead customers', 'SOC pakages sold to existing customers', 'Insurance packages sold',
        'Insurance packages sold to new customers', 'Insurance packages sold to referred customers',
        'Insurance packages sold to lead customers', 'Insurance packages sold to existing customers',
        'Income from risk assessment packages', 'Income from SOC packages', 'Income from insurance packages',
        'Total income', 'Admin staff', 'Tele staff', 'Sales staff', 'Cyber staff', 'Logistics staff',
        'Total staff', 'Labor cost', 'Risk assessment packages cost', 'SOC packages cost', 'Marketing cost',
        'General overhead', 'Legal & Accounting cost', 'Total cost', 'Gross profit',
    ])

    df = df.T
    df = df.reset_index()
    df.to_excel('test.xlsx', index=False, header=False)

    # Add the Excel file to the Git staging area
    subprocess.run(['git', 'add', 'test.xlsx'], check=True)

    # Commit the Excel file with a message
    commit_message = 'Add Excel file generated by GitHub Actions workflow'
    subprocess.run(['git', 'commit', '-m', commit_message], check=True)

    # Push the changes back to the repository
    subprocess.run(['git', 'push'], check=True)

    time.sleep(30)


if __name__ == '__main__':
    test()



