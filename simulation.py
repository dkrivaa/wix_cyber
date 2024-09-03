import simpy
import pandas as pd


def run_simulation(data_dict):

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




    class Customer:
        def __init__(self, env, customer_type):
            self.env = env
            self.customer_type = customer_type


    # Model Parameters not included in user controlled assumptions
    tele_efficient = 0.6
    sales_efficient = 0.6
    cyber_efficient = 0.7
