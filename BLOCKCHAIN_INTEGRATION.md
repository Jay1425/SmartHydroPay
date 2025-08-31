# Blockchain Integration for Green Hydrogen Subsidy Disbursement

This document provides a step-by-step guide to integrate and run the blockchain functionality with your Flask application.

## 1. Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js and npm**: Required for Hardhat.
- **Ganache**: A personal blockchain for Ethereum development. Download it from [here](https://www.trufflesuite.com/ganache).
- **Python and pip**: You should already have this for your Flask application.

## 2. Setup Hardhat and Compile the Smart Contract

1.  **Install Hardhat and dependencies:**
    Open a terminal in the `blockchain` directory and run:
    ```bash
    cd blockchain
    npm cache clean --force
    npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox --legacy-peer-deps
    ```
    
    **Note:** If you encounter dependency conflicts, the `--legacy-peer-deps` flag resolves them by using npm's legacy dependency resolution algorithm.

2.  **Start Ganache:**
    Launch your Ganache application. It will start a local Ethereum network, typically at `http://127.0.0.1:8545`.

3.  **Compile the Smart Contract:**
    In the `blockchain` directory, run the Hardhat compile task:
    ```bash
    npx hardhat compile
    ```
    This will create an `artifacts` directory containing the compiled contract ABI. I will create a copy of the ABI in `blockchain/contracts/SubsidyDisbursement.json` for the Flask app to use.

## 3. Deploy the Smart Contract

1.  **Run the deployment script:**
    Use the Hardhat script to deploy your contract to the default network.
    ```bash
    npx hardhat run scripts/deploy.js
    ```
    **Your contract has been deployed to: `0x5FbDB2315678afecb367f032d93F642f64180aa3`**

2.  **Contract Address:**
    The deployment script outputs the address of the deployed `SubsidyDisbursement` contract:
    ```
    Deploying contracts with the account: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
    SubsidyDisbursement contract deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3
    ```
    **This address has already been configured in your Flask app.**

## 4. Configure the Flask Application

1.  **The Flask app is already configured:**
    The `blockchain/web3_utils.py` file has been updated with the deployed contract address: `0x5FbDB2315678afecb367f032d93F642f64180aa3`

2.  **Install Python dependencies:**
    Make sure you have `web3.py` installed:
    ```bash
    pip install web3
    ```
    **This has already been installed.**

## 5. Run the Example Flow

Your Flask application now has three new API endpoints to interact with the smart contract.

1.  **Start your Flask server:**
    ```bash
    python run.py
    ```

2.  **Interact with the API endpoints:**
    You can use a tool like `curl` or Postman to make requests.

    **a. Register a Producer:**
    Get a producer's Ethereum address from Ganache.
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"producer_address": "PRODUCER_ETHEREUM_ADDRESS"}' http://127.0.0.1:5000/blockchain/register_producer
    ```

    **b. Set a Milestone:**
    Set a production milestone for the registered producer.
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"producer_address": "PRODUCER_ETHEREUM_ADDRESS", "target_volume": 1000, "subsidy_amount": 10}' http://127.0.0.1:5000/blockchain/set_milestone
    ```
    *Note: The `subsidy_amount` is in Ether.*

    **c. Verify Milestone and Release Subsidy:**
    Once the producer meets the milestone, your backend can verify this and trigger the subsidy release.
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"producer_address": "PRODUCER_ETHEREUM_ADDRESS", "actual_volume": 1050}' http://127.0.0.1:5000/blockchain/verify_and_release
    ```
    If `actual_volume` is greater than or equal to `target_volume`, the smart contract will automatically transfer the subsidy to the producer's address.

## 6. Audit Trail

I have added a `SubsidyLog` model to your database. The blockchain interaction routes will now log every disbursement action, creating an audit trail within your Flask application's database.

## 7. Package.json Update

Ensure your `package.json` in the `blockchain` directory has the correct Hardhat version:
```json
"devDependencies": {
  "hardhat": "^3.0.3",
  "@nomicfoundation/hardhat-toolbox": "^3.0.0"
}
```
