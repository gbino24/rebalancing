import rebalancing as rb

# Input
target_weights = 'targetWeights_20230321.json'

# As per the PDF, we are hard-coding the positions class with zero units of inventory for each asset
init_positions = rb.Positions( {"AAPL": 0, "TSLA": 0, "MSFT": 0} )

# If the portfolio has zero units in each asset, we have to allocate an amount (in $) of capital to invest asset allocation split.
# If the portfolio has non-zero units, the cash variable is ignored.
cash = 1000

# Broker is initialized to the initial positions of zero
broker = rb.Broker( initial_positions = init_positions )

# Create the portfolio class which communicates and updates the broker class
portfolio = rb.Portfolio( target_weights, broker, cash )

# Rebalance the portfolio
portfolio.rebalance_portfolio()

# Save the trades
portfolio.save_trades()