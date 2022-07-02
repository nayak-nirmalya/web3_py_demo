from solcx import compile_standard, install_solc
import json

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Install Solidity Compiler (Only Run for the First Time)
# install_solc("0.6.0")

# Compile Our Solidity File
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)
