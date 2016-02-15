"""
Cookie Clicker Simulator
"""

# try:
#     import simpleplot
#     SIMPLEGUICS2PYGAME = False
#
# except ImportError:
#     import SimpleGUICS2Pygame.simpleplot as simpleplot
#     SIMPLEGUICS2PYGAME = True

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
#SIM_TIME = 320.0

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
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
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
               "Total no of cookies: "+str(self._total_cookies)

    def get_cookies(self):
        """
        Return current number of cookies (not total number of cookies)
        :rtype: float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS
        :rtype: float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time
        :rtype: float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list. Should be a list of tuples of the form: (time, item, cost of item, total cookies)
        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,so that they will not be modified outside of the class.
        Note that get_history should return a copy of the history list so that you are not returning a reference
        to an internal data structure. This will prevent broken strategy function from inadvertently messing up history
        :rtype: list
        """
        return self._history[:]

    def time_until(self, cookies):
        """
        Return num of seconds until you have the given numb of cookies(could be 0.0 if you already have enough cookies)
        You cannot wait for fractional seconds, so while you should return a float it should not have a fractional part.
        """
        if self.get_cookies() >= cookies:
            return 0.0
        else:
            return math.ceil((cookies - self.get_cookies()) / self.get_cps())
    
    def wait(self, time):
        """
        Wait for given amount of time and update state. Should do nothing if time <= 0.0
        This method should "wait" for the given amount of time. This means you should appropriately increase the time,
        the current number of cookies, and the total number of cookies.
        """
        if time <= 0:
            return
        else:
            self._current_time += time
            self._current_cookies += time * self._current_cps
            self._total_cookies += time * self._current_cps
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
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self.get_time(), item_name, cost, self._total_cookies))


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given duration with the given strategy.
    Returns a ClickerState object corresponding to the final state of the game.
    """
    #  Make a clone of the build_info object and create a new ClickerState object.
    my_object = build_info.clone()
    state_of_affairs = ClickerState()
    exitus = False

    # The function should then loop until the time in the ClickerState object reaches the duration of the simulation.
    while state_of_affairs.get_time() <= duration and not exitus:
        print "starting loop: current time:", state_of_affairs.get_time()

        # Check the current time and break out of the loop if the duration has been passed.
        # Call the strategy function with the appropriate arguments to determine which item to purchase next.
        item_to_purchase = strategy(state_of_affairs.get_cookies(), state_of_affairs.get_cps(),
                                    state_of_affairs.get_history(), duration - state_of_affairs.get_time(), my_object)
        print "strategy provides item:", item_to_purchase

        # If the strategy function returns None, you should break out of the loop, no more items will be purchased.
        if item_to_purchase is None:
            exitus = True
        else:
            # Determine how much time must elapse until it is possible to purchase the item.
            time_needed = state_of_affairs.time_until(my_object.get_cost(item_to_purchase))
            print "cost of item:", my_object.get_cost(item_to_purchase)
            print "current cps: ", state_of_affairs.get_cps()
            print "time needed: ", time_needed
            print

            # If you would have to wait past duration of simulation to purchase the item, you should end the simulation.
            if time_needed > duration - state_of_affairs.get_time():
                exitus = True
            else:
                # Wait until that time.
                state_of_affairs.wait(time_needed)
                # Buy the item.
                state_of_affairs.buy_item(item_to_purchase, my_object.get_cost(item_to_purchase),
                                          my_object.get_cps(item_to_purchase))
                print "Bought item."
                print state_of_affairs
                # Update the build information.
                my_object.update_item(item_to_purchase)
                print "Updated object."
                print "cps of object:", my_object.get_cps(item_to_purchase)
                print
    print "state of affairs before final wait:\n", state_of_affairs
    print "history:\n", state_of_affairs.get_history()
    print
    print "time left: ", duration - state_of_affairs.get_time()
    state_of_affairs.wait(duration - state_of_affairs.get_time())
    print
    print "state of affairs after final wait:\n", state_of_affairs
    print
    # print "trying to buy after final wait:"
    # items_available = []
    # for item in my_object.build_items():
    #     items_available.append(item)
    # print items_available
    # print type(items_available)
    # while items_available:
    #     max_cost = 0
    #     for item in items_available:
    #         print "item:", item, "cost:", my_object.get_cost(item)
    #         if my_object.get_cost(item) > max_cost:
    #             max_cost = my_object.get_cost(item)
    #             most_expensive = item
    #     print "most expensive:", most_expensive
    #     # check if cookies enough
    #     print "checking cookies"
    #     print "cookies available:", state_of_affairs.get_cookies()
    #     print "cost:", max_cost
    #     if state_of_affairs.get_cookies() < max_cost:
    #         items_available.remove(most_expensive)
    #         print "not enough,", most_expensive, "removed"
    #     else:
    #         # Buy the item.
    #         state_of_affairs.buy_item(most_expensive, my_object.get_cost(most_expensive),
    #                                   my_object.get_cps(most_expensive))
    #         # Update the build information.
    #         my_object.update_item(most_expensive)
    #         print most_expensive, "purchased"
    #
    #     print
    return state_of_affairs



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
    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)


def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    run_strategy("None", SIM_TIME, strategy_none)



#run()

# if SIMPLEGUICS2PYGAME:
#     simpleplot._block()
