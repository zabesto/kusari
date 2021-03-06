import base64
import ipfsapi                                             # Peer to Peer distributed storage
import json
import os
import time

from Crypto.Cipher import PKCS1_OAEP					   # Encryption
from Crypto.PublicKey import RSA                           # Python key pair generator
from flask import Flask, jsonify, request, make_response   # Python microframework
from io import FileIO                                      # Create temp file to upload to IPFS
from rfpglobals import *
from solc import compile_files                             # Python wrapper for the Solidity compiler
from web3 import Web3, HTTPProvider                        # Python implementation of Web3 to interact with the blockchain

# flask server
app = Flask(__name__)

# testrpc
testrpc = Web3(HTTPProvider('http://localhost:8545'))

''' IPFS '''

HOST_IPFS = '127.0.0.1'
PORT_IPFS = 5001

ipfs = ipfsapi.connect(HOST_IPFS, PORT_IPFS)

def upload(file):
	FILE_NAME = 'temp_file.txt'

	# write to temp file
	printd('creating temp file...')
	with FileIO(FILE_NAME, 'w') as temp_file:
		temp_file.write(file)

	# upload to ipfs
	printd('uploading file...')
	result = ipfs.add(FILE_NAME)

	printd(result['Hash'])

	# TODO: delete file
	os.remove(FILE_NAME)

	return result

def decode(file):
	printd('decoding file...')
	BASE64_PREFIX = 'data:text/markdown;base64,'   # TODO update to use regex
	base64_file = file.replace(BASE64_PREFIX, '')
	decoded_file = base64.b64decode(base64_file)

	return decoded_file

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
	rfc_instance = DRFPContract(contract_addr)
	# generate whitelist


	for addr in request_body[DRFP_WHITELIST]:
		rfc_instance.transact({'from': owner_addr, 'gas':1000000}).addBidder(addr)

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
	response[SC_WHITELIST] = instance.call({'from': owner_addr}).getWhitelist()

	response[SC_BIDDERS] = []
	for addr in response[SC_WHITELIST]:
		bidder = instance.call({'from': owner_addr}).bidders(addr)
		response[SC_BIDDERS].append(bidder)

	return jsonify(response)

'''
	Upload the bidder proposal.
'''
@app.route(ROUTE_DRFP + '/proposal', methods=['POST'])
def bid_proposal():
	request_body = request.get_json()
	bidder_addr = request_body[SC_BIDDER_ADDR]
	contract_addr = request_body[SC_CONTRACT_ADDR]
	file = request_body[SC_FILE]
	
	decoded_file = decode(file)

	keys = generate_keypair()
	public_key = keys[0]

	rfc_instance = DRFPContract(contract_addr)
	rfc_instance.transact({'from': bidder_addr, 'gas':1000000}).addPublicKey(public_key)

	# encrypt file
	printd('encrypting file...')
	rsa_key = RSA.importKey(public_key)
	cipher = PKCS1_OAEP.new(rsa_key)
	encrypted_file = cipher.encrypt(decoded_file)
	printd(encrypted_file)

	# get hash of ipfs file
	upload_results = upload(encrypted_file)
	file_hash = upload_results['Hash']
	rfc_instance.transact({'from': bidder_addr, 'gas':1000000}).addBidLocation(file_hash)

	return jsonify(keys)

@app.route(ROUTE_DRFP + '/decrypt', methods=['POST'])
def decrypt():
	request_body = request.get_json()
	private_key = request_body[SC_PRIVATE_KEY]
	encrypted_file = request_body[SC_FILE]
	decoded_file = base64.b64decode(encrypted_file)

	rsa_key = RSA.importKey(private_key)
	cipher = PKCS1_OAEP.new(rsa_key)
	decrypted_file = cipher.decrypt(decoded_file)

	print jsonif(decrypted_file)

'''
	Reveal the private key for the IPFS file that was submitted by the bidder.

	- returns the private key for the IPFS file
'''
@app.route(ROUTE_DRFP + '/reveal', methods=['POST'])
def reveal_ipfs_key():
	request_body = request.get_json()
	bidder_addr = request_body[SC_BIDDER_ADDR]
	contract_addr = request_body[SC_CONTRACT_ADDR]
	private_key = request_body[SC_PRIVATE_KEY]

	rfc_instance = DRFPContract(contract_addr)
	rfc_instance.transact({'from': bidder_addr, 'gas':1000000}).addPrivateKey(private_key)

	return 'success'

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
	file = params[DRFP_FILE]
	decoded_file = decode(file)

	# get ipfs hash for spec and template
	upload_results = upload(decoded_file)
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
	Generate keypair.

	- returns an array containing a public and private key
'''
def generate_keypair():
	key = RSA.generate(RSA_BITS)
	private_key = key.exportKey(RSA_FORMAT)
	public_key = key.publickey().exportKey(RSA_FORMAT)

	printd('public_key: %s' % (public_key))
	printd('private_key: %s' % (private_key))

	return [public_key, private_key]

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
