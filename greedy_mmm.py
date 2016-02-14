"""
Simulator for greedy boss scenario
"""
import math

try:
    #import simplegui
    import simpleplot
    SIMPLEGUICS2PYGAME = False

except ImportError:
    #import SimpleGUICS2Pygame.simplegui as simplegui
    import SimpleGUICS2Pygame.simpleplot as simpleplot
    SIMPLEGUICS2PYGAME = True

# Used to increase the timeout, if necessary
# try:
#     import codeskulptor
# except ImportError:
#     import SimpleGUICS2Pygame.codeskulptor as codeskulptor
# codeskulptor.set_timeout(20)


STANDARD = True
LOGLOG = False

# constants for simulation
INITIAL_SALARY = 100
SALARY_INCREMENT = 100
INITIAL_BRIBE_COST = 1000


def greedy_boss(days_in_simulation, bribe_cost_increment, plot_type = STANDARD):
    """
    Simulation of greedy boss
    """
    # initialize necessary local variables
    current_day = 1
    current_salary = INITIAL_SALARY
    earnings = 1
    bribe_cost = INITIAL_BRIBE_COST
    money_at_hand = 0
    # define  list consisting of days vs. total salary earned for analysis
    days_vs_earnings = []

    # Each iteration of this while loop simulates one bribe
    while current_day <= days_in_simulation:
        
        # update list with days vs total salary earned
        # use plot_type to control whether regular or log/log plot
        if plot_type == STANDARD:
            days_vs_earnings.append((current_day, earnings))
        else:
            days_vs_earnings.append([math.log(current_day), math.log(earnings)])
        # check whether we have enough money to bribe without waiting
        while money_at_hand >= bribe_cost:
            money_at_hand -= bribe_cost
            current_salary += SALARY_INCREMENT
            bribe_cost += bribe_cost_increment
            # advance current_day to day of next bribe (DO NOT INCREMENT BY ONE DAY)
        day = current_day * 1
        if (bribe_cost - money_at_hand)%current_salary != 0:
            current_day += (bribe_cost - money_at_hand)/current_salary + 1
        else:
            current_day += (bribe_cost - money_at_hand)/current_salary
        # update state of simulation to reflect bribe
        money_at_hand += current_salary * (current_day - day)  # bribe_cost-money_at_hand
        earnings += current_salary * (current_day - day)  # bribe_cost-money_at_hand

    return days_vs_earnings


def run_simulations():
    """
    Run simulations for several possible bribe increments
    """
    plot_type = LOGLOG
    days = 150
    inc_0 = greedy_boss(days, 0, plot_type)
    inc_500 = greedy_boss(days, 500, plot_type)
    inc_1000 = greedy_boss(days, 1000, plot_type)
    inc_2000 = greedy_boss(days, 2000, plot_type)
    simpleplot.plot_lines("Greedy boss", 600, 600, "days", "total earnings",
                          [inc_0], False,
                         ["Bribe increment = 0"])

#run_simulations()


# print greedy_boss(35, 100)
# should print [(0, 0), (10, 1000), (16, 2200), (20, 3400), (23, 4600), (26, 6100), (29, 7900), (31, 9300), (33, 10900), (35, 12700)]

print greedy_boss(70, 0)
# should print [(0, 0), (10, 1000), (15, 2000), (19, 3200), (21, 4000), (23, 5000), (25, 6200), (27, 7600), (28, 8400), (29, 9300), (30, 10300), (31, 11400), (32, 12600), (33, 13900), (34, 15300), (34, 15300), (35, 16900)]

if SIMPLEGUICS2PYGAME:
    simpleplot._block()

# print greedy_boss(50, 1000)
#
# for d in range(51):
#     print "day:", d, ", slr:", 50*(d/10+1)*d

