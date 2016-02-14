"""
Example comparisons of growth rates
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

STANDARD = True
LOGLOG = False

# constants for simulation
INITIAL_SALARY = 100
SALARY_INCREMENT = 100
INITIAL_BRIBE_COST = 1000


def f(n):
    """
    A test function
    """
    #return 0.1 * n ** 3 + 20 * n
    return 1000 * n

def g(n):
    """
    A test function
    """
    #return n ** 3
    #return 20 * n ** 2
    #return .1 * n ** 4
    return (n-1) * 1.15


def make_plot(fun1, fun2, plot_length):
    """
    Create a plot relating the growth of fun1 vs. fun2
    """
    answer = []
    for index in range(10, plot_length):
        answer.append([index, fun1(index) / float(fun2(index))])
    simpleplot.plot_lines("Growth rate comparison", 300, 300, "n", "f(n)/g(n)", [answer])

# create an example plot
make_plot(f, g, 10000)





def greedy_boss(days_in_simulation, bribe_cost_increment, plot_type = STANDARD):
    """
    Simulation of greedy boss
    """

    # initialize necessary local variables
    current_day = 1
    current_savings = 0
    total_salary_earned = 1
    current_bribe_cost = INITIAL_BRIBE_COST
    current_salary = INITIAL_SALARY

    # define  list consisting of days vs. total salary earned for analysis
    days_vs_earnings = []

    # Each iteration of this while loop simulates one bribe
    while current_day <= days_in_simulation:

        # update list with days vs total salary earned
        # use plot_type to control whether regular or log/log plot
        if plot_type == STANDARD:
            days_vs_earnings.append((current_day, total_salary_earned))
        else:
            print current_day, total_salary_earned
            days_vs_earnings.append([math.log(current_day), math.log(total_salary_earned)])

        # check whether we have enough money to bribe without waiting
        if current_savings >= current_bribe_cost:
            days_to_next_bribe = 0
        else:
            time_to_next_bribe = (current_bribe_cost - current_savings) / float(current_salary)
            days_to_next_bribe = int(math.ceil(time_to_next_bribe))

        # advance current_day to day of next bribe (DO NOT INCREMENT BY ONE DAY)
        current_day += days_to_next_bribe

        # update state of simulation to reflect bribe
        current_savings += days_to_next_bribe * current_salary
        current_savings -= current_bribe_cost
        total_salary_earned += days_to_next_bribe * current_salary
        current_bribe_cost += bribe_cost_increment
        current_salary += SALARY_INCREMENT

    return days_vs_earnings


def c(d):

    #return 9.5 * d ** 4
    #return math.exp(0.095*d)
    #return 95 * d ** 2
    return math.exp(9.5*d)


def boss(days):
    return greedy_boss(days, 0, LOGLOG)[1]


# def make_plot(fun1, fun2, plot_length):
#     """
#     Create a plot relating the growth of fun1 vs. fun2
#     """
#     answer = []
#     points = [[2.30258509299, 6.90775527898], [2.7080502011, 7.60090245954], [2.94443897917, 8.07090608879], [3.04452243772, 8.2940496401], [3.13549421593, 8.51719319142], [3.21887582487, 8.73230457103], [3.295836866, 8.93590352627], [3.33220451018, 9.03598698483], [3.36729582999, 9.13776967914], [3.40119738166, 9.23989917422], [3.43398720449, 9.34136863438], [3.4657359028, 9.44145209294], [3.49650756147, 9.53964411912], [3.52636052462, 9.63560810738], [3.52636052462, 9.63560810738], [3.55534806149, 9.73506890091]]
#
#     for point in points:
#         answer.append([point[0], point[1] / float(fun2(point[0]))])
#     simpleplot.plot_lines("Growth rate comparison", 300, 300, "n", "boss(n)/c(n)", [answer])
#
#     #simpleplot.plot_lines("Greedy boss", 600, 600, "days", "total earnings", [inc_0])
#
#
# # create an example plot
# make_plot(boss, c, 100)

if SIMPLEGUICS2PYGAME:
    simpleplot._block()
