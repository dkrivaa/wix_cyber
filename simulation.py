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
            self.package2 = 0
            self.package3 = 0

            self.income = 0
            self.product_cost = 0

            self.customer_cost = 0

        def labor_cost(self, env):
            return (self.admin_staff * data_dict['adminSalary'] * labor_overhead +
                    self.tele_staff * data_dict['teleSalary'] * labor_overhead +
                    self.sales_staff * data_dict['salesSalary'] * labor_overhead +
                    self.cyber_staff * data_dict['cyberSalary'] * labor_overhead +
                    self.logistics_staff * data_dict['logisticsSalary'] * labor_overhead +
                    self.meetings_bonus * labor_overhead +
                    self.sales_bonus * labor_overhead)

        def marketing_cost(self, env):
            return 10000 + 1500 * self.package3

        def overhead_cost(self, env):
            staff = (self.admin_staff + self.tele_staff + self.sales_staff +
                     self.cyber_staff + self.logistics_staff)
            return max(25000, min(50000, (25000 / 8) * staff))

        def legal_account_cost(self, env):
            return max(2000, min(40000, int(self.income * 0.02)))

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
                customers = start_customers / (1 + data_dict['year1'] / 100)
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
        if customer.package != 0:
            while True:
                yield env.timeout(12)
                customer.customer_type = 'existing'
                customer.customer_risk = data_dict['existingRisk'] / 100
                customer.customer_priority = 1
                customer.customer_commission = data_dict['existingCommission'] / 100
                customer.package = 0

                env.process(serve_customer(env, business, customer))

    def serve_customer(env, business, customer):
        # Function to determine if customer buying and what package
        def buying_chance(customer):
            chance = random.random()
            return [3 if chance < customer.customer_risk
                    else 2 if chance < customer.customer_risk + 0.05
                    else 1 if chance < customer.customer_risk + 0.1
                    else 0][0]

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
                        return [True if random.random() < 0.25 else False]
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
                        return [True if random.random() < 0.25 else False]
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
                            return
                    else:
                        return
                cyber_meet = yield env.process(cyber_process(env, business, customer))
                if cyber_meet:
                    # Transferring to buying process
                    env.process(buy_process(env, business, customer))

        yield env.timeout(0)

    # Buying process
    def buy_process(env, business, customer):
        # Risk assessment
        def package1(env, business, customer):
            business.income += data_dict['riskAssessmentPrice'] * 12
            business.product_cost += (data_dict['riskAssessmentInitialCost'] * dollar +
                                      data_dict['riskAssessmentMonthlyCost'] * dollar * 12)

        # Soc and consulting
        def package2(env, business, customer):
            business.income += data_dict['socPrice'] * dollar * customer.customer_size * 12
            business.income += (data_dict['consultSecurityProductsHours'] *
                                data_dict['consultSecurityProductsHourPrice'])
            business.income += (data_dict['workerEducationHours'] *
                                data_dict['workerEducationHourPrice'])
            business.product_cost += data_dict['socCost'] * dollar * customer.customer_size * 12
            business.product_cost += (data_dict['consultSecurityProductsHours'] *
                                      data_dict['consultSecurityProductsHourCost'])
            business.product_cost += (data_dict['workerEducationHours'] *
                                      data_dict['workerEducationHourCost'])

        # Insurance
        def package3(env, business, customer):
            # factor = random.gauss(0,1/3)
            business.income += data_dict['insurancePrice'] * customer.customer_commission
            business.sales_bonus += ((data_dict['insurancePrice'] * customer.customer_commission) *
                                     data_dict['salesIncentive'])

        if customer.package == 1:
            business.package1 += 1
            package1(env, business, customer)
        if customer.package == 2:
            business.package2 += 1
            package1(env, business, customer)
            package2(env, business, customer)
        if customer.package == 3:
            business.package3 += 1
            package1(env, business, customer)
            package2(env, business, customer)
            package3(env, business, customer)

        env.process(renewal(env, business, customer))

        yield env.timeout(0)

    def update_staff(env, business):
        while True:
            request_time = env.now
            with business.tele_resource.request(priority=1) as req:
                yield req
                get_time = env.now
                if get_time - request_time > 10 / month:
                    business.tele_staff += 1

            with business.sales_resource.request(priority=1) as req:
                yield req
                get_time = env.now
                if get_time - request_time > 10 / month:
                    business.sales_staff += 1

            with business.cyber_resource.request(priority=1) as req:
                yield req
                get_time = env.now
                if get_time - request_time > 20 / month:
                    business.cyber_staff += 1


    def track_data(env, business, ):
        yield env.timeout(1)
        print(math.floor(env.now), business.tele_staff)


    # Model Parameters not included in user controlled assumptions
    tele_efficient = 0.6
    sales_efficient = 0.6
    cyber_efficient = 0.7

    labor_overhead = 1.3

    month = 21*8*60
    tele_session = 15 / month
    sales_session = 20 / month
    cyber_session = 30 / month

    dollar = 3.6

    start_customers = 100


    # Starting simulation environment
    env = simpy.Environment(initial_time=1)
    business = Business(env, )

    env.process(customer_generation(env, business))
    env.process((update_staff(env, business)))
    env.process(track_data(env, business))

    env.run(until=61)
