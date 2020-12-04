"""
Monte Carlo simulation of library computer utilization
Sara Rasmussen (saralr2)
IS597PR
Fall 2020
"""
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def calculate_pert(low, likely, high, weight=4) -> float:
    """
    Simple PERT estimate = (a + 4b + c)/6 used in determining multiple variables

    :param low: Lowest number a in distribution
    :param likely: Middle number b in distribution
    :param high: Highest number c in distribution
    :param weight: How many times more likely is the middle number?
    :return: Float pert value
    >>> calculate_pert(90, 500, 900, 4)
    498.3333333333333
    >>> calculate_pert(80, 400, 900, 4)
    430.0
    """
    pert = (low + (weight * likely) + high)/(weight+2)
    return pert


def determine_fleet_availability(total_inventory: int) -> int:
    """
    RANDOMIZED VARIABLE: Given the number of computers in your fleet, calculate out-of-service count, return the number of computers in service today.
    Uses a PERT distribution.
    ---
    "Mean time between failures (MTBF) is the predicted elapsed time between inherent failures of a mechanical or electronic system, during normal system operation.
    MTBF can be calculated as the arithmetic mean (average) time between failures of a system." (Wikipedia)
    Average laptop failure rate after 2 years = 19%; after 3 years = 31% (Sands and Tseng)
    - For each machine, there is some probability of failure
    - For each day, count the number of machines failed

    :total_inventory: The number of computers in your inventory. Must be an int.
    :Weight: Default value is 4; the amount of likelihood that the middle point will be true.
    :return: The number of computers available to be used today. Must be an int.
    >>> determine_fleet_availability(153)
    145
    """
    best_case = 0.00
    likely_case = 0.04
    worst_case = random.uniform(0.19, 0.31)
    pct_out = calculate_pert(best_case, likely_case, worst_case)
    out_of_service = (total_inventory * pct_out)
    todays_inventory = total_inventory - int(out_of_service)
    return todays_inventory


def select_reservation_length() -> int:
    """
    RANDOMIZED VARIABLE
    Binomial distribution.
    For one computer reservation, randomly select the reservation length:
    Options for length of use selected by the patrons: 15 or 1 hour.
    Discrete distribution between two options. Not 50/50. Probably skewed more like 25/75.
    Computer use policy:
    After each computer use, there will be a 15-minute delay (where the computer is unavailable to be used)
        so that staff can sanitize the area per the library’s COVID-19 cleaning procedures.

    :return: The length of time
    """
    return 1


def set_total_patrons_count(samples: int = 1) -> int:
    """
    Set the total number of patrons for 1 day.
    Uses a beta distribution.


    :samples: Number of times to run the simulation, used for testing the distribution.
    :return: RANDOMIZED variable, based on Chicago Public Library data.
    >>> results = []
    >>> for test in range(5):
    ...     results.append(set_total_patrons_count(samples=10000))  # Testing mode
    >>> print(results)
    >>> min(results) >= 444
    True
    >>> max(results) <= 949
    True
    """
    # We cannot assume that because people have used public computers in the past, they will continue to.
    # In fact, CPL data shows that usage decreased for the last 3 years, specifically by 13.5% from 2018 to 2019.
    low_service = (514 * .865)      # I've intentionally lowered the low end by 13.5%.
    # But it's also likely that due to the economic crisis, usage will go up (Jaeger et al., 2011).
    peak_service = random.uniform(622, 949)     # 949 was the highest number in 2016
    # Source: https://github.com/iSchool-597PR/Examples_Fa20/blob/master/week_07/Probability_Distributions.ipynb & https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.beta.html
    g = np.random.default_rng()
    patron_pct = np.random.Generator.beta(g, low_service, peak_service, samples)
    if samples > 1:
        # Testing my distribution: Does it look like the CPL data?
        patron_array = (low_service * patron_pct) + low_service
        plt.hist(patron_array,
                        bins=200,
                        density=True)
        plt.show()
    patron_count = (low_service * patron_pct[0]) + low_service
    return int(patron_count)


def patrons_per_minute(total_patrons: int, plot: bool = False) -> list:
    """
    #use these as weights, for each person coming that day, which minute did they arrive? Draw one random # representing the minute, for each person.
    Discrete probability distribution of patrons being added, based on Seattle Public Library data.
    Note: Demand for computers != use of computers, but we only have data measuring use.

    :param total_patrons: Int yielded from set_total_patrons_count()
    :param plot: Optional, prints 10 plots to review the distribution of patrons
    :return: Returns a list of all hours that patrons arrived
    >>> patrons_per_minute(700)
    [1,2,3]
    >>> for i in range(10):
    ...     patrons_per_minute(700, plot=True)
    [1,2,3]
    """
    # Determine RANDOMLY, WITH WEIGHTS, what minute each patron arrived at.
    hours = np.arange(10)
    minutes = np.arange(600)
    probs = []
    for i in range(600):
        if i < 60:
            probs.append(0.035010)
        elif i < 120:
            probs.append(0.045726)
        elif i < 180:
            probs.append(0.055542)
        elif i < 240:
            probs.append(0.136442)
        elif i < 300:
            probs.append(0.165399)
        elif i < 360:
            probs.append(0.223067)
        elif i < 420:
            probs.append(0.199427)
        elif i < 480:
            probs.append(0.088998)
        elif i < 540:
            probs.append(0.047607)
        elif i < 600:
            probs.append(0.002781)
    patron_dist = random.choices(minutes, weights=probs, k=total_patrons)   # np.random.choice(hours, total_patrons, p=probs)
    if plot is True:
        plt.hist(patron_dist,
                 bins=200,
                 density=True)
        plt.show()
    return patron_dist


def run_one_day(fleet) -> dict:
    """
    Simulate one day at the library.
    MC sim requirement: Return all data, so that it can be analyzed in aggregate.

    :return: Returns answers to the following questions, as a dict:
    - How many computers were in service today?                             (Returns 1 int)
    - What was the utilization per hour? (# computers used / # available)   (Returns a list of floats)
    - How many patrons waited to use a computer, per hour?                  (Returns a list of ints)
    - How many patrons left the queue because the wait was over 1 hour?     (Returns 1 int)
    >>> run_one_day(120)
    {'Computers available': 47, 'Utilization': (0.46808510638297873, ..., 1.0), 'Wait count per hour': [0, ..., 0], 'Departed wait queue': 243}
    >>> run_one_day(50)
    {'Computers available': 47, 'Utilization': [0.46808510638297873, ..., 1.0], 'Wait count per hour': [0, 0, 0, 41, 101, 144, 129, 57, 30, 0], 'Departed wait queue': 243}
    """
    computers_available = determine_fleet_availability(fleet)
    daily_results = {"Computers available": computers_available}
    wait_count_by_hour = []
    utilization_by_hour = []
    departed_queue = []
    hours_open = 10
    waiting = 0
    total_patrons_today = set_total_patrons_count()
    for hour in range(hours_open):
        new_patrons = patrons_per_minute(total_patrons_today)
        users = new_patrons + waiting
        # If waited more than 1 hour, leave the line
        if waiting > computers_available:
            leavers = waiting - computers_available
            departed_queue.append(leavers)
            users = users - leavers
        if users > computers_available:
            waiting = users - computers_available
            utilization = computers_available/computers_available
        else:
            waiting = 0
            utilization = users/computers_available
        wait_count_by_hour.append(waiting)          # List of ints
        utilization_by_hour.append(utilization)     # List of floats
    daily_results['Utilization'] = utilization_by_hour
    daily_results['Wait count per hour'] = wait_count_by_hour
    daily_results['Departed wait queue'] = sum(departed_queue)
    return daily_results


def run_simulation(inventory_qtys: list, number_of_days: int= 1):
    """
    Run as many days of simulation run_one_day() as specified. Collect all the stats. Print a summary to console.

    :param number_of_days: Number of times the simulation should be run. 1 year=365; 4 years=1,460
    :param inventory_qtys: Devices qtys to simulate.
    :return: Answers to these questions:
    - What was the total cost of the service provided?
        (# devices * price of device) + (max(# devices unavailable) * repair fee)
    - What was the min/median/max utilization rate for all simulations run?
    - What was the average # of drop-offs (people who left because they waited longer than 30 minutes) for all sims run?
    From this, the user can discern: How many computers should we buy?
    """
    print("Running simulation of", number_of_days, "days...\n")

    # Run the simulation once for each device count
    avg_cost = []
    avg_util = []
    users_waiting = []
    for number_of_devices in inventory_qtys:
        # Acquisition is a fixed cost based on the number of devices in inventory
        acquisition_cost = (number_of_devices * 375)    # Your average Chromebook price

        # Run the simulation the specified # times
        for days in range(number_of_days):
            # Call the single simulation
            single_simulation = V3_run_one_day(number_of_devices)

            # Determine the total repair cost for n simulations run
            # Repair fee: $95 (2 hours to collect, re-image, return a computer * median(DOIS help desk tech $40-55/hr wage)) (Source: Chicago Data Portal)
            repair_cost = ((number_of_devices - single_simulation['Computers available']) * 95)
            total_cost = acquisition_cost + repair_cost
            avg_cost.append(total_cost)

            # Determine utilization for n simulations run
            utilization = sum(single_simulation['Utilization'])/len(single_simulation['Utilization'])
            avg_util.append(utilization)

            # Determine avg wait time over n simulations run
            # users_waiting.append(sum(single_simulation['Users Waiting']))

        total_waiting = sum(users_waiting)
        final_cost = sum(avg_cost)/len(avg_cost)
        final_util = sum(avg_util)/len(avg_util)
        print("# Devices: {}\nAvg cost: ${:,.2f}\t\tAvg utilization: {:2.2%}\t\t Total users who waited: {:,}\n".format(number_of_devices, final_cost, final_util, total_waiting))

        # Clear these variables at the end of each loop
        avg_util = []
        avg_cost = []
        users_waiting = []


def main():
    # TODO: Convert to user input
    # n = input("How many days should the simulation run? ")
    n = 1460
    run_simulation([20, 80, 120, 160, 200], number_of_days=n)


if __name__ == '__main__':
    main()

