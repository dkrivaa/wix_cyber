import os

# Access the parameters
scenario_name = os.environ.get('SCENARIO_NAME')
insurance_price = os.environ.get('INSURANCE_PRICE')

print(f"Scenario Name: {scenario_name}")
print(f"Insurance Price: {insurance_price}")

