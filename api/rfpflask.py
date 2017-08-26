import base64
import ipfsapi                              # Peer to Peer distributed storage
import json
import time

from flask import Flask, jsonify, request   # Python microframework
from flask_cors import CORS                 # Cross Origin Resource Sharing
from solc import compile_files              # Python wrapper for the Solidity compiler
from web3 import Web3, TestRPCProvider      # Python implementation of Web3 to interact with the blockchain

DEBUG = True

# flask server
app = Flask(__name__)

# cross origin resource sharing
CORS(app)

# testrpc
web3 = Web3(TestRPCProvider())

''' IPFS '''

HOST_IPFS = '127.0.0.1'
PORT_IPFS = 5001

ROUTE_IPFS='/ipfs'

ipfs = ipfsapi.connect(HOST_IPFS, PORT_IPFS)

def upload(file):
	BASE64_PREFIX = 'data:text/markdown;base64,'
	base64_file = file.replace(BASE64_PREFIX)
	result = ipfs.add(base64.b64decode(file))

	return jsonify(result)

''' Web3 '''

ROUTE_DRFP='/drfp'

# DRFP params
DRFP_ACCOUNT='account'
DRFP_OWNER='owner'
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
	params[DRFP_OWNER] = 'String'
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

'''
	Returns the request data.

	- returns the request data
'''
@app.route(ROUTE_DRFP + '/create/dummy', methods=['POST'])
def create_drfp_dummy():
	return jsonify(request.data)

'''
	Create a new DRFP.a


	- returns the results

'''
'''
@app.route(ROUTE_DRFP + '/create', methods=['POST'])
def create_drfp():
	DEPLOY_COST = 4000000

    # extract args from request
	printd('extracting args...')
	owner_addr = request.form[DRFP_ACCOUNT]
	args = get_args(request.data)

    # deploy the contract to the blockchain
	trans_hash = DRFPContract.deploy(
        args=args,
        transaction={'from':owner_addr, 'gas':DEPLOY_COST}
    )

    # fetch the instance of the contract
	trans_receipt = web3.eth.getTransactionReceipt(trans_hash)
	contract_addr = trans_receipt['contractAddress']
	rfc_contract = DRFPContract(contract_addr)

	RESULT = rfc_contract.call(
        {'from': web3.eth.coinbase}
    )

	return jsonify(RESULT)
'''

@app.route(ROUTE_DRFP + '/contract/dummy')
def get_contract_dummy():
	data = {}
	data['name'] = 'Contruct12'
	data['manager'] = 'rishabh'
	data['managerAddress'] = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNA3DQEBAQUAA4GNqGKukO1De7zhZj6+H0q'
	data['specLink'] = 'https://www.google.com/'

	periods = {}
	periods['bidding'] = int(round(time.time() * 1000))
	periods['reveal'] = int(round(time.time() * 1000))
	periods['award'] = int(round(time.time() * 1000))
	data['periods'] = periods

	whitelist = []
	whitelist.append("MIGfMA0GCSqGSIb")
	whitelist.append("3DQEBAQUAA4GN")
	whitelist.append("3DQEBAQUAA4GN")
	whitelist.append("ukO1De7zhZj6+")

	data['whitelist'] = whitelist

	return jsonify(data)

@app.route(ROUTE_DRFP + '/contract/<contract_addr>')
def get_contract(contract_addr):
	DRFPContract(contract_addr)

def compile_drfp_sol():
	CONTRACT_NAME = 'drfp'
	FILE_NAME = CONTRACT_NAME + '.sol'
	PATH = '/truffle/contracts/' + FILE_NAME

	printd('compiling %s...' % (FILE_NAME))
	COMPILED = compile_files([FILE_NAME])
	RFP = COMPILED[FILE_NAME + ':' + CONTRACT_NAME]
	global DRFPContract
	DRFPContract = web3.eth.contract(
        abi = RFP['abi'],
        bytecode = RFP['bin'],
        bytecode_runtime = RFP['bin-runtime']
    )

'''
	Construct the args from the given params for the contract.

	- params: the drfp params (see get_params)

	- returns the args as a [String]
'''
def get_args(params):
	# get ipfs hash for spec and template
	file_hash = upload(params[DRFP_FILE])

	# construct args
	args = []
	args.append(params[DRFP_OWNER])
	args.append(params[DRFP_NAME])
	args.append(file_hash)
	args.append(params[DRFP_ADVERTISING])
	args.append(params[DRFP_BIDDING])
	args.append(params[DRFP_REVEAL])
	args.append(params[DRFP_AWARD])

	return args

'''
	Get the IPFS hash from the given file.

	- file: The file to be added to IPFS

	- returns the IPFS hash
'''
def get_ipfs_hash(file):
	return upload()['hash']

'''
	Debug print.

	- msg: The message to print
'''
def printd(msg):
	if DEBUG == False:
		return
	print '##########   %s   ##########' % (msg)

# compile the smart contract
# compile_drfp_sol()
