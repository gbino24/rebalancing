# rebalancing
Program which rebalances a portfolio of positions to a set of target allocations.

Quantitative Strategist Coding Assignment.

The question asks to create a system that will correctly rebalance a portfolio of positions to respect
a target set of asset allocations. In my program, I am assuming that the initial position of the portfolio is zero in each asset class.

"AAPL": 0.0 & "TSLA": 0.0  & "MSFT": 0.0

In order to perform the portfolio rebalance, we need to include a dollar amount to the portfolio value to invest (if we have zero units in each asset, the portfolio value = 0). So, we included an additional variable 'cash' which is used for the allocation when the sum of asset values is zero. For non-zero asset values, the 'cash' variable is ignored.

The program contains a class called 'RebalancingSystem' which is responsible for loading in positions, pricing and rebalancing. The 'rebalance()' member function performs the following:

1. Sets the target weights that we must allocate our assets with respect to (40/40/20 split).
2. Loads the current positions of the portfolio from the broker.
3. Gets the live prices from the broker class (randomly generated).
4. Calculates the total dollar value of the portfolio.
5. If the dollar value of the portfolio is zero, utilize the cash to hit targets.
6. Determines the correct positions that are required to hit the target weights.
7. Determines the adjustments required on the current positions (from step 2) in order to get the correct positions (from step 5).
8. The 'positions', and 'trades' values of the broker object are updated.

This function is called within the 'Portfolio' class member function 'rebalance_portfolio' 

We then save the outputs to a json file using the 'save_trades' function.
- 'trades_to_execute.json' : This file contains the adjustments that were made to the current position in order to hit the target weights.

The rebalancing can be done by simply running the 'main.py' script which imports all classes from the 'rebalancing.py' script.
