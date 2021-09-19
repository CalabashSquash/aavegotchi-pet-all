#!/bin/python3
import sys
import time
import os
from web3 import Web3
from web3.auto import w3
from eth_account import Account
from decouple import config


# get environment variables
private_key = config('PRIVATE_KEY')
rpc = config('MATIC_RPC')

twelve_hours = 12 * 60 * 60
aavegotchi_abi = ""
aavegotchi_diamond = ""

with open("abi.json", "r") as reader:
    aavegotchi_abi = reader.read().strip()

with open("aavegotchiDiamond.txt", "r") as reader:
    aavegotchi_diamond = reader.read().strip()

web3 = Web3(Web3.HTTPProvider(rpc))
from web3.middleware import geth_poa_middleware
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

aavegotchi_diamond = web3.toChecksumAddress(aavegotchi_diamond)

acct = Account.privateKeyToAccount(private_key)
ether_address = acct.address

contract = web3.eth.contract(address=aavegotchi_diamond, abi=aavegotchi_abi)
gotchis = contract.functions.tokenIdsOfOwner(ether_address).call()

# These are the numeric traits of a portal
portal_numeric_traits = [0, 0, 0, 0, 0, 0]
# We want to delete any portals from the list because the transaction will
# revert when trying to interact with them
def filterPortals(gotchi): 
    numeric_traits = contract.functions.getNumericTraits(gotchi).call()
    return not len(set(numeric_traits).intersection(portal_numeric_traits)) != 0

summoned_gotchis = list(filter(filterPortals, gotchis))

print("Attempting to pet gotchis with the following IDs:")
print(f"{summoned_gotchis}")

def pet():
    nonce = web3.eth.get_transaction_count(ether_address)
    pet_tx = contract.functions.interact(summoned_gotchis).buildTransaction({
        "chainId":137,
        "gasPrice": w3.toWei("1", "gwei"),
        "nonce": nonce
    })

    signed_txn = web3.eth.account.sign_transaction(pet_tx, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()

    print("interact() called. Transaction ID:")
    print(f"https://polygonscan.com/tx/{tx_hash}")

def next_interact_time(contract):
    aavegotchi_details = contract.functions.getAavegotchi(summoned_gotchis[0]).call()
    next_interact_time = aavegotchi_details[13] + twelve_hours
    print(f"Next interaction time: {next_interact_time}")
    print(f"Current time: {time.time()}")
    time_till = (next_interact_time - time.time())
    print(f"Time till next interaction: {time_till / (60*60)} hours.")
    return time_till

if summoned_gotchis:
    while True:
        time_till = next_interact_time(contract)
        if time_till > 0:
            print(f"Sleeping for {time_till} seconds")
            time.sleep(time_till + 30)
        pet()
        time.sleep(120)
        if next_interact_time(contract) > 11*60*60:
            break

class AavegotchiCareTaker:
    def __init__(self, private_key_filename:str, matic_rpc_filename:str, \
                 gotchi_diamond_address:str, gotchi_abi:str):
        self.rpc = ""
        self.private_key = ""
        self.aavegotchi_abi = ""
        self.aavegotchi_diamond = ""
        with open(matic_rpc_filename, "r") as rpc_reader, \
             open(gotchi_abi, "r") as abi_reader, \
             open(gotchi_diamond_address, "r") as diamond_addr_reader, \
             open(private_key_filename, "r") as private_key_reader:
            self.rpc = rpc_reader.read()
            self.aavegotchi_abi = abi_reader.read()
            self.aavegotchi_diamond = diamond_addr_reader.read()
            self.private_key = private_key_reader.read()
            self.acct = Account.privateKeyToAccount(private_key)
            self.aavegotchi_diamond = web3.toChecksumAddress(this.aavegotchi_diamond)

        self.web3 = Web3(Web3.HTTPProvider(self.rpc))
        from web3.middleware import geth_poa_middleware
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.ether_address = acct.address

        self.contract = web3.eth.contract(address=aavegotchi_diamond, abi=aavegotchi_abi)

    def fetch_gotchis(self):
        return self.contract.functions.tokenIdsOfOwner(self.ether_address).call()

    def set_gotchis(self, gotchiIds:[int]):
        self.gotchis = gotchiIds

    def fetch_all_gotchi_details(self):
        details = []
        for i in range(0, len(gotchis)):
            details.append(self.contract.functions.getAavegotchi(gotchis[i]).call())

        
