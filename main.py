import rebalancing

# Input
target_weights = 'targetWeights_20230321.json'

# As per the PDF, we are hard-coding the positions class with zero units of inventory for each asset
init_positions = rebalancing.Positions( {"AAPL": 0.0, "TSLA": 0.0, "MSFT": 0.0} )
init_aum = 0.0

# Broker is initialized to the initial positions of zero
broker = rebalancing.Broker( initial_positions = init_positions, initial_aum = init_aum )

# Create the portfolio class which communicates and updates the broker class
portfolio = rebalancing.Portfolio(target_weights, broker)

# Rebalance the portfolio and save the output
portfolio.rebalance_portfolio( save_position = True )