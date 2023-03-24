import numpy as np
import logging
import json
import os

# =============================================================================================================================================== #

class Positions:
    def __init__ (self , positions: dict[str, float]): 
        self._pos = positions
    
    def get_universe(self) -> list[str]: 
        return list(self._pos.keys())
    
    # Used to save a position to JSON file
    def save(self, filename):
        with open( filename + ".json", "w") as f:
            json.dump(self._pos, f)
            logging.info("Output saved as '" + filename + ".json'" )

# =============================================================================================================================================== #

class Broker:
    def __init__(self, initial_positions: Positions, initial_aum: float = 0.0):
        self.positions: Positions = initial_positions
        self.aum: float = initial_aum       # not used
        self.trades: Positions = Positions({})

        # Seed
        np.random.seed(100)
    
    def get_live_price(self) -> dict[str, float]:
        prices = { asset: np.random.uniform(10,30) for asset in self.positions.get_universe() }
        return prices
    
    def get_positions(self) -> Positions:
        return self.positions
    
    def save(self):
        # self.positions.save(filename = 'new_positions')     -- New positions
        self.trades.save(filename = 'trades_to_execute')

    def execute_trades(self, execution_positions: Positions) -> None:
        pass

# =============================================================================================================================================== #

class RebalancingSystem():
    def __init__(self, target_allocations_json: str, broker_object: Broker):
        self.target: str = target_allocations_json
        self.broker: Broker =  broker_object
        self.date: str = self.target[14:-5]

        # Initialize the logger
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler('execution_log_' + self.date + '.txt')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        logging.getLogger('').addHandler(file_handler)
        logging.info("** =========== NEW LOG BEGIN ============ ** " )
    
    # Update logger with dictionary keys
    def update_logger( self, dictionary: dict[str, float] ):
        for key in dictionary.keys(): logging.info( key + " : " + str(dictionary[key]) )

    # Initialize the target allocation (in %)
    def set_targets(self) -> dict[str, float]:
        # We are assuming the file is in the same directory
        if os.path.exists(self.target):
            with open(self.target, 'r') as file:
                self.target_weights = json.load(file)
                logging.info("== Target allocations successfully loaded ==")
                self.update_logger(self.target_weights) 
        else:
            # File does not exist, exit the program
            logging.error("Could not load current positions. File '" +  self.target + "' not found.")
            quit()

    # Load in our current positions
    def get_current_positions(self) -> dict[str, float]:
        self.current_positions = self.broker.get_positions()._pos
        logging.info("== Current positions successfully loaded ==")
        self.update_logger(self.current_positions)
    
    # Rebalances the portfolio and modifies the broker object in place.
    def rebalance(self, cash_to_invest: float):
        
        # Generate the target allocations
        self.set_targets()

        # Load the current positions
        self.get_current_positions()

        # Get the live prices from the broker
        prices = self.broker.get_live_price()
        logging.info("== Current asset prices (in $) ==")
        self.update_logger(prices)

        # Calculate the total dollar value
        total_value = sum( prce * units for (prce, units) in zip(prices.values(), self.current_positions.values()) )

        # If the portfolio asset value is zero, use 'cash_to_invest' to reach the target allocations.
        if total_value == 0 and cash_to_invest != 0:
            total_value = cash_to_invest
        # Avoid 'ZeroDivisionError'. If we have zero units in each asset, we need additional capital to reach target allocations.
        elif total_value == 0 and cash_to_invest == 0:
            logging.error("Cannot allocate assets. Portfolio value is zero.")
            quit()

        # Compute the amount to be allocated to each asset
        target_values = {}
        logging.info("== Target positions established ==")
        for key in self.target_weights.keys():
            
            # Dollar amount for target
            asset_dollar_value = self.target_weights[key] * total_value

            # The required number of assets to satisfy the target weights
            target_values[key] = asset_dollar_value / prices[key]
            logging.info( key + " target position : " + str(target_values[key]) + " (" + str(100 *asset_dollar_value/total_value)[:4] + "%)")
        
        # Trades required to hit target allocation
        logging.info("== Required trades to be executed ==")
        adjustments_required = { asset : trgt - crnt for (asset,trgt,crnt) in zip(self.target_weights.keys(),target_values.values(),self.current_positions.values()) }
        self.update_logger(adjustments_required)

        # Update the positions in broker class
        self.broker.positions = Positions(target_values)
        self.broker.trades    = Positions(adjustments_required)

# =============================================================================================================================================== #

# Class to handle portfolio actions
class Portfolio():
    def __init__(self, target_allocations_json: str, broker_object: Broker, cash_to_invest: float):
        self.target: str = target_allocations_json
        self.broker: Broker = broker_object
        self.cash_to_invest: float = cash_to_invest
    
    def rebalance_portfolio(self):
        RebalancingSystem(self.target, self.broker).rebalance(self.cash_to_invest)
    
    def save_trades(self):
        self.broker.save()

# =============================================================================================================================================== #
