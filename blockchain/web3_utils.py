from web3 import Web3
import json
import os

class Web3Utils:
    def __init__(self, provider_url, contract_address, contract_abi, government_private_key):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
        
        # Create government account from private key
        self.government_account = self.web3.eth.account.from_key(government_private_key)
        self.web3.eth.default_account = self.government_account.address

    def register_producer(self, producer_address):
        # Build transaction
        transaction = self.contract.functions.registerProducer(producer_address).build_transaction({
            'from': self.government_account.address,
            'nonce': self.web3.eth.get_transaction_count(self.government_account.address),
            'gas': 200000,
            'gasPrice': self.web3.to_wei('20', 'gwei')
        })
        
        # Sign and send transaction
        signed_txn = self.web3.eth.account.sign_transaction(transaction, self.government_account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return self.web3.eth.wait_for_transaction_receipt(tx_hash)

    def set_milestone(self, producer_address, target_volume, subsidy_amount):
        subsidy_amount_wei = self.web3.to_wei(subsidy_amount, 'ether')
        
        transaction = self.contract.functions.setMilestone(producer_address, target_volume, subsidy_amount_wei).build_transaction({
            'from': self.government_account.address,
            'nonce': self.web3.eth.get_transaction_count(self.government_account.address),
            'gas': 200000,
            'gasPrice': self.web3.to_wei('20', 'gwei')
        })
        
        signed_txn = self.web3.eth.account.sign_transaction(transaction, self.government_account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return self.web3.eth.wait_for_transaction_receipt(tx_hash)

    def verify_and_release(self, producer_address, actual_volume):
        transaction = self.contract.functions.verifyAndRelease(producer_address, actual_volume).build_transaction({
            'from': self.government_account.address,
            'nonce': self.web3.eth.get_transaction_count(self.government_account.address),
            'gas': 200000,
            'gasPrice': self.web3.to_wei('20', 'gwei')
        })
        
        signed_txn = self.web3.eth.account.sign_transaction(transaction, self.government_account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return self.web3.eth.wait_for_transaction_receipt(tx_hash)

def get_web3_utils():
    # Configuration for local Hardhat network
    provider_url = 'http://127.0.0.1:8545'  # Default Hardhat network
    
    # Load contract ABI
    abi_path = os.path.join(os.path.dirname(__file__), 'contracts', 'SubsidyDisbursement.json')
    with open(abi_path, 'r') as f:
        contract_interface = json.load(f)
    
    contract_abi = contract_interface['abi']
    
    # Deployed contract address (update this after deployment)
    contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
    
    # Government private key (first account from Hardhat's default accounts)
    government_private_key = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'

    return Web3Utils(provider_url, contract_address, contract_abi, government_private_key)

