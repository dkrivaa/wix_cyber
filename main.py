import os

# Access the parameters of the scenario (as entered by user in Wix)
scenario_name = os.environ.get('SCENARIO_NAME')
insurance_price = os.environ.get('INSURANCE_PRICE')
risk_assessment_price = os.environ.get('RISK_ASSESSMENT_PRICE')
soc_price = os.environ.get('SOC_PRICE')
consult_security_products_hours = os.environ.get('CONSULT_SECURITY_PRODUCTS_HOURS')
consult_security_products_price = os.environ.get('CONSULT_SECURITY_PRODUCTS_PRICE')
worker_education_hours = os.environ.get('WORKER_EDUCATION_HOURS')
worker_education_price = os.environ.get('WORKER_EDUCATION_PRICE')
risk_assessment_initial_cost = os.environ.get('RISK_ASSESSMENT_INITIAL_COST')
risk_assessment_monthly_cost = os.environ.get('RISK_ASSESSMENT_MONTHLY_COST')
soc_cost = os.environ.get('SOC_COST')
consult_security_products_cost = os.environ.get('CONSULT_SECURITY_PRODUCTS_COST')
worker_education_cost = os.environ.get('WORKER_EDUCATION_COST')
new_customers = os.environ.get('NEW_CUSTOMERS')
referred_customers = os.environ.get('REFERRED_CUSTOMERS')
lead_customers = os.environ.get('LEAD_CUSTOMERS')
year1 = os.environ.get('YEAR1')
year2 = os.environ.get('YEAR2')
year3 = os.environ.get('YEAR3')
year4 = os.environ.get('YEAR4')
year5 = os.environ.get('YEAR5')
new_commission = os.environ.get('NEW_COMMISSION')
referred_commission = os.environ.get('REFERRED_COMMISSION')
lead_commission = os.environ.get('LEAD_COMMISSION')
existing_commission = os.environ.get('EXISTING_COMMISSION')
new_risk = os.environ.get('NEW_RISK')
referred_risk = os.environ.get('REFERRED_RISK')
lead_risk = os.environ.get('LEAD_RISK')
existing_risk = os.environ.get('EXISTING_RISK')
new_cost = os.environ.get('NEW_COST')
referred_cost = os.environ.get('REFERRED_COST')
lead_cost = os.environ.get('LEAD_COST')





print(f"Scenario Name: {scenario_name}")
print(f"Insurance Price: {insurance_price}")

