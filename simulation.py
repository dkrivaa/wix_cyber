import simpy
import pandas as pd
import math
import random


def run_simulation(data_dict):

    # Defining Business class
    class Business:
        def __init__(self, env):
            self.env = env

            self.admin_staff = data_dict['adminStaff']
            self.tele_staff = data_dict['teleStaff']
            self.sales_staff = data_dict['salesStaff']
            self.cyber_staff = data_dict['cyberStaff']
            self.logistics_staff = data_dict['logisticsStaff']

            self.tele_resource = simpy.PriorityResource(env, capacity=max(1, int(self.tele_staff *
                                                                          tele_efficient)))
            self.sales_resource = simpy.PriorityResource(env, capacity=max(1, int(self.sales_staff *
                                                                           sales_efficient)))
            self.cyber_resource = simpy.PriorityResource(env, capacity=max(1, int(self.cyber_staff *
                                                                           cyber_efficient)))
            self.meetings_bonus = 0
            self.sales_bonus = 0

            self.package1 = 0
            self.package1_new = 0
            self.package1_referred = 0
            self.package1_lead = 0
            self.package1_existing = 0

            self.package2 = 0
            self.package2_new = 0
            self.package2_referred = 0
            self.package2_lead = 0
            self.package2_existing = 0

            self.package3 = 0
            self.package3_new = 0
            self.package3_referred = 0
            self.package3_lead = 0
            self.package3_existing = 0

            self.income1 = 0
            self.income2 = 0
            self.income3 = 0

            self.product_cost1 = 0
            self.product_cost2 = 0

            self.customer_cost = 0

            self.customers_served = 0
            self.new_customer = 0
            self.referred_customer = 0
            self.lead_customer = 0
            self.existing_customer = 0

            self.no_tele = 0
            self.no_sales = 0
            self.no_cyber = 0

        def labor_cost(self, ):
            return (self.admin_staff * data_dict['adminSalary'] * labor_overhead +
                    self.tele_staff * data_dict['teleSalary'] * labor_overhead +
                    self.sales_staff * data_dict['salesSalary'] * labor_overhead +
                    self.cyber_staff * data_dict['cyberSalary'] * labor_overhead +
                    self.logistics_staff * data_dict['logisticsSalary'] * labor_overhead)

        def marketing_cost(self, ):
            return 10000 + 1500 * self.package3

        def overhead_cost(self, ):
            staff = (self.admin_staff + self.tele_staff + self.sales_staff +
                     self.cyber_staff + self.logistics_staff)
            return max(25000, min(50000, (25000 / 8) * staff))

        def legal_account_cost(self, ):
            return max(2000, min(40000, int((self.income1 + self.income2 + self.income3) * 0.02)))

    # Defining Customer class
    class Customer:
        def __init__(self, env, customer_id, customer_type):
            self.env = env
            self.customer_id = customer_id
            self.customer_type = customer_type

            risk_dict = {'new': data_dict['newRisk'] / 100,
                         'referred': data_dict['referredRisk'] / 100,
                         'lead': data_dict['leadRisk'] / 100,
                         'existing': data_dict['existingRisk'] / 100}
            self.customer_risk = risk_dict[customer_type]

            priority_dict = {'new': 4, 'referred': 3,
                             'lead': 2, 'existing': 1}
            self.customer_priority = priority_dict[customer_type]

            commission_dict = {'new': data_dict['newCommission'] / 100,
                               'referred': data_dict['referredCommission'] / 100,
                               'lead': data_dict['leadCommission'] / 100,
                               'existing': data_dict['existingCommission'] / 100}
            self.customer_commission = commission_dict[customer_type]

            self.customer_size = max(5, int(random.random() * 100))
            # Package bought by customer
            self.package = 0
            self.renewal = False
            self.buy_time = 0

    def customer_generation(env, business):
        customer_num = 0
        while True:
            customer_num += 1
            # Making Customer
            customer_id = f'customer_{customer_num}'
            customer_type = random.choices(['new', 'referred', 'lead'],
                                           [data_dict['newCustomers'],
                                            data_dict['referredCustomers'],
                                            data_dict['leadCustomers']])[0]
            customer = Customer(env, customer_id, customer_type)

            customer_cost_dict = {'new': data_dict['newCost'],
                                  'referred': data_dict['referredCost'],
                                  'lead': data_dict['leadCost']}
            business.customer_cost += customer_cost_dict[customer.customer_type]

            # Transferring customer to receive service
            env.process(serve_customer(env, business, customer))

            # function to calculate costumers for present period (month)
            def customer_birth(period):
                customers = start_customers  # / (1 + data_dict['year1'] / 100)
                last_period = 0
                last_idx = 0

                growth = [data_dict['year1'] / 100, data_dict['year2'] / 100, data_dict['year3'] / 100,
                          data_dict['year4'] / 100, data_dict['year5'] / 100]

                periods = [12, 24, 36, 48]

                if period <= 12:
                    return customers * (1 + growth[0]) ** period
                else:
                    for idx, per in enumerate(periods):
                        if period > per:
                            customers *= (1 + growth[idx]) ** (per if idx == 0 else per - periods[idx - 1])
                            last_idx = idx
                            last_period = per
                    return customers * (1 + growth[last_idx + 1]) ** (period - last_period)

            # calculating costumers for present period (month)
            customers = customer_birth(math.floor(env.now))
            # Pause until next customer 'birth'
            yield env.timeout(1 / customers)

    def renewal(env, business, customer):
        if 11 <= math.floor(env.now) - math.floor(customer.buy_time) <= 13 and customer.package != 0:

            while True:
                yield env.timeout(12)
                print(customer.customer_id, math.floor(customer.buy_time), math.floor(env.now))
                customer.customer_type = 'existing'
                customer.customer_risk = data_dict['existingRisk'] / 100
                customer.customer_priority = 1
                customer.customer_commission = data_dict['existingCommission'] / 100
                customer.renewal = True
                env.process(serve_customer(env, business, customer))
        else:
            customer.package = 0



    def serve_customer(env, business, customer):
        business.customers_served += 1
        if customer.customer_type == 'new':
            business.new_customer += 1
        if customer.customer_type == 'referred':
            business.referred_customer += 1
        if customer.customer_type == 'lead':
            business.lead_customer += 1
        if customer.customer_type == 'existing':
            business.existing_customer += 1

        # Function to determine if customer buying and what package
        def buying_chance(customer):

            if customer.customer_type != 'existing':
                chance = random.random()
                return [random.choices([1, 2, 3], [1, 1, 1])[0] if chance < customer.customer_risk
                        else 0][0]
            else:
                while True:
                    chance = random.random()
                    pack = [3 if chance < customer.customer_risk - 0.1
                            else 2 if chance < customer.customer_risk - 0.05
                            else 1 if chance < customer.customer_risk
                            else 0][0]
                    if pack == 0:
                        customer.package = 0
                        return pack
                    if pack >= customer.package:
                        return pack

        # Function to determine number of interactions
        def sales_interactions(customer):
            return [random.choices([1, 2, 3, 4], [1, 1, 1, 1])[0]
                    if customer.customer_type != 'existing' else 1][0]

        # Process of teleMeeting
        def tele_process(env, business, customer):
            with business.tele_resource.request(priority=customer.customer_priority) as req:
                result = yield req | env.timeout(0)
                if req in result:
                    yield env.timeout(tele_session)
                    if customer.package > 0:
                        return True
                    else:
                        return [True if random.random() < 0.25 else False][0]
                else:
                    return False

        # Process of sales meeting
        def sales_process(env, business, customer):
            with business.sales_resource.request(priority=customer.customer_priority) as req:
                result = yield req | env.timeout(0)
                if req in result:
                    yield env.timeout(sales_session)
                    if customer.package > 0:
                        return True
                    else:
                        return [True if random.random() < 0.25 else False][0]
                else:
                    return False

        # Process of cyber analysis
        def cyber_process(env, business, customer):
            with business.cyber_resource.request(priority=customer.customer_priority) as req:
                result = yield req | env.timeout(0)
                if req in result:
                    yield env.timeout(cyber_session)
                    return True
                else:
                    return False

        buy = buying_chance(customer)
        if buy > 0:
            customer.package = buy
        tele_meet = yield env.process(tele_process(env, business, customer))
        if tele_meet:
            business.meetings_bonus += 50
            sales_meet = yield env.process(sales_process(env, business, customer))
            if sales_meet:
                interactions = sales_interactions(customer)
                # Loop of sales interactions
                for _ in range(interactions):
                    tele_meet = yield env.process(tele_process(env, business, customer))
                    if tele_meet:
                        business.meetings_bonus += 50
                        sales_meet = yield env.process(sales_process(env, business, customer))
                        if not sales_meet:
                            business.no_sales += 1
                            return
                    else:
                        business.no_tele += 1
                        return
                cyber_meet = yield env.process(cyber_process(env, business, customer))
                if cyber_meet:
                    # Transferring to buying process
                    env.process(buy_process(env, business, customer))
                else:
                    business.no_cyber += 1
            else:
                business.no_sales += 1
        else:
            business.no_tele += 1

        yield env.timeout(0)

    # Buying process
    def buy_process(env, business, customer):
        customer.buy_time = math.floor(env.now)
        customer.renewal = False

        # Risk assessment
        def package1(env, business, customer):
            business.income1 += data_dict['riskAssessmentPrice'] * 12
            business.product_cost1 += (data_dict['riskAssessmentInitialCost'] * dollar +
                                       data_dict['riskAssessmentMonthlyCost'] * dollar * 12)

        # Soc and consulting
        def package2(env, business, customer):
            business.income2 += data_dict['socPrice'] * dollar * customer.customer_size * 12
            business.income2 += (data_dict['consultSecurityProductsHours'] *
                                 data_dict['consultSecurityProductsPrice'])
            business.income2 += (data_dict['workerEducationHours'] *
                                 data_dict['workerEducationPrice'])
            business.product_cost2 += data_dict['socCost'] * dollar * customer.customer_size * 12
            business.product_cost2 += (data_dict['consultSecurityProductsHours'] *
                                       data_dict['consultSecurityProductsCost'])
            business.product_cost2 += (data_dict['workerEducationHours'] *
                                       data_dict['workerEducationCost'])

        # Insurance
        def package3(env, business, customer):
            # factor = random.gauss(0,1/3)
            business.income3 += data_dict['insurancePrice'] * customer.customer_commission
            business.sales_bonus += ((data_dict['insurancePrice'] * customer.customer_commission) *
                                     data_dict['salesIncentive'] / 100)

        if customer.package == 1:
            business.package1 += 1
            if customer.customer_type == 'new':
                business.package1_new += 1
            if customer.customer_type == 'referred':
                business.package1_referred += 1
            if customer.customer_type == 'lead':
                business.package1_lead += 1
            if customer.customer_type == 'existing':
                business.package1_existing += 1
            package1(env, business, customer)

        if customer.package == 2:
            business.package2 += 1
            if customer.customer_type == 'new':
                business.package2_new += 1
            if customer.customer_type == 'referred':
                business.package2_referred += 1
            if customer.customer_type == 'lead':
                business.package2_lead += 1
            if customer.customer_type == 'existing':
                business.package2_existing += 1
            package1(env, business, customer)
            package2(env, business, customer)

        if customer.package == 3:
            business.package3 += 1
            if customer.customer_type == 'new':
                business.package3_new += 1
            if customer.customer_type == 'referred':
                business.package3_referred += 1
            if customer.customer_type == 'lead':
                business.package3_lead += 1
            if customer.customer_type == 'existing':
                business.package3_existing += 1
            package1(env, business, customer)
            package2(env, business, customer)
            package3(env, business, customer)

        env.process(renewal(env, business, customer))

        yield env.timeout(0)

    def update_staff(env, business):
        prev_package3 = 0

        while True:
            yield env.timeout((month/4) / month)

            # Update tele staff
            request_time = env.now
            with business.tele_resource.request(priority=4) as req:
                yield req
                get_time = env.now
                if get_time - request_time > 1 / month:
                    business.tele_staff += 1
            business.tele_resource = simpy.PriorityResource(env, capacity=
                                                            max(1, int(business.tele_staff * tele_efficient)))
            # Update sales staff
            request_time = env.now
            with business.sales_resource.request(priority=4) as req:
                yield req
                get_time = env.now
                if get_time - request_time > 1 / month:
                    business.sales_staff += 1
            business.sales_resource = simpy.PriorityResource(env, capacity=
                                                             max(1, int(business.sales_staff * sales_efficient)))
            # Update cyber staff
            request_time = env.now
            with business.cyber_resource.request(priority=4) as req:
                yield req
                get_time = env.now
                if get_time - request_time > 5 / month:
                    business.cyber_staff += 1
            business.cyber_resource = simpy.PriorityResource(env, capacity=
                                                             max(1, int(business.cyber_staff * cyber_efficient)))
            # Update logistics staff
            package3 = business.package3 - prev_package3
            if package3 / business.logistics_staff > 100:
                business.logistics_staff += 1
            prev_package3 = business.package3

            # Update admin staff



    def track_data(env, business, results):
        # Accumulated data being tracked
        prev_customers = 0
        prev_new_customer = 0
        prev_referred_customer = 0
        prev_lead_customer = 0
        prev_exiting_customer = 0

        prev_package1 = 0
        prev_package1_new = 0
        prev_package1_referred = 0
        prev_package1_lead = 0
        prev_package1_existing = 0

        prev_package2 = 0
        prev_package2_new = 0
        prev_package2_referred = 0
        prev_package2_lead = 0
        prev_package2_existing = 0

        prev_package3 = 0
        prev_package3_new = 0
        prev_package3_referred = 0
        prev_package3_lead = 0
        prev_package3_existing = 0

        prev_income1 = 0
        prev_income2 = 0
        prev_income3 = 0

        prev_meetings_bonus = 0
        prev_sales_bonus = 0

        prev_product_cost1 = 0
        prev_product_cost2 = 0

        prev_no_tele = 0
        prev_no_sales = 0
        prev_no_cyber = 0

        while True:
            yield env.timeout(1)
            period = math.floor(env.now)

            customers_served = business.customers_served - prev_customers
            new_customer_served = business.new_customer - prev_new_customer
            referred_customer_served = business.referred_customer - prev_referred_customer
            lead_customer_served = business.lead_customer - prev_lead_customer
            existing_customer_served = business.existing_customer - prev_exiting_customer

            package1 = business.package1 - prev_package1
            package1_new = business.package1_new - prev_package1_new
            package1_referred = business.package1_referred - prev_package1_referred
            package1_lead = business.package1_lead - prev_package1_lead
            package1_existing = business.package1_existing - prev_package1_existing

            package2 = business.package2 - prev_package2
            package2_new = business.package2_new - prev_package2_new
            package2_referred = business.package2_referred - prev_package2_referred
            package2_lead = business.package2_lead - prev_package2_lead
            package2_existing = business.package2_existing - prev_package2_existing

            package3 = business.package3 - prev_package3
            package3_new = business.package3_new - prev_package3_new
            package3_referred = business.package3_referred - prev_package3_referred
            package3_lead = business.package3_lead - prev_package3_lead
            package3_existing = business.package3_existing - prev_package3_existing

            all_packages_sold = package1 + package2 + package3

            income1 = business.income1 - prev_income1
            income2 = business.income2 - prev_income2
            income3 = business.income3 - prev_income3
            total_income = income1 + income2 + income3

            total_staff = (business.admin_staff + business.tele_staff + business.sales_staff +
                           business.cyber_staff + business.logistics_staff)
            meeting_bonus = (business.meetings_bonus - prev_meetings_bonus) * labor_overhead
            sales_bonus = (business.sales_bonus - prev_sales_bonus) * labor_overhead
            labor_cost = business.labor_cost() + meeting_bonus + sales_bonus

            product_cost1 = business.product_cost1 - prev_product_cost1
            product_cost2 = business.product_cost2 - prev_product_cost2

            marketing_cost = 10000 + 1500 * package3
            overhead_cost = business.overhead_cost()
            legal_account_cost = max(2000, min(40000, int(total_income * 0.02)))

            total_cost = (labor_cost + product_cost1 + product_cost2 + marketing_cost +
                          overhead_cost + legal_account_cost)

            gross_profit = total_income - total_cost



            no_tele = business.no_tele - prev_no_tele
            no_sales = business.no_sales - prev_no_sales
            no_cyber = business.no_cyber - prev_no_cyber

            results.append([period, customers_served, new_customer_served, referred_customer_served,
                            lead_customer_served, existing_customer_served, package1, package1_new,
                            package1_referred, package1_lead, package1_existing, package2, package2_new,
                            package2_referred, package2_lead, package2_existing, package3, package3_new,
                            package3_referred, package3_lead, package3_existing, all_packages_sold,
                            income1, income2, income3, total_income,
                            business.admin_staff, business.tele_staff, business.sales_staff,
                            business.cyber_staff, business.logistics_staff, total_staff, labor_cost,
                            product_cost1, product_cost2, marketing_cost, overhead_cost, legal_account_cost,
                            total_cost, gross_profit, ])

            prev_customers = business.customers_served
            prev_new_customer = business.new_customer
            prev_referred_customer = business.referred_customer
            prev_lead_customer = business.lead_customer
            prev_exiting_customer = business.existing_customer

            prev_package1 = business.package1
            prev_package1_new = business.package1_new
            prev_package1_referred = business.package1_referred
            prev_package1_lead = business.package1_lead
            prev_package1_existing = business.package1_existing

            prev_package2 = business.package2
            prev_package2_new = business.package2_new
            prev_package2_referred = business.package2_referred
            prev_package2_lead = business.package2_lead
            prev_package2_existing = business.package2_existing

            prev_package3 = business.package3
            prev_package3_new = business.package3_new
            prev_package3_referred = business.package3_referred
            prev_package3_lead = business.package3_lead
            prev_package3_existing = business.package3_existing

            prev_income1 = business.income1
            prev_income2 = business.income2
            prev_income3 = business.income3

            prev_meetings_bonus = business.meetings_bonus
            prev_sales_bonus = business.sales_bonus

            prev_product_cost1 = business.product_cost1
            prev_product_cost2 = business.product_cost2

            prev_no_tele = business.no_tele
            prev_no_sales = business.no_sales
            prev_no_cyber = business.no_cyber


    # Model Parameters not included in user controlled assumptions
    tele_efficient = 0.6
    sales_efficient = 0.6
    cyber_efficient = 0.7

    labor_overhead = 1.3

    month = 21*8*60
    tele_session = 10 / month
    sales_session = 15 / month
    cyber_session = 30 / month

    dollar = 3.6

    start_customers = 100


    # Starting simulation environment
    env = simpy.Environment()
    business = Business(env, )

    env.process(customer_generation(env, business))
    env.process((update_staff(env, business)))

    # List of monthly simulation results
    results = []
    env.process(track_data(env, business, results))

    env.run(until=61)

    return results