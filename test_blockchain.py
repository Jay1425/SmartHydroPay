"""
Test script for blockchain integration.
This script demonstrates the complete workflow:
1. Register a producer
2. Set milestone
3. Verify and release subsidy
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_blockchain_integration():
    print("🚀 Testing Blockchain Integration for Green Hydrogen Subsidy Disbursement\n")
    
    # Test producer address (from Hardhat's default accounts)
    producer_address = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
    
    print(f"👨‍🏭 Producer Address: {producer_address}")
    print(f"🏛️  Government Address: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")
    print(f"📄 Contract Address: 0x5FbDB2315678afecb367f032d93F642f64180aa3\n")
    
    # Step 1: Register Producer
    print("📝 Step 1: Registering producer...")
    register_data = {"producer_address": producer_address}
    
    try:
        response = requests.post(f"{BASE_URL}/blockchain/register_producer", 
                               json=register_data, 
                               headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Producer registered successfully!")
            print(f"   Transaction Hash: {result.get('tx_hash')}")
        else:
            print(f"❌ Failed to register producer: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error registering producer: {e}")
        return
    
    print()
    
    # Step 2: Set Milestone
    print("🎯 Step 2: Setting milestone...")
    milestone_data = {
        "producer_address": producer_address,
        "target_volume": 1000,  # 1000 units of hydrogen
        "subsidy_amount": 5     # 5 ETH subsidy
    }
    
    try:
        response = requests.post(f"{BASE_URL}/blockchain/set_milestone", 
                               json=milestone_data, 
                               headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Milestone set successfully!")
            print(f"   Target Volume: {milestone_data['target_volume']} units")
            print(f"   Subsidy Amount: {milestone_data['subsidy_amount']} ETH")
            print(f"   Transaction Hash: {result.get('tx_hash')}")
        else:
            print(f"❌ Failed to set milestone: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error setting milestone: {e}")
        return
    
    print()
    
    # Step 3: Verify and Release Subsidy
    print("💰 Step 3: Verifying milestone and releasing subsidy...")
    verify_data = {
        "producer_address": producer_address,
        "actual_volume": 1200  # Producer achieved 1200 units (more than target)
    }
    
    try:
        response = requests.post(f"{BASE_URL}/blockchain/verify_and_release", 
                               json=verify_data, 
                               headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Milestone verified and subsidy released!")
            print(f"   Actual Volume: {verify_data['actual_volume']} units")
            print(f"   Transaction Hash: {result.get('tx_hash')}")
            print(f"🎉 Subsidy of 5 ETH has been automatically transferred to the producer!")
        else:
            print(f"❌ Failed to verify and release: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error verifying and releasing: {e}")
        return
    
    print("\n🏁 Blockchain integration test completed successfully!")
    print("📊 Check your Flask app's database for audit trail logs.")

if __name__ == "__main__":
    test_blockchain_integration()
