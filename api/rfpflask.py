import base64
import ipfsapi                              # Peer to Peer distributed storage
import json
import time

from flask import Flask, jsonify, request   # Python microframework
from solc import compile_files              # Python wrapper for the Solidity compiler
from io import FileIO
from web3 import Web3, TestRPCProvider      # Python implementation of Web3 to interact with the blockchain

DEBUG = True

# flask server
app = Flask(__name__)

# testrpc
web3 = Web3(TestRPCProvider())

''' IPFS '''

HOST_IPFS = '127.0.0.1'
PORT_IPFS = 5001

ROUTE_IPFS='/ipfs'

ipfs = ipfsapi.connect(HOST_IPFS, PORT_IPFS)

def upload(file):
	# decode file
	printd('decoding file...')
	BASE64_PREFIX = 'data:text/markdown;base64,'   # TODO update to use regex
	base64_file = file.replace(BASE64_PREFIX, '')
	decoded_file = base64.b64decode(base64_file)

	# write to temp file
	printd('creating temp file...')
	with FileIO('temp_file', 'w') as temp_file:
		temp_file.write(decoded_file)

	# upload to ipfs
	printd('uploading file...')
	# result = ipfs.add('README.md')
	result = ipfs.add('temp_file')

	return result

''' Web3 '''

ROUTE_DRFP='/drfp'

# DRFP params
DRFP_ACCOUNT = 'account'
DRFP_OWNER = 'manager'
DRFP_NAME = 'name'
DRFP_WHITELIST = 'whitelist'
DRFP_PERIODS = 'periods'
DRFP_ADVERTISING = 'advertising'
DRFP_BIDDING = 'bidding'
DRFP_REVEAL = 'reveal'
DRFP_AWARD = 'award'
DRFP_FILE = 'file'

'''
	Return the DRFP parameters.

	- returns the DRFP parameters as a json string
'''
@app.route(ROUTE_DRFP + '/params')
def get_params():
	periods = {}
	periods[DRFP_BIDDING] = 'uint'
	periods[DRFP_REVEAL] = 'uint'
	periods[DRFP_AWARD] = 'uint'

	params = {}
	params[DRFP_ACCOUNT] = 'String'
	params[DRFP_OWNER] = 'String'
	params[DRFP_NAME] = 'String'
	params[DRFP_WHITELIST] = '[String]'
	params[DRFP_PERIODS] = periods
	params[DRFP_FILE] = 'file'

	return jsonify(params)

'''
	Fetch the existing owner.

	- returns an address to the owner
'''
@app.route(ROUTE_DRFP + '/account/owner')
def create_owner():
	return jsonify(web3.eth.accounts[0])

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

	return jsonify(web3.eth.accounts[id])

'''
	Returns the request data.

	- returns the request data
'''
@app.route(ROUTE_DRFP + '/create/dummy', methods=['POST'])
def create_drfp_dummy():
	return jsonify(request.data)

'''
	Create a new DRFP.


	- returns the results

'''
@app.route(ROUTE_DRFP + '/create', methods=['POST'])
def create_drfp():
	DEPLOY_COST = 4000000

	request_body = request.get_json()
	owner_addr = request_body[DRFP_ACCOUNT]
	printd(owner_addr)

    # extract args from request
	printd('convert to json...')
	printd(jsonify(request_body))
	args = get_args(request_body)

    # deploy the contract to the blockchain
	printd('deploying...')
	trans_hash = DRFPContract.deploy(
        args=args,
        transaction={'from':owner_addr, 'gas':DEPLOY_COST}
    )

    # fetch the instance of the contract
	printd('fetching transaction for smart contract instance...')
	trans_receipt = web3.eth.getTransactionReceipt(trans_hash)
	contract_addr = trans_receipt['contractAddress']
	global rfc_instance
	rfc_instance = DRFPContract(contract_addr)

	return jsonify(contract_addr)

# smart contract params
SC_NAME = DRFP_NAME
SC_OWNER = DRFP_OWNER
SC_ADDR = 'managerAddress'
SC_LINK = 'specLink'
SC_PERIODS = DRFP_PERIODS
SC_BIDDING = DRFP_BIDDING
SC_REVEAL = DRFP_REVEAL
SC_AWARD = DRFP_AWARD
SC_WHITELIST = DRFP_WHITELIST

@app.route(ROUTE_DRFP + '/contract/dummy')
def get_contract_dummy():
	data = {}
	data[SC_NAME] = 'Contruct12'
	data[SC_OWNER] = 'rishabh'
	data[SC_ADDR] = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNA3DQEBAQUAA4GNqGKukO1De7zhZj6+H0q'
	data[SC_LINK] = 'https://www.google.com/'

	periods = {}
	periods[SC_BIDDING] = int(round(time.time() * 1000))
	periods[SC_REVEAL] = int(round(time.time() * 1000))
	periods[SC_AWARD] = int(round(time.time() * 1000))
	data[SC_PERIODS] = periods

	whitelist = []
	whitelist.append("MIGfMA0GCSqGSIb")
	whitelist.append("3DQEBAQUAA4GN")
	whitelist.append("3DQEBAQUAA4GN")
	whitelist.append("ukO1De7zhZj6+")

	data[SC_WHITELIST] = whitelist

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

	printd(DRFPContract)

'''
	Construct the args from the given params for the contract.

	- params: the drfp params (see get_params)

	- returns the args as a [String]
'''
def get_args(params):
	printd('extracting args...')

	# get ipfs hash for spec and template
	upload_results = upload(params[DRFP_FILE])
	file_hash = upload_results['Hash']

	# get nested periods
	periods = params[DRFP_PERIODS]

	# construct args
	args = []
	args.append(params[DRFP_OWNER])
	args.append(params[DRFP_NAME])
	args.append(file_hash)
	args.append(int(periods[DRFP_ADVERTISING]))
	args.append(int(periods[DRFP_BIDDING]))
	args.append(int(periods[DRFP_REVEAL]))
	args.append(int(periods[DRFP_AWARD]))

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
compile_drfp_sol()
