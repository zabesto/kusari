import base64
import ipfsapi                              # Peer to Peer distributed storage
import json
import time

from flask import Flask, jsonify, request   # Python microframework
from io import FileIO
from rfpglobals import *
from solc import compile_files              # Python wrapper for the Solidity compiler
from web3 import Web3, HTTPProvider         # Python implementation of Web3 to interact with the blockchain

DEBUG = True

# flask server
app = Flask(__name__)

# testrpc
testrpc = Web3(HTTPProvider('http://localhost:8545'))

''' Storage '''

rfp_store = {}

''' IPFS '''

HOST_IPFS = '127.0.0.1'
PORT_IPFS = 5001

ipfs = ipfsapi.connect(HOST_IPFS, PORT_IPFS)

def upload(file):
	# decode file
	printd('decoding file...')
	BASE64_PREFIX = 'data:text/markdown;base64,'   # TODO update to use regex
	base64_file = file.replace(BASE64_PREFIX, '')
	decoded_file = base64.b64decode(base64_file)

	FILE_NAME = 'temp_file.txt'

	# write to temp file
	printd('creating temp file...')
	with FileIO(FILE_NAME, 'w') as temp_file:
		temp_file.write(decoded_file)

	# upload to ipfs
	printd('uploading file...')
	result = ipfs.add(FILE_NAME)

	printd(result['Hash'])

	return result

''' Web3 '''

'''
	Fetch the existing owner.

	- returns an address to the owner
'''
@app.route(ROUTE_DRFP + '/account/owner')
def create_owner():
	for account in testrpc.eth.accounts:
		printd(account)

	return jsonify(testrpc.eth.accounts[0])

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
		return testrpc.eth.accounts[MIN_ID]

	if id > MAX_ID:
		print('WARNING: %s is GREATER THAN the max: %s' % (id, MAX_ID))
		return testrpc.eth.accounts[MAX_ID]

	return jsonify(testrpc.eth.accounts[id])

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
	trans_receipt = testrpc.eth.getTransactionReceipt(trans_hash)
	contract_addr = trans_receipt['contractAddress']
	global rfc_instance
	rfc_instance = DRFPContract(contract_addr)

	# generate whitelist
	for addr in request_body[DRFP_WHITELIST]:
		rfc_instance.call({'from': owner_addr, 'gas':100000}).addBidder(addr)

	return jsonify(contract_addr)

'''
	Fetch the contract.

	- returns the contract
'''
@app.route(ROUTE_DRFP + '/search', methods=['POST'])
def find_contract():
	request_body = request.get_json()
	owner_addr = request_body[SC_OWNER_ADDR]
	contract_addr = request_body[SC_CONTRACT_ADDR]

	instance = DRFPContract(contract_addr)

	response = {}
	response[SC_NAME] = instance.call({'from': owner_addr}).bidPackage()[0]
	response[SC_OWNER] = instance.call({'from': owner_addr}).bidManager()
	response[SC_OWNER_ADDR] = owner_addr
	response[SC_LINK] = instance.call({'from': owner_addr}).bidPackage()[1]
	response[SC_AWARD] = instance.call({'from': owner_addr}).periodStarts()[3]
	response[SC_REVEAL] = instance.call({'from': owner_addr}).periodStarts()[2]
	response[SC_BIDDING] = instance.call({'from': owner_addr}).periodStarts()[1]

	#bidders = instance.call({'from': owner_addr}).bidders()
	#response['bidders'] = bidders
	whitelist = []
	response[SC_WHITELIST] = whitelist

	return jsonify(response)

'''
	Upload the bidder proposal.
'''
@app.route(ROUTE_DRFP + '/proposal', methods=['POST'])
def bid_proposal():
	request_body = request.get_json()
	bidder_addr = request_body[SC_BIDDER_ADDR]
	contract_addr = request_body[SC_CONTRACT_ADDR]
	
	# get hash of ipfs file
	upload_results = upload(request_body[SC_FILE])
	file_hash = upload_results['Hash']

	# store the hash
	return add_to_rfp_store(contract_addr, bidder_addr, file_hash)

'''
	Reveal the private key for the IPFS file that was submitted by the bidder.

	- returns the private key for the IPFS file
'''
@app.route(ROUTE_DRFP + '/reveal', methods=['POST'])
def reveal_ipfs_key():
	request_body = request.get_json()
	bidder_addr = request_body[SC_BIDDER_ADDR]
	contract_addr = request_body[SC_CONTRACT_ADDR]

	return get_from_rfp_store(contract_addr, bidder_addr)

def add_to_rfp_store(contract_addr, bidder_addr, file_hash):
	bid_dict = {}
	bid_dict[bidder_addr] = file_hash
	rfp_store[contract_addr] = bid_dict

	return 'ok'

def get_from_rfp_store(contract_addr, bidder_addr):
	bid_dict = rfp_store[contract_addr]

	return jsonify(bid_dict[bidder_addr])

def compile_drfp_sol():
	CONTRACT_NAME = 'drfp'
	FILE_NAME = CONTRACT_NAME + '.sol'
	PATH = '/truffle/contracts/' + FILE_NAME

	printd('compiling %s...' % (FILE_NAME))
	COMPILED = compile_files([FILE_NAME])
	RFP = COMPILED[FILE_NAME + ':' + CONTRACT_NAME]
	global DRFPContract
	DRFPContract = testrpc.eth.contract(
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
