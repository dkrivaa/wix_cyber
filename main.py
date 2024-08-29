import os
import json

json_vars = os.getenv('JSON_VARS')
vars_dict = json.loads(json_vars)  # Decode JSON string into a dictionary

print(vars_dict)

scenario_name = vars_dict.get('scenarioName')
insurance_price = vars_dict.get('insurancePrice')
risk_assessment_price = vars_dict.get('riskAssessmentPrice')
soc_price = vars_dict.get('socPrice')
consult_security_products_hours = vars_dict.get('consultSecurityProductsHours')
consult_security_products_price = vars_dict.get('consultSecurityProductsPrice')
worker_education_hours = vars_dict.get('workerEducationHours')
worker_education_price = vars_dict.get('workerEducationPrice')
risk_assessment_initial_cost = vars_dict.get('riskAssessmentInitialCost')
risk_assessment_monthly_cost = vars_dict.get('riskAssessmentMonthlyCost')
soc_cost = vars_dict.get('socCost')
consult_security_products_cost = vars_dict.get('consultSecurityProductsCost')
worker_education_cost = vars_dict.get('workerEducationCost')
new_customers = vars_dict.get('newCustomers')
referred_customers = vars_dict.get('referredCustomers')
lead_customers = vars_dict.get('leadCustomers')
year1 = vars_dict.get('year1')
year2 = vars_dict.get('year2')
year3 = vars_dict.get('year3')
year4 = vars_dict.get('year4')
year5 = vars_dict.get('year5')
new_commission = vars_dict.get('newCommission')
referred_commission = vars_dict.get('referredCommission')
lead_commission = vars_dict.get('leadCommission')
existing_commission = vars_dict.get('existingCommission')
new_risk = vars_dict.get('newRisk')
referred_risk = vars_dict.get('referredRisk')
lead_risk = vars_dict.get('leadRisk')
existing_risk = vars_dict.get('existingRisk')
new_cost = vars_dict.get('newCost')
referred_cost = vars_dict.get('referredCost')
lead_cost = vars_dict.get('leadCost')

print('scenario name: ', scenario_name)
print('insurance price: ', insurance_price)

# Access the parameters of the scenario (as entered by user in Wix)
# scenario_name = os.environ.get('SCENARIO_NAME')
# insurance_price = os.environ.get('INSURANCE_PRICE')
# risk_assessment_price = os.environ.get('RISK_ASSESSMENT_PRICE')
# soc_price = os.environ.get('SOC_PRICE')
# consult_security_products_hours = os.environ.get('CONSULT_SECURITY_PRODUCTS_HOURS')
# consult_security_products_price = os.environ.get('CONSULT_SECURITY_PRODUCTS_PRICE')
# worker_education_hours = os.environ.get('WORKER_EDUCATION_HOURS')
# worker_education_price = os.environ.get('WORKER_EDUCATION_PRICE')
# risk_assessment_initial_cost = os.environ.get('RISK_ASSESSMENT_INITIAL_COST')
# risk_assessment_monthly_cost = os.environ.get('RISK_ASSESSMENT_MONTHLY_COST')
# soc_cost = os.environ.get('SOC_COST')
# consult_security_products_cost = os.environ.get('CONSULT_SECURITY_PRODUCTS_COST')
# worker_education_cost = os.environ.get('WORKER_EDUCATION_COST')
# new_customers = os.environ.get('NEW_CUSTOMERS')
# referred_customers = os.environ.get('REFERRED_CUSTOMERS')
# lead_customers = os.environ.get('LEAD_CUSTOMERS')
# year1 = os.environ.get('YEAR1')
# year2 = os.environ.get('YEAR2')
# year3 = os.environ.get('YEAR3')
# year4 = os.environ.get('YEAR4')
# year5 = os.environ.get('YEAR5')
# new_commission = os.environ.get('NEW_COMMISSION')
# referred_commission = os.environ.get('REFERRED_COMMISSION')
# lead_commission = os.environ.get('LEAD_COMMISSION')
# existing_commission = os.environ.get('EXISTING_COMMISSION')
# new_risk = os.environ.get('NEW_RISK')
# referred_risk = os.environ.get('REFERRED_RISK')
# lead_risk = os.environ.get('LEAD_RISK')
# existing_risk = os.environ.get('EXISTING_RISK')
# new_cost = os.environ.get('NEW_COST')
# referred_cost = os.environ.get('REFERRED_COST')
# lead_cost = os.environ.get('LEAD_COST')
#






