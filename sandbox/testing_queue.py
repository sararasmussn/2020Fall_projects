# # """
# # https://pymotw.com/2/Queue/
# # """
# # import miller_ranum as mr
# # import queue
# #
# # hours_open = 10
# # minutes_open = hours_open * 60
# #
# # q = queue.Queue(maxsize=90)
# #
# # for i in range(minutes_open):
# #     if i < 60:
# #         q.put(i)
# #     elif i < (60*2):
# #         q.put(i)
# #     elif i < (60*3):
# #         q.put(i)
# #     elif i < (60*4):
# #         q.put(i)
# #     elif i < (60*5):
# #         q.put(i)
# #     elif i < (60*6):
# #         q.put(i)
# #     elif i < (60*7):
# #         q.put(i)
# #     elif i < (60*8):
# #         q.put(i)
# #     elif i < (60*9):
# #         q.put(i)
# #     else:
# #         q.put(i)
# #
# # while not q.empty(): # While not True
# #     print(q.get())
# #
# #
# #
# #
# #
# #
# #     # People get into the computer use queue THROUGHOUT today's open hours.
# #     # patron_joins_queue()
# #         # Note: What is the minute they got in queue?
# #         # Check - is a computer available? (Is # of computers avail > 0?)
# #         # If yes:
# #             # dequeue to use the computer.
# #             # New availability = Number of computers available - 1
# #             # Note: What is the minute they got a computer?
# #         # Else, wait:
# #             # Is this a "while a computer is not available, check every 2 minutes" situation?
# #     # Time elapses, the day ends.
# #     # Anyone still in the queue gets booted, make note of this. Combine with above = # patrons who left the queue today.
# #
# #
# #
# #     computerQueue = mr.Queue()
# #     wait_times = []
# #     one_day = 480     # 8 hours * 60 = Minutes that library is open
# #     for one_minute in range(one_day):
# #
# #         if mr.new_person():
# #             session = one_minute    # The minute at which the session starts
# #             computerQueue.enqueue(session)
# #
# #             # if someone comes,
# #                 # number of computers available = number of computers available - 1, for the length of 1 hour
# #             #print(session)
# #         # if not computerQueue.isEmpty():     # If computer Queue is not empty
# #         #     nexttask = computerQueue.dequeue()
# #         #     wait_times.append(nexttask.waitTime(one_minute))
# #
# #
# #
# # def run_one_day_v2(fleet):
# #     """
# #     The patron queue is empty to start.
# #     Add patrons to the queue of people wanting to use a computer - attribute of time added.
# #     If there is a computer available, assign the person to an open computer.
# #
# #     Patron's reservation length is an attribute of the patron.
# #     - Keep track of WHEN they got in the queue
# #     - If a patron has to wait more than 30 minutes, they will leave queue. Make note of it.
# #     :return:
# #     """
# #     waitcount = 0
# #     total_patrons_today = set_total_patrons_count()
# #     computers_available = determine_fleet_availability(fleet)
# #     test_q = queue.Queue(maxsize=computers_available)
# #     for hour in range(10):
# #         p = patrons_per_hour(total_patrons_today, hour)
# #         for patron in range(p):
# #             test_q.put(hour)
# #             if test_q.qsize() >= computers_available:
# #                 waitcount += 1
# #         for patron in range(p):
# #             test_q.get()
# #     print("total who waited:", waitcount)
#
# import numpy as np
# n = np.arange(0,600)
# for x in n:
#     if x in range(59,600,60):
#         print(x)
#
#
#
# # TODO: In current design, it's possible for patrons arriving at the end of the day to be assigned a computer before they arrive
#     last_patron_arrival = patron_df['Arrival_minute'].max()
#     last_minute = (hours_open * 60) - 1
#     neg_waits = patron_df[patron_df['Wait_duration'] < 0]
#     if len(neg_waits) > 1:
#         patron_df.iat[-1,1] = np.nan
#     if (last_minute - last_patron_arrival) < 15:
#         # Basically delete the people who arrive in last few minutes?
#         patron_df.iat[-1,1] = np.nan
#         patron_df.iat[-1,3] = np.nan
#         patron_df.iat[-1,-1] = np.nan
#
#
#
#     # Source: https://stackoverflow.com/questions/35019156/pandas-format-column-as-currency
#     # results[1] = results[1].apply(format_currency)
#     # print(results[1])
#
#
#     # Cost format: ${:,.2f}
#     # Percent format: {:2.2%}
#     # Big number format: {:,}
#
#     # def format_currency(value):
#     #     """
#     #
#     #     :param value:
#     #     :return:
#     #     """
#     #     return "${:,.2f}".format(value)
#     #
#     # def format_percentage(value):
#     #     """
#     #
#     #     :param value:
#     #     :return:
#     #     """
#     #     return "{:2.2%}".format(value)

comps_free = 1
patrons_this_minute = 2

while comps_free > 0:
    print("help!")
    comps_free -= 1
