import json

from flask import Flask, jsonify
from solc import compile_files
from web3 import Web3, TestRPCProvider
import ipfsapi

app = Flask(__name__)

''' IPFS '''

@app.route('/ipfs/upload')
def upload():
    FILE_NAME = ''

    api = ipfsapi.connect('127.0.0.1', 5001)
    result = api.add(FILE_NAME)

    return jsonify(result)

''' Web3 '''

# @app.route("/drfp/create", method=['POST'])
# def create_drfp():

#     # the smart contract
#     CONTRACT_NAME = 'drfp'
#     FILE_NAME = CONTRACT_NAME + '.sol'

#     DEPLOY_COST = 4000000

#     # compile the sol file
#     COMPILED = compile_files([FILE_NAME])
#     RFP = COMPILED[FILE_NAME + ':' + CONTRACT_NAME]
#     RFPContract = web3.eth.contract(
#         abi = RFP['abi'],
#         bytecode = RFP['bin'],
#         bytecode_runtime = RFP['bin-runtime']
#     )

#     # extract args from request
#     # get address
#     owner_addr = web3.eth.accounts[0]
#     # int(request.form[''])

#     # deploy the contract to the blockchain
#     trans_hash = CONTRACT.deploy(
#         args=['hello bobby boy'],
#         transaction={'from':owner_addr, 'gas':DEPLOY_COST}
#     )

#     # fetch the instance of the contract
#     trans_receipt = web3.eth.getTransactionReceipt(trans_hash)
#     contract_addr = trans_receipt['contractAddress']
#     rfc_contract = RFPContract(contract_addr)

#     RESULT = rfc_contract.call(
#         {'from': web3.eth.coinbase}
#     )

#     return jsonify(RESULT)
