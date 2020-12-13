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
from collections import Counter
import datetime


def calculate_pert(low, likely, high, weight=4) -> float:
    """
    Simple PERT estimate = (a + 4b + c)/6 used in determining multiple variables
    Source: https://mediaspace.illinois.edu/media/t/1_lawwsyso

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
    "Mean time between failures (MTBF) is the predicted elapsed time between inherent failures of a mechanical or electronic system, during normal system operation.
    MTBF can be calculated as the arithmetic mean (average) time between failures of a system." (Source: Wikipedia)
    Average laptop failure rate after 2 years = 19%; after 3 years = 31% (Source: Sands and Tseng)

    :total_inventory: The number of computers in your inventory. Must be an int.
    :Weight: Default value is 4; the amount of likelihood that the middle point will be true.
    :return: The number (int) of computers available to be used today
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
    For one computer reservation, randomly select the reservation length:
    Options for length of use selected by the patrons: 15 or 1 hour.
    Discrete distribution between two options. Not 50/50. Probably skewed more like 30/70. (Source: Personal experience)

    :return: The length of time
    >>> results = Counter()
    >>> tests = 100000
    >>> for test in range(tests):
    ...     if select_reservation_length() == 15:
    ...         results[15] += 1
    ...     else:
    ...         results[60] += 1
    >>> .72 <= (results[60] / tests) <= .78
    True
    >>> .22 <= (results[15] / tests) <= .28
    True
    """
    choices = [15, 60]
    skew = [30, 70]
    reservation = random.choices(choices, weights=skew, k=1)
    return reservation[0]


def set_wait_length() -> int:
    """
    RANDOMIZED VARIABLE (Uniform distribution) of how long patrons are willing to wait.

    :return: Int between 15 and 90
    """
    wait = random.uniform(15, 90)
    return int(wait)


def set_total_patrons_count(samples: int = 1) -> int:
    """
    Set the total number of patrons for 1 day.
    RANDOMIZED VARIABLE, based on Chicago Public Library data. Uses a beta distribution.

    :samples: Number of times to run the simulation, used for testing the distribution.
    :return: An int between 444 and 821
    >>> results = []
    >>> for test in range(5):
    ...     results.append(set_total_patrons_count(samples=10000))  # Testing mode
    >>> min(results) >= 444
    True
    >>> max(results) <= 949
    True
    """
    # We cannot assume that because people have used public computers in the past, they will continue to.
    # In fact, CPL data shows that usage decreased for the last 3 years, specifically by 13.5% from 2018 to 2019.
    low_service = (514 * .865)      # I've intentionally lowered the low end by 13.5%.
    # But it's also likely that due to the economic crisis, usage will go up (Jaeger et al., 2011).
    peak_service = random.triangular((622 * .865), (949 * .865), (622))     # Triangular distribution, giving more weight to probability of lower numbers; 949 was the peak in 2016.
    # Source: https://github.com/iSchool-597PR/Examples_Fa20/blob/master/week_07/Probability_Distributions.ipynb & https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.beta.html
    g = np.random.default_rng()
    patron_pct = np.random.Generator.beta(g, low_service, peak_service, samples)
    if samples > 1:
        # Testing my distribution: Does it look like the CPL data?
        patron_array = ((peak_service - low_service) * patron_pct) + low_service
        plt.hist(patron_array, bins=200, density=True)
        plt.show()
    patron_count = ((peak_service - low_service) * patron_pct[0]) + low_service
    return int(patron_count)


def patrons_per_minute(total_patrons: int, plot: bool = False) -> list:
    """
    Draw one random # representing the minute arrived, for each person.
    Discrete probability distribution of patrons showing up throughout the day, based on Seattle Public Library data.
    Note: Demand for computers != use of computers, but we only have data measuring use.

    :param total_patrons: Int yielded from set_total_patrons_count()
    :param plot: Optional, prints 10 plots to review the distribution of patrons
    :return: Returns a list of all hours that patrons arrived
    >>> test1 = patrons_per_minute(550, plot=True)  # X-axis = Minute arrived
    >>> len(test1)      # Confirm total number of patrons that day
    550
    >>> counter = []
    >>> for p in range(100):      # Verify that 20% or fewer arrivals are before minute 240
    ...     test2 = patrons_per_minute(450)
    ...     early = 0
    ...     for minute in test2:
    ...         if minute < 180:
    ...             early +=1
    ...     counter.append(early/len(test2))
    >>> counter.sort()
    >>> for c in counter: c <= 0.20      # doctest: +ELLIPSIS
    True
    ...
    True
    """
    minutes = np.arange(600)
    probs = []
    for i in range(600):
        if i < 60:      # Hour 1
            probs.append(0.035010)
        elif i < 120:
            probs.append(0.045726)
        elif i < 180:
            probs.append(0.055542)
        elif i < 240:
            probs.append(0.136442)
        elif i < 300:   # Hour 5
            probs.append(0.165399)
        elif i < 360:
            probs.append(0.223067)
        elif i < 420:
            probs.append(0.199427)
        elif i < 480:
            probs.append(0.088998)
        elif i < 540:
            probs.append(0.047607)
        elif i < 600:   # Hour 10
            probs.append(0.002781)
    patron_dist = random.choices(minutes, weights=probs, k=total_patrons)
    if plot is True:
        plt.hist(patron_dist,
                 bins=200,
                 density=True)
        plt.show()
    return patron_dist


def run_one_day(fleet: int, hours_open: int = 10) -> pd.DataFrame:
    """
    Simulate one day at the library.
    MC sim requirement: Return all data, so that it can be analyzed in aggregate.
    # Source: https://pymotw.com/2/doctest/

    :param fleet: number_of_devices in the IT fleet
    :param hours_open: number of hours open per day; 10 by default
    :return: Return Dataframe shaped (1,27) with answers to the following questions: (n=hours_open)
    - How many computers were in service today?                             (dtype int)
    - What was the utilization per hour? (# computers used / # available)   (n columns with dtype float)
    - How many patrons waited to use a computer, per hour?                  (n columns with dtype int)
    - How many patrons left the queue because the wait was longer than wait_length()?     (n columns with dtype int)
    - What was the repair cost for the day?                                 (dtype int)
    >>> run_one_day(150)     # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Computers available...min wait duration
    ...
    <BLANKLINE>
    [1 rows x 27 columns]
    """
    # Determine total number of computers and patrons today
    computers_available = determine_fleet_availability(fleet)
    total_patrons_today = set_total_patrons_count()
    # Source: https://eulertech.wordpress.com/2017/11/28/pandas-valueerror-if-using-all-scalar-values-you-must-pass-an-index/
    daily_results = pd.DataFrame.from_dict({'Patrons today': [total_patrons_today], 'Computers available': [computers_available]}, orient='columns')
    wait_count_by_hour = []
    utilization_by_hour = []
    waiting = 0
    hour = 1

    # For each of the patrons today, distribute the patrons' arrival minutes
    ppm = patrons_per_minute(total_patrons_today)
    # Collect by-patron data
    patrons_df = pd.DataFrame(ppm, columns=['Arrival_minute'])
    patrons_df = patrons_df.sort_values(['Arrival_minute'])
    patrons_df['Got_computer_minute'] = np.nan
    patrons_df['Leave_minute'] = np.nan
    patrons_df['Wait_duration'] = np.nan
    patrons_df['Departed_queue'] = np.nan

    # COUNT # PATRONS ARRIVED @ A PARTICULAR MINUTE
    counts = patrons_df['Arrival_minute'].value_counts()
    computers_in_use = 0
    for minute in range(hours_open * 60):
        # UPDATE COMPUTER USAGE
        # Before assigning new patrons to a computer, assign patrons who are waiting
        while waiting > 0 and (computers_in_use < computers_available):
            comps_free = computers_available - computers_in_use
            # Return a series or int w/ min(arrival minute) where got_computer_minute is null
            oldest_arrive_min = patrons_df['Arrival_minute'][(patrons_df['Got_computer_minute'].isnull() == True) & (patrons_df['Departed_queue'].isnull() == True)].min()
            # Source: https://github.com/iSchool-597PR/Examples_Fa20/blob/master/week_09/pandas_pt2.ipynb
            patrons_df.loc[lambda x: (x['Got_computer_minute'].isnull() == True) & (x['Arrival_minute'] == oldest_arrive_min), ['Got_computer_minute']] = minute
            patrons_df.loc[lambda x: x['Arrival_minute'] == oldest_arrive_min, ['Leave_minute']] = minute + select_reservation_length()
            patrons_df.loc[lambda x: x['Arrival_minute'] == oldest_arrive_min, ['Wait_duration']] = minute - patrons_df['Arrival_minute']
            waiting -= comps_free
            computers_in_use += comps_free
        # If 0 patrons arrived at this minute, skip ahead. Otherwise... count how many patrons arrived.
        if minute not in counts.index.values:
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
                patrons_df.loc[lambda x: x['Arrival_minute'] == minute, ['Got_computer_minute']] = minute                # Add when they got a computer
                patrons_df.loc[lambda x: x['Arrival_minute'] == minute, ['Leave_minute']] = minute + select_reservation_length()  # Add when they got a computer
                patrons_df.loc[lambda x: x['Arrival_minute'] == minute, ['Wait_duration']] = (patrons_df['Got_computer_minute'] - patrons_df['Arrival_minute'])
        # UPDATE QUEUE LEAVERS
        # Free up computer when patron reaches end of reservation length
        session_end = patrons_df[patrons_df['Leave_minute'] == minute]   # Return df where Leave_minute == now
        se = session_end['Leave_minute'].tolist()      # Turn that into a list, and see if it's been their reservation length (handles multiple patrons at 1 minute)
        if len(se) > 0 and minute == se[0]:
            computers_in_use -= 1
        # Count people who have NOT gotten a computer AND waited over set_wait_length() minutes, 1) leave the queue, 2) set wait duration
        wait_length = set_wait_length()
        patrons_df.loc[lambda x: (x['Got_computer_minute'].isnull() == True) & (x['Arrival_minute'] == minute - wait_length), ['Departed_queue']] = 1
        patrons_df.loc[lambda x: (x['Got_computer_minute'].isnull() == True) & (x['Arrival_minute'] == minute - wait_length), ['Wait_duration']] = wait_length
        done_waiting = patrons_df['Arrival_minute'][(patrons_df['Got_computer_minute'].isnull() == True) & (patrons_df['Arrival_minute'] == minute - wait_length)].tolist()
        if len(done_waiting) > 0:
            waiting -= len(done_waiting)
        # COLLECT STATS @ END OF EACH HOUR
        if minute in range(59, (hours_open*60), 60):
            utilization = computers_in_use/computers_available
            utilization_by_hour.append(utilization)
            wait_count_by_hour.append(waiting)
            daily_results["Utilization " + str(hour)] = utilization
            daily_results["Patrons_waiting " + str(hour)] = waiting
            hour += 1

    # UPDATE DAILY RESULTS
    daily_results['Departed wait queue'] = int(patrons_df['Departed_queue'].sum())
    daily_results['min wait duration'] = patrons_df['Wait_duration'].min()
    daily_results['median wait duration'] = patrons_df['Wait_duration'].median()
    daily_results['max wait duration'] = patrons_df['Wait_duration'].max()
    # Repair fee: $95 (2 hours to collect, re-image, return a computer * median(DOIS help desk tech $40-55/hr wage)) (Source: Chicago Data Portal)
    daily_results['Repair cost'] = (fleet - daily_results['Computers available']) * 95
    # Replacing negative values with zeroes is not an ideal solution, but it will do for now.
    daily_results = daily_results.replace(list(np.arange(-100, -1)), 0)
    daily_results = daily_results.sort_index(axis=1)
    return daily_results


def run_simulation(inventory_qtys: list, number_of_days: int = 1) -> list:
    """
    Run as many days of simulation run_one_day() as specified.

    :param number_of_days: Number of times the simulation should be run for each inventory_qty.
    :param inventory_qtys: Devices qtys to simulate.
    :return: A list of dataframes with answers to these questions:
    - DETAILED: Full output, useful if you were planning to load the data into Tableau for detailed analysis and visualizations.
    - FINANCIALS: What was the upfront cost of devices and median cost of repairs?
    - WAIT_DURATIONS: What was the min/median/max wait time for patrons to get a computer, for all sims run?
    - DEPARTURES: What was the min/median/max # of patrons who left because they waited longer than n minutes, grouped by inventory_qty?
    - PATRONS_WAITING: What was the max # of patrons waiting to get a computer, grouped by inventory_qty?
    - UTILIZATION: What was the min/median/max utilization rate per hour, grouped by inventory_qty?

    From this, the user can discern: How many computers should we buy in the next ITAD (IT asset disposition) cycle?
    """
    hours_open = 10
    print("Running simulation of", number_of_days, "days...\n")
    sims = []
    # Source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.append.html & https://maneeshasane.com/programming/2020/09/pandas-cheat-sheet.html
    financials = pd.concat([pd.DataFrame([i], columns=['Inventory qty']) for i in inventory_qtys], ignore_index=True)
    # 375 = Your average Chromebook price; Acquisition is a fixed cost based on the number of devices in inventory; Ignore bulk pricing models
    financials['Acquisition cost'] = financials['Inventory qty'].apply(lambda x: x * 375)
    for number_of_devices in inventory_qtys:
        print(datetime.datetime.now(), ": Simulating", number_of_devices, "qty...")
        # Run the simulation the specified # times
        for days in range(number_of_days):
            # Call the single simulation
            single_simulation = run_one_day(number_of_devices)
            single_simulation['Inventory qty'] = number_of_devices
            sims.append(single_simulation)  # List of all simulation dfs
    detailed = pd.concat(sims, ignore_index=True)    # detailed is the master DataFrame from which aggregate stats can be derived
    repairs = detailed[['Inventory qty', 'Repair cost']]
    # Source: https://stackoverflow.com/questions/46306786/flatten-multi-index-pandas-dataframe-where-column-names-become-values/46306841
    repairs = repairs.groupby('Inventory qty').agg([np.median]).stack().reset_index()
    financials = pd.concat([financials, repairs['Repair cost']], axis=1)
    # Source: https://stackoverflow.com/questions/43290051/renaming-tuple-column-name-in-dataframe
    financials = financials.rename(columns={financials.columns[-1]: "Median repair cost"})
    financials['Total cost'] = financials['Acquisition cost'] + financials['Median repair cost']
    financials = financials.set_index('Inventory qty')
    detailed = detailed.drop(columns=['Repair cost'])
    wait_durations = detailed[['Inventory qty', 'min wait duration', 'median wait duration', 'max wait duration']]
    wait_durations = wait_durations.groupby('Inventory qty').agg([np.median])
    departures = detailed[['Inventory qty', 'Patrons today', 'Departed wait queue']]
    departures = departures.groupby('Inventory qty').agg([np.min, np.median, np.max])
    utils = [detailed[['Inventory qty']]]
    pats = [detailed[['Inventory qty']]]
    for hour in range(hours_open):
        utils.append(detailed['Utilization ' + str(hour+1)])
        pats.append(detailed['Patrons_waiting ' + str(hour+1)])
    utilization = pd.concat(utils, axis=1)
    utilization = utilization.groupby('Inventory qty').agg([np.min, np.median, np.max])
    patrons_waiting = pd.concat(pats, axis=1).groupby('Inventory qty').agg([np.max])
    return [detailed, financials, wait_durations, departures, patrons_waiting, utilization]


def main():
    """
    Requests user input for # days to simulate. Outputs results to CSV files.
    :return: None
    """
    try:
        days = int(input("How many days should the simulation run? "))      # 1 year=365; 4 years=1,460
        results = run_simulation([75, 150, 225, 300, 375], number_of_days=days)            # [75, 150, 225, 300, 375]
        folder = 'sample_output/'
        filenames = ['detailed_output.csv', 'financial_overview.csv', 'wait_durations_in_minutes.csv',
                     'patron_departures.csv', 'max_patrons_waiting_by_hour.csv', 'utilization_by_hour.csv']
        # Source: https://realpython.com/python-zip-function/#traversing-lists-in-parallel
        for df, output in zip(results, filenames):
            df.to_csv(folder + output)
    except ValueError:
        print("Please enter an integer. ")


if __name__ == '__main__':
    main()
