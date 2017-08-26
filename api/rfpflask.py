import ipfsapi                              # Peer to Peer distributed storage
import json

from flask import Flask, jsonify, request   # Python microframework
from flask_cors import CORS                 # Cross Origin Resource Sharing
from solc import compile_files              # Python wrapper for the Solidity compiler
from web3 import Web3, TestRPCProvider      # Python implementation of Web3 to interact with the blockchain

# flask server
app = Flask(__name__)

# cross origin resource sharing
CORS(app)

# testrpc
web3 = Web3(TestRPCProvider())

''' IPFS '''

ROUTE_IPFS='/ipfs'

@app.route(ROUTE_IPFS + '/upload')
def upload():
    FILE_NAME = ''

    api = ipfsapi.connect('127.0.0.1', 5001)
    result = api.add(FILE_NAME)

    return jsonify(result)

''' Web3 '''

ROUTE_DRFP='/drfp'

# DRFP params
DRFP_ACCOUNT='account'
DRFP_NAME='name'
DRFP_WHITELIST='whitelist'
DRFP_ENDPERIODS='endPeriods'
DRFP_ADVERTISING='advertisingStart'
DRFP_BIDDING='biddingStart'
DRFP_REVEAL='revealStart'
DRFP_AWARD='awardDate'
DRFP_FILE='file'

'''
	Return the DRFP parameters.

	- returns the DRFP parameters as a json string
'''
@app.route(ROUTE_DRFP + '/params')
def get_params():
	end_periods = {}
	end_periods[DRFP_ADVERTISING] = 'uint'
	end_periods[DRFP_BIDDING] = 'uint'
	end_periods[DRFP_REVEAL] = 'uint'
	end_periods[DRFP_AWARD] = 'uint'

	params = {}
	params[DRFP_ACCOUNT] = 'String'
	params[DRFP_NAME] = 'String'
	params[DRFP_WHITELIST] = '[String]'
	params[DRFP_ENDPERIODS] = end_periods
	params[DRFP_FILE] = 'file'

	return jsonify(params)

'''
	Fetch the existing owner.

	- returns an address to the owner
'''
@app.route(ROUTE_DRFP + '/account/owner')
def create_owner():
	return web3.eth.accounts[0]

'''
	Fetch an existing bidder.

	- returns an address to the bidder
'''
@app.route(ROUTE_DRFP + '/account/bidder/<int:id>')
def create_bidder(id):
	MIN_ID = 1
	MAX_ID = 9

	if id < MIN_ID:
		print('WARNING: %s is LESS THAN the min: %s' % (id, MIN_ID))
		return web3.eth.accounts[MIN_ID]

	if id > MAX_ID:
		print('WARNING: %s is GREATER THAN the max: %s' % (id, MAX_ID))
		return web3.eth.accounts[MAX_ID]

	return web3.eth.accounts[id]


# TODO dummy endpoint
@app.route(ROUTE_DRFP + '/create', methods=['POST'])
def create_drfp():
	return jsonify(request.data)

'''
@app.route(ROUTE_DRFP + '/create', methods=['POST'])
def create_drfp():

    # the smart contract
    CONTRACT_NAME = 'drfp'
    FILE_NAME = CONTRACT_NAME + '.sol'

    DEPLOY_COST = 4000000

    # compile the sol file
    COMPILED = compile_files([FILE_NAME])
    RFP = COMPILED[FILE_NAME + ':' + CONTRACT_NAME]
    RFPContract = web3.eth.contract(
        abi = RFP['abi'],
        bytecode = RFP['bin'],
        bytecode_runtime = RFP['bin-runtime']
    )

    # get ipfs hash for spec and template

    # extract args from request
    owner_addr = request.form[DRFP_ACCOUNT]
    args = get_args(request.form)

    # deploy the contract to the blockchain
    trans_hash = CONTRACT.deploy(
        args=args, #['hello bobby boy']
        transaction={'from':owner_addr, 'gas':DEPLOY_COST}
    )

    # fetch the instance of the contract
    trans_receipt = web3.eth.getTransactionReceipt(trans_hash)
    contract_addr = trans_receipt['contractAddress']
    rfc_contract = RFPContract(contract_addr)

    RESULT = rfc_contract.call(
        {'from': web3.eth.coinbase}
    )

    return jsonify(RESULT)
'''

'''
	Construct the args from the given params for the contract.

	- params: the drfp params (see get_params)

	- returns the args as a [String]
'''
def get_args(params):
	# whitelist = params[DRFP_WHITELIST] # ??
	return [
		params[DRFP_NAME],
		params[DRFP_ENDPERIODS],
		params[DRFP_ADVERTISING],
		params[DRFP_BIDDING],
		params[DRFP_REVEAL],
		params[DRFP_AWARD]
	]

'''
	Get the IPFS hash from the given file.

	- file: The file to be added to IPFS

	- returns the IPFS hash
'''
def get_ipfs_hash(file):
	return upload()['hash']

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
