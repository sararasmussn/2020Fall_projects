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


def patrons_per_minute(total_patrons: int, plot: bool=False) -> list:
    """
    #use these as weights, for each person coming that day, which minute did they arrive? Draw one random # representing the minute, for each person.
    Discrete probability distribution of patrons being added, based on Seattle Public Library data.
    Note: Demand for computers != use of computers, but we only have data measuring use.

    :param total_patrons:
    :param plot:
    :return:
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
    return patron_dist  # Returns a list of all hours that patrons arrived


def run_one_day(fleet: int) -> pd.DataFrame:
    """
    Simulate one day at the library.
    MC sim requirement: Return all data, so that it can be analyzed in aggregate.

    :param fleet: number_of_devices in the IT fleet
    :return: Return Dataframe shaped (1,26) with answers to the following questions: (n=hours_open)
    - How many computers were in service today?                             (dtype int)
    - What was the utilization per hour? (# computers used / # available)   (n columns with dtype float)
    - How many patrons waited to use a computer, per hour?                  (n columns with dtype int)
    - How many patrons left the queue because the wait was longer than TODO?     (n columns with dtype int)
    >>> run_one_day(120)
    {'Patrons today': 621, 'Computers available': 47, 'Utilization': (0.46808510638297873, ..., 1.0), 'Wait count per hour': [0, ..., 0], 'Departed wait queue': 243}
    >>> run_one_day(50)
    {'Patrons today': 621, 'Computers available': 47, 'Utilization': [0.46808510638297873, ..., 1.0], 'Wait count per hour': [0, 0, 0, 41, 101, 144, 129, 57, 30, 0], 'Departed wait queue': 243}
    """
    hours_open = 10

    # Determine total number of computers and patrons today
    computers_available = determine_fleet_availability(fleet)
    total_patrons_today = set_total_patrons_count()
    # Source: https://eulertech.wordpress.com/2017/11/28/pandas-valueerror-if-using-all-scalar-values-you-must-pass-an-index/
    daily_results = pd.DataFrame.from_dict({'Patrons today': [total_patrons_today], 'Computers available': [computers_available]}, orient='columns')
    wait_count_by_hour = []
    utilization_by_hour = []
    waiting = 0
    leavers = 0
    n = 1

    # For each of the patrons today, distribute the patrons' arrival minutes
    ppm = patrons_per_minute(total_patrons_today)

    patron_df = pd.DataFrame(ppm, columns=['Arrival_minute'])
    patron_df = patron_df.sort_values(['Arrival_minute'])
    patron_df['Got_computer_minute'] = np.nan
    patron_df['Leave_minute'] = np.nan
    patron_df['Wait_duration'] = np.nan
    patron_df['Departed_queue'] = np.nan

    # COUNT # PATRONS ARRIVED @ A PARICULAR MINUTE
    counts = patron_df['Arrival_minute'].value_counts()
    # For each new minute...
    computers_in_use = 0
    for minute in range(hours_open * 60):
        # UPDATE COMPUTER USAGE
        while waiting > 0 and (computers_in_use < computers_available):
            comps_free = computers_available - computers_in_use
            # for comps_free:
            # find patron_df min(arrival_time) && got_comp_min.isna == True
            # update got_comp_min == min, leave_min == min + 60
            # wait duration = got_comp_min - min
            waiting -= comps_free
            computers_in_use += comps_free

        if minute not in counts.index.values:
            # If 0 patrons arrived at this minute, skip ahead. Otherwise... count how many patrons arrived.
            patrons_this_minute = 0
        else:
            patrons_this_minute = counts[minute]
            if computers_in_use == computers_available:
                # If a computer is unavailable, people_waiting += # patrons
                waiting += patrons_this_minute
                # Add wait time (how long you waited before getting a computer OR leaving, max wait time = length of time they are "willing" to wait))
            elif computers_in_use < computers_available:
                # If computer available, add # patrons to computers in use
                computers_in_use += patrons_this_minute
                # Find and update ONLY df rows where "Arrival_minute" = minute
                # Source: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
                patron_df.loc[lambda x: x['Arrival_minute'] == minute, ['Got_computer_minute']] = minute                # Add when they got a computer
                patron_df.loc[lambda x: x['Arrival_minute'] == minute, ['Leave_minute']] = minute + 60  # Add when they got a computer   # TODO: Update 60 to vary w/ the time length they are staying for
                patron_df.loc[lambda x: x['Arrival_minute'] == minute, ['Wait_duration']] = (patron_df['Got_computer_minute'] - patron_df['Arrival_minute'])
        # UPDATE QUEUE LEAVERS
        session_end = patron_df[patron_df['Leave_minute'] == minute]   # Return df where Leave_minute == now
        se = session_end['Leave_minute'].tolist()      # Turn that into a list, and see if it's been 60 minutes (handles multiple patrons at 1 minute)
        if len(se) > 0 and minute == se[0]:
            # Free up computer when patron reaches 1 hour
            computers_in_use -= 1
        # Source: https://github.com/iSchool-597PR/Examples_Fa20/blob/master/week_09/pandas_pt2.ipynb

        # Count people who have NOT gotten a computer AND waited over n minutes, 1) leave the queue, 2) set wait duration
        # TODO: Make wait time of 60 an adjustable value
        patron_df.loc[lambda x: (x['Got_computer_minute'].isnull() == True) & (x['Arrival_minute'] == minute - 60), ['Departed_queue']] = 1
        patron_df.loc[lambda x: (x['Got_computer_minute'].isnull() == True) & (x['Arrival_minute'] == minute - 60), ['Wait_duration']] = 60
        done_waiting = patron_df['Arrival_minute'][(patron_df['Got_computer_minute'].isnull() == True) & (patron_df['Arrival_minute'] == minute - 60)].tolist()
        if len(done_waiting) > 0:
            waiting -= len(done_waiting)
            leavers += len(done_waiting) # TODO: get rid of me later
        # COLLECT STATS @ END OF EACH HOUR
        if minute in range(59, (hours_open*60), 60):
            utilization = computers_in_use/computers_available
            utilization_by_hour.append(utilization)
            wait_count_by_hour.append(waiting)
            daily_results["utilization" + str(n)] = utilization
            daily_results["num_waiting" + str(n)] = waiting
            n+=1

    # daily_results['Utilization per hour'] = utilization_by_hour
    # daily_results['Wait count per hour'] = wait_count_by_hour
    daily_results['Departed wait queue'] = leavers # Update to sum the departed queue column in patron_df
    # TODO: Add wait duration results. This data is collected at a per-patron grain, but we are reporting back at daily grain. Yield min, mean, max wait for the whole day. (Note, Max is never higher than whatever I set it to be)
    return daily_results


def run_simulation(inventory_qtys: list, number_of_days: int= 1):
    """
    Run as many days of simulation run_one_day() as specified. Collect all the stats. Print a summary to console.
    TODO: Generates a DataFrame shaped (number_of_days rows, 30 cols) with cols:
        Inventory_qtys: Int
        Acquisition_cost: Int
        Repair_cost: Int
        Total_cost: Int
        [ attach to cols from df returned by run_one_day() ]
    1 row = 1 day; after each day, concat

    :param number_of_days: Number of times the simulation should be run for each inventory_qty. 1 year=365; 4 years=1,460
    :param inventory_qtys: Devices qtys to simulate.
    :return: Answers to these questions:
    TODO: Group up by Inventory_qtys to derive min, median, maxes. NOTE! For some cols, this is by day. For others, by hour.
    - COST_DIST: What was the min/median/max total cost of the service provided?
        (# devices * price of device) + (max(# devices unavailable) * repair fee)
    - UTIL_DIST: What was the min/median/max utilization rate, for all simulations run?
    - WAIT_DURATION_DIST: What was the min/median/max wait time for patrons to get a computer, for all sims run?
    - NUM_WAIT_DIST: What was the min/median/max # of patrons waiting to get a computer, for all sims run?
    - LEAVE_DIST: What was the min/median/max # of people who left because they waited longer than n minutes, for all sims run?
    From this, the user can discern: How many computers should we buy in the next ITAD (IT asset disposition) cycle?
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
            single_simulation = run_one_day(number_of_devices)

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
    n = 100
    run_simulation([20, 80, 120, 160, 200], number_of_days=n)


if __name__ == '__main__':
    main()

