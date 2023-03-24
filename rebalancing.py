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
    def __init__(self, initial_positions: Positions, initial_aum: float):
        self.positions: Positions = initial_positions
        self.aum: float = initial_aum
        self.portfolio_adjustments: Positions = Positions({})
    
    def get_live_price(self) -> dict[str, float]:
        prices = { asset: np.random.uniform(10,30) for asset in self.positions.get_universe() }
        return prices
    
    def get_positions(self) -> Positions:
        return self.positions
    
    def save(self):
        self.positions.save(filename = 'new_positions')
        self.portfolio_adjustments.save(filename = 'trades_to_execute')

    def execute_trades(self, execution_positions: Positions) -> None:
        pass

# =============================================================================================================================================== #

# Simple class to load positions from JSON files
class LoadPositions():
    def __init__(self, json_file: str):
        self.filename: str = json_file
    
    def initialize(self) -> dict[str, float]:
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                logging.info("Initial positions successfully loaded.")
                return json.load(file)
        else:
            return None

# =============================================================================================================================================== #

class RebalancingSystem():
    def __init__(self, target_allocations_json: str, broker_object: Broker):
        self.target: str = target_allocations_json
        self.broker: Broker =  broker_object
        self.date: str = self.target[14:-5]
        self.init_positions_filename: str = 'executedTrades'

        # Initialize the logger
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler('execution_log_' + self.date + '.txt')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        logging.getLogger('').addHandler(file_handler)
        logging.info(" ** =========== NEW LOG BEGIN =========== ** " )
    
    # Initialize the target allocation (in %)
    def set_targets(self) -> dict[str, float]:

        # We are assuming the file is in the same directory
        if os.path.exists(self.target):
            with open(self.target, 'r') as file:
                self.target_weights = json.load(file)
                logging.info("Target allocations successfully loaded.")
                self.update_logger(self.target_weights)
                
        else:
            # File does not exist, exit the program
            logging.error("Could not load current positions. File '" +  self.target +"' not found.")
            quit()

    # Load in our current positions
    def get_current_positions(self) -> dict[str, float]:
        
        # Ensures the target weights and executed trades have the same date 
        filename = self.init_positions_filename + '_' + self.date
        self.current_positions = LoadPositions(filename + '.json').initialize()

        # Make sure the appropriate file exists
        if self.current_positions is None:
            logging.error("Could not load current positions. File not found.")
            quit()
        else:
            # Update the logger with the initial position from the file
            self.update_logger(self.current_positions)
    
    # Update logger with dictionary keys
    def update_logger( self, dictionary: dict[str, float] ):
        for key in dictionary.keys(): logging.info( key + " : " + str(dictionary[key]) )

    # Rebalances the portfolio and modifies the broker object in place.
    def rebalance(self):
        
        # Generate the target allocations
        self.set_targets()

        # Load the current positions
        self.get_current_positions()

        # Get the live prices from the broker
        prices = self.broker.get_live_price()
        logging.info("Current asset prices:")
        self.update_logger(prices)

        # Calculate the total dollar value
        total_value = sum( prce * units for (prce, units) in zip(prices.values(), self.current_positions.values()) )

        # Compute the amount to be allocated to each asset
        target_values = {}
        logging.info("Target positions established.")
        for key in self.target_weights.keys():
            
            # Dollar amount for target
            asset_dollar_value = self.target_weights[key] * total_value

            # The required number of assets to satisfy the target weights
            target_values[key] = asset_dollar_value / prices[key]
            logging.info( key + " target position : " + str(target_values[key]) )
        
        # Trades required to hit target allocation
        logging.info("Required adjustments to be executed.")
        adjustments_required = { asset : trgt - crnt for (asset,trgt, crnt) in zip(self.target_weights.keys(),target_values.values(), self.current_positions.values()) }
        self.update_logger(adjustments_required)

        # Update the broker class
        self.broker.positions = Positions(target_values)
        self.broker.portfolio_adjustments = Positions(adjustments_required)
        self.broker.aum = sum( prce * units for (prce, units) in zip(prices.values(), target_values.values()) )

# =============================================================================================================================================== #

# Class to handle portfolio actions
class Portfolio():
    def __init__(self, target_allocations_json: str, broker_object: Broker):
        self.target: str = target_allocations_json
        self.broker: Broker = broker_object
    
    def get_current_position(self):
        return self.broker.get_positions()

    def rebalance_portfolio(self, save_position: bool = True):
        RebalancingSystem(self.target, self.broker).rebalance()
        if save_position is True:
            self.broker.save()

# =============================================================================================================================================== #
