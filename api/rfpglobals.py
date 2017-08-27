DEBUG = True

''' ROUTE '''
ROUTE_IPFS = '/ipfs'
ROUTE_DRFP = '/drfp'

''' DRFP params '''
DRFP_ACCOUNT = 'account'           # account address
DRFP_OWNER = 'manager'             # name of the manager
DRFP_NAME = 'name'                 # name of the contract
DRFP_WHITELIST = 'whitelist'
DRFP_PERIODS = 'periods'
DRFP_ADVERTISING = 'advertising'   # nested in periods
DRFP_BIDDING = 'bidding'           # nested in periods
DRFP_REVEAL = 'reveal'             # nested in periods
DRFP_AWARD = 'award'               # nested in periods
DRFP_FILE = 'file'                 # base64 encrypted file

''' smart contract params '''
SC_NAME = DRFP_NAME
SC_OWNER = DRFP_OWNER
SC_ADDR = 'managerAddress'
SC_LINK = 'specLink'
SC_PERIODS = DRFP_PERIODS
SC_BIDDING = DRFP_BIDDING
SC_REVEAL = DRFP_REVEAL
SC_AWARD = DRFP_AWARD
SC_WHITELIST = DRFP_WHITELIST

SC_OWNER_ADDR = 'ownerAddr'
SC_BIDDER_ADDR = 'bidderAddr'
SC_CONTRACT_ADDR = 'contractAddr'

SC_FILE = DRFP_FILE
