import os
import json

json_vars = os.getenv('JSON_VARS')
data_dict = json.loads(json_vars)  # Decode JSON string into a dictionary

print(data_dict)

scenario_name = data_dict.get('scenarioName')
insurance_price = data_dict.get('insurancePrice')
risk_assessment_price = data_dict.get('riskAssessmentPrice')
soc_price = data_dict.get('socPrice')
consult_security_products_hours = data_dict.get('consultSecurityProductsHours')
consult_security_products_price = data_dict.get('consultSecurityProductsPrice')
worker_education_hours = data_dict.get('workerEducationHours')
worker_education_price = data_dict.get('workerEducationPrice')
risk_assessment_initial_cost = data_dict.get('riskAssessmentInitialCost')
risk_assessment_monthly_cost = data_dict.get('riskAssessmentMonthlyCost')
soc_cost = data_dict.get('socCost')
consult_security_products_cost = data_dict.get('consultSecurityProductsCost')
worker_education_cost = data_dict.get('workerEducationCost')
new_customers = data_dict.get('newCustomers')
referred_customers = data_dict.get('referredCustomers')
lead_customers = data_dict.get('leadCustomers')
year1 = data_dict.get('year1')
year2 = data_dict.get('year2')
year3 = data_dict.get('year3')
year4 = data_dict.get('year4')
year5 = data_dict.get('year5')
new_commission = data_dict.get('newCommission')
referred_commission = data_dict.get('referredCommission')
lead_commission = data_dict.get('leadCommission')
existing_commission = data_dict.get('existingCommission')
new_risk = data_dict.get('newRisk')
referred_risk = data_dict.get('referredRisk')
lead_risk = data_dict.get('leadRisk')
existing_risk = data_dict.get('existingRisk')
new_cost = data_dict.get('newCost')
referred_cost = data_dict.get('referredCost')
lead_cost = data_dict.get('leadCost')
admin_staff = data_dict.get('adminStaff')
tele_staff = data_dict.get('teleStaff')
sales_staff = data_dict.get('salesStaff')
cyber_staff = data_dict.get('cyberStaff')
logistics_staff = data_dict.get('logisticsStaff')
admin_salary = data_dict.get('adminSalary')
tele_salary = data_dict.get('teleSalary')
sales_salary = data_dict.get('salesSalary')
cyber_salary = data_dict.get('cyberSalary')
logistics_salary = data_dict.get('logisticsSalary')
tele_incentive = data_dict.get('teleIncentive')
sales_incentive = data_dict.get('salesIncentive')

print('scenario name: ', scenario_name)
print('insurance price: ', insurance_price, type(insurance_price))






