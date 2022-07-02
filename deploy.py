import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("compiled_code.json", "r") as file:
    compiled_sol = json.load(file)

# Getting the ByteCode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Getting ABI
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# For Connecting to Ganache
w3 = Web3(Web3.HTTPProvider(os.getenv("URL")))
chain_id = os.getenv("CHAIN_ID")
address = os.getenv("ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Create the Contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the Latest Transaction Number
nonce = w3.eth.getTransactionCount(address)

# 1. Build Transaction
trasaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": address, "nonce": nonce, "gasPrice": w3.eth.gas_price}
)

# 2. Sign Transaction
signed_transaction = w3.eth.account.signTransaction(trasaction, private_key)

# 3. Send Transaction
tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
# print(abi)

# Working with Contract
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Reading & Writing Contract
print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(25).buildTransaction(
    {
        "chainId": chain_id,
        "from": address,
        "nonce": nonce + 1,
        "gasPrice": w3.eth.gas_price,
    }
)
signed_store_transaction = w3.eth.account.signTransaction(
    store_transaction, private_key
)
transaction_hash = w3.eth.sendRawTransaction(signed_store_transaction.rawTransaction)
transaction_receipt = w3.eth.waitForTransactionReceipt(transaction_hash)

print(simple_storage.functions.retrieve().call())
