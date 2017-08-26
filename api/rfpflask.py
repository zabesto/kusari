import ipfsapi                           # Peer to Peer distributed storage
import json

from flask import Flask, jsonify         # Python microframework
from solc import compile_files           # Python wrapper for the Solidity compiler
from web3 import Web3, TestRPCProvider   # Python implementation of Web3 to interact with the blockchain

app = Flask(__name__)

''' IPFS '''

@app.route('/ipfs/upload')
def upload():
    FILE_NAME = ''

    api = ipfsapi.connect('127.0.0.1', 5001)
    result = api.add(FILE_NAME)

    return jsonify(result)

''' Web3 '''

# DRFP params
DRFP_ACCOUNT='account'
DRFP_NAME='name'
DRFP_WHITELIST='whitelist'
DRFP_ENDPERIODS='endPeriods'
DRFP_ADVERTISING='advertisingStart'
DRFP_BIDDING='biddingStart'
DRFP_REVEAL='revealStart'
DRFP_AWARD='awardDate'
DRFP_SPEC='spec'
DRFP_TEMPLATE='template'

'''
	Return the DRFP parameters.

	- returns the DRFP parameters as a json string
'''
@app.route('/drfp/params')
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
	params[DRFP_SPEC] = 'file'
	params[DRFP_TEMPLATE] = 'file'

	return jsonify(params)

'''
@app.route('/drfp/create', method=['POST'])
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
