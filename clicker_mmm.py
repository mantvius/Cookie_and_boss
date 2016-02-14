"""
Cookie Clicker Simulator
"""

try:
    import simpleplot
    SIMPLEGUICS2PYGAME = False

except ImportError:
    import SimpleGUICS2Pygame.simpleplot as simpleplot
    SIMPLEGUICS2PYGAME = True

import poc_clicker_provided as provided
import math

# Used to increase the timeout, if necessary
# try:
#     import codeskulptor
# except ImportError:
#     import SimpleGUICS2Pygame.codeskulptor as codeskulptor
# codeskulptor.set_timeout(20)


# Constants
SIM_TIME = 10000000000.0


class ClickerState:
    """
    Simple class to keep track of the game state.

    The ClickerState class must keep track of four things:
    The total number of cookies produced throughout the entire game (this should be initialized to 0.0).
    The current number of cookies you have (this should be initialized to 0.0).
    The current time (in seconds) of the game (this should be initialized to 0.0).
    The current CPS (this should be initialized to 1.0).

    Note that you should use floats to keep track of all state properties.
    During a simulation, upgrades are only allowed at an integral number of seconds as required in Cookie Clicker.
    However, the CPS value is a floating point number. In addition to this information, your ClickerState class must
    keep track of the history of the game. We will track the history as a list of tuples. Each tuple in the list will
    contain 4 values: a time, an item that was bought at that time (or None), the cost of the item, and the total number
    of cookies produced by that time. This history list should therefore be initialized as [(0.0, None, 0.0, 0.0)].
    """

    def __init__(self):
        self.total_cookies = 0.0
        self.current_cookies = 0.0
        self.current_time = 0.0
        self.current_cps = 0.0
        self.history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        This method should return the state (possibly without the history list) as a string in a human readable format.
        This is primarily to help you develop and debug your program. It will also be used by OwlTest
        in error messages to show you the state of your ClickerState object after you fail a test.

        """
        return "Current state of affairs:\n" \
               "Current no of cookies: "+str(self.get_cookies())+"\n" \
               "Current time: "+str(self.get_time())+"\n" \
               "Current CPS: "+str(self.get_cps())+"\n" \
               "Total no of cookies: "+str(self.total_cookies)

    def get_cookies(self):
        """
        Return current number of cookies (not total number of cookies)
        :rtype: float
        """
        return self.current_cookies
    
    def get_cps(self):
        """
        Get current CPS
        :rtype: float
        """
        return self.current_cps
    
    def get_time(self):
        """
        Get current time
        :rtype: float
        """
        return self.current_time
    
    def get_history(self):
        """
        Return history list. Should be a list of tuples of the form: (time, item, cost of item, total cookies)
        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,so that they will not be modified outside of the class.
        Note that get_history should return a copy of the history list so that you are not returning a reference
        to an internal data structure. This will prevent broken strategy function from inadvertently messing up history
        :rtype: list
        """
        return self.history[:]

    def time_until(self, cookies):
        """
        Return num of seconds until you have the given numb of cookies(could be 0.0 if you already have enough cookies)
        You cannot wait for fractional seconds, so while you should return a float it should not have a fractional part.
        """
        return math.floor((cookies - self.get_cookies()) / self.get_cps())
    
    def wait(self, time):
        """
        Wait for given amount of time and update state. Should do nothing if time <= 0.0
        This method should "wait" for the given amount of time. This means you should appropriately increase the time,
        the current number of cookies, and the total number of cookies.
        """
        if time <= 0:
            return
        else:
            self.current_time += time
            self.current_cookies += time * self.current_cps
            self.total_cookies += time * self.current_cps
            return
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state. You should appropriately adjust the current number of cookies, the CPS,
        and add an entry into the history.
        If a method is passed an argument that is invalid (such as an attempt to buy an item for which you
        do not have enough cookies),you should just return from the method without doing anything.
        """
        if self.get_cookies() < cost:
            return
        else:
            self.current_cookies -= cost
            self.current_cps += additional_cps
            self.history.append((self.get_time(), item_name, cost, self.total_cookies))

    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given duration with the given strategy.
    Returns a ClickerState object corresponding to the final state of the game.
    """

    # Replace with your code
    return ClickerState()


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly check whether it can actually buy a Cursor in the
    time left. Your simulate_clicker function must be able to deal with such broken strategies. Further, your
    strategy functions must correctly check if you can buy the item in the time left and return None if you can't.
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None


def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    return None


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    return None


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    return None

        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)


def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)


run()
if SIMPLEGUICS2PYGAME:
    simpleplot._block()
