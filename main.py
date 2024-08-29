import os
import json

json_vars = os.getenv('JSON_VARS')
vars_dict = json.loads(json_vars)  # Decode JSON string into a dictionary

print(vars_dict)

scenario_name = vars_dict.get('scenarioName')
insurance_price = int(vars_dict.get('insurancePrice'))
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
admin_staff = vars_dict.get('adminStaff')
tele_staff = vars_dict.get('teleStaff')
sales_staff = vars_dict.get('salesStaff')
cyber_staff = vars_dict.get('cyberStaff')
logistics_staff = vars_dict.get('logisticsStaff')
admin_salary = vars_dict.get('adminSalary')
tele_salary = vars_dict.get('teleSalary')
sales_salary = vars_dict.get('salesSalary')
cyber_salary = vars_dict.get('cyberSalary')
logistics_salary = vars_dict.get('logisticsSalary')
tele_incentive = vars_dict.get('teleIncentive')
sales_incentive = vars_dict.get('salesIncentive')

print('scenario name: ', scenario_name)
print('insurance price: ', insurance_price, type(insurance_price))






