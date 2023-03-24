# rebalancing
Program which rebalances a portfolio of positions to a set of target allocations.

Solution to the Quantitative Strategist coding assignment.

The question asks to create a system that will correctly rebalance a portfolio of positions to respect
a target set of asset allocations. In my program, I am assuming that the initial position of the portfolio is provided
in the 'executedTrades_20230321.json' file.

Opening the file, we see that the initial positions are all short positions:

"AAPL": -238.24266869570647 & "TSLA": -522.6410456647545  & "MSFT": -1079.967091359672

The broker is initiated to hold zero units of each asset (as per the provided PDF). The program contains a class called 
'RebalancingSystem' which is responsible for loading in positions, pricing and rebalancing. The 'rebalance()' member function
performs the following:

1. Sets the target weights that we must allocate our assets with respect to (40/40/20 split).
2. Loads the current positions of the portfolio from 'executedTrades_20230321.json'.
3. Gets the live prices from the broker class (randomly generated).
4. Calculates the total dollar value of the portfolio.
5. Determines the correct positions that are required to respect the target weights.
6. Determines the adjustments required on the current positions (from step 2) in order to get the correct positions (from step 5).
7. The 'positions', 'aum' and 'portfolio_adjustments' values of the broker object are updated.

This function is called within the 'Portfolio' class member function 'rebalance_portfolio' which provides an option to save the outputs to a json file.
The program will save two files:

1. 'new_positions.json' :  This file contains the new positions after rebalancing.
2. 'trades_to_execute.json' : This file contains the adjustments that were made to 'executedTrades_20230321.json' in order to get the new positions.

The rebalancing can be done by simply running the 'main.py' script which imports all classes from the 'rebalancing.py' script.
