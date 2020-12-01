"""
Monte Carlo simulation of library computer utilization
Sara Rasmussen (saralr2)
IS597PR
Fall 2020
"""
import random
import queue    # https://docs.python.org/3/library/queue.html


def determine_fleet_availability(total_inventory: int, weight=4) -> int:
    """
    RANDOMIZED VARIABLE: Given the number of computers in your fleet, calculate out-of-service count, return the number of computers in service today.
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
    likely_case = .04
    worst_case = random.uniform(.19, .33)
    # Simple PERT estimate = (a + 4b + c)/6
    pct_out = (best_case + (weight * likely_case) + worst_case)/(weight+2)
    out_of_service = (total_inventory * pct_out)
    todays_inventory = total_inventory - int(out_of_service)
    return todays_inventory


def select_reservation_length() -> int:
    """
    RANDOMIZED VARIABLE
    For one computer reservation, randomly select the reservation length:
    Options for length of use selected by the patrons: 15 or 1 hour.
    Discrete distribution between two options. Not 50/50. Probably skewed more like 25/75.
    Computer use policy:
    After each computer use, there will be a 15-minute delay (where the computer is unavailable to be used)
        so that staff can sanitize the area per the library’s COVID-19 cleaning procedures.

    :return: The length of time + 15min delay, measured in hours (.50 or 1.25)
    """
    return 1


def set_total_patrons_count():
    """
    RANDOMIZED variable, based on Chicago Public Library data (min=514, max=949)
    Set the number of patrons for 1 day.
    :return:
    """
    patron_count = random.randrange(514, 949)
    return patron_count


def patrons_per_hour(total_patrons, hour):
    """
    Depending on the hour, set the number of patrons entering the queue.
    Discrete probability distribution of patrons being added, based on Seattle Public Library data.
    Note: Demand for computers != use of computers, but we only have data measuring use.
    >>> patrons_per_hour(949, 10)
    33
    >>> patrons_per_hour(514, 15)
    114
    """
    if hour == 0:
        patrons = total_patrons * 0.035010
    elif hour == 1:
        patrons = total_patrons * 0.045726
    elif hour == 2:
        patrons = total_patrons * 0.055542
    elif hour == 3:
        patrons = total_patrons * 0.136442
    elif hour == 4:
        patrons = total_patrons * 0.165399
    elif hour == 5:
        patrons = total_patrons * 0.223067
    elif hour == 6:
        patrons = total_patrons * 0.199427
    elif hour == 7:
        patrons = total_patrons * 0.088998
    elif hour == 8:
        patrons = total_patrons * 0.047607
    elif hour == 9:
        patrons = total_patrons * 0.002781
    else:
        patrons = 0
    return int(patrons)


def run_one_day_v2(fleet):
    """
    The patron queue is empty to start.
    Add patrons to the queue of people wanting to use a computer - attribute of time added.
    If there is a computer available, assign the person to an open computer.

    Patron's reservation length is an attribute of the patron.
    - Keep track of WHEN they got in the queue
    - If a patron has to wait more than 30 minutes, they will leave queue. Make note of it.
    :return:
    """
    waitcount = 0
    total_patrons_today = set_total_patrons_count()
    computers_available = determine_fleet_availability(fleet)
    test_q = queue.Queue(maxsize=computers_available)
    for hour in range(10):
        p = patrons_per_hour(total_patrons_today, hour)
        for patron in range(p):
            test_q.put(hour)
            if test_q.qsize() >= computers_available:
                waitcount += 1
        for patron in range(p):
            test_q.get()
    print("total who waited:", waitcount)


def run_one_day(fleet):
    """
    Simulate one day at the library.

    Questions to answer, within 1 day:
    - How many computers were in service today?
    - How many computers were utilized today, out of those in service? (# used / # available, not # in fleet)
    - How long did patrons wait to use a computer? (Keep track of time elapsed in queue, save all of this - not just the average)
    - How many patrons left the queue because of the wait?

    :return:
    # """
    # Determine how many computers are in service today.
    computers_available = determine_fleet_availability(fleet)

    # Super basic test
    daily_results = {"Computers Available" : computers_available, "Utilization": [], "Users Waiting":[]}
    total_demand_by_hour = []
    wait_count_by_hour = []
    hours_open = 10
    waiting = 0

    for minute in range(hours_open * 60):
        users = random.randrange(0,300) + waiting
        if users > computers_available:
            waiting = users - computers_available
            utilization = computers_available/computers_available
        else:
            waiting = 0
            utilization = users/computers_available
        total_demand_by_hour.append(users)
        wait_count_by_hour.append(waiting)
        daily_results['Utilization'].append(utilization)
        daily_results['Users Waiting'].append(waiting)
    return daily_results


def run_simulation(inventory_qtys: list, number_of_days: int= 1):
    """
    Run as many days of simulation as specified. Collect all the stats. Return a summary to console.
    This function does not return anything.

    Summary questions to answer:
    - What was the total cost of the service provided?
        (# devices * price of device) + (max(# devices unavailable) * repair fee)
    - What was the average utilization rate (# used / # available) for all simulations run?
    - What was the average wait time for all sims run?
    - What was the average # of drop-offs (people who left because they waited longer than 30 minutes) for all sims run?

    From this, the user can discern: How many computers should we buy?

    :param number_of_days: 1 year=365; 4 years=1,460
    :param inventory_qtys: A list of devices to
    :return:
    """
    print("Running simulation of", number_of_days, "days...\n")

    # Your average Chromebook price
    device_cost = 375

    avg_cost = []
    avg_util = []
    users_waiting = []

    # Run the simulation once for each device count
    for number_of_devices in inventory_qtys:
        # Acquisition is a fixed cost based on the number of devices in inventory
        acquisition_cost = (number_of_devices * device_cost)

        # Run the simulation the specified # times
        for days in range(number_of_days):
            # Call the single simulation
            single_simulation = run_one_day(number_of_devices)

            # Determine the total repair cost for n simulations run
            # Repair fee: $95 (2 hours to collect, re-image, return a computer * median(DOIS help desk tech $40-55/hr wage)) (Source: Chicago Data Portal)
            repair_cost = ((number_of_devices - single_simulation['Computers Available']) * 95)
            total_cost = acquisition_cost + repair_cost
            avg_cost.append(total_cost)

            # Determine utilization for n simulations run
            utilization = sum(single_simulation['Utilization'])/len(single_simulation['Utilization'])
            avg_util.append(utilization)

            # Determine avg wait time over n simulations run
            users_waiting.append(sum(single_simulation['Users Waiting']))

        total_waiting = sum(users_waiting)
        final_cost = sum(avg_cost)/len(avg_cost)
        final_util = sum(avg_util)/len(avg_util)
        print("# Devices: {}\nAvg cost: ${:,.2f}\tAvg util: {:2.2%}\t Total users who waited: {:,}\n".format(number_of_devices, final_cost, final_util, total_waiting))

        # Clear these variables at the end of each loop
        avg_util = []
        avg_cost = []
        users_waiting = []


def main():
    """
    Put all editable bits here.

    :return: Results of program
    """
    # TODO: Convert to user input
    # n = input("How many days should the simulation run? ")
    n = 1460
    run_simulation([20, 80, 120, 160, 200], number_of_days=n)


if __name__ == '__main__':
    main()

