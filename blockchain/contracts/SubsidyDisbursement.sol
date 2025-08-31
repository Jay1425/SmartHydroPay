// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SubsidyDisbursement {
    address public government;
    
    struct Producer {
        bool isRegistered;
        uint256 milestone; // e.g., target volume of hydrogen
        uint256 subsidyAmount;
        bool milestoneMet;
    }
    
    mapping(address => Producer) public producers;
    
    event ProducerRegistered(address indexed producerAddress);
    event MilestoneSet(address indexed producerAddress, uint256 milestone, uint256 subsidyAmount);
    event SubsidyReleased(address indexed producerAddress, uint256 amount);
    
    modifier onlyGovernment() {
        require(msg.sender == government, "Only government can call this function");
        _;
    }
    
    constructor() {
        government = msg.sender;
    }
    
    function registerProducer(address producerAddress) public onlyGovernment {
        require(!producers[producerAddress].isRegistered, "Producer already registered");
        producers[producerAddress].isRegistered = true;
        emit ProducerRegistered(producerAddress);
    }
    
    function setMilestone(address producerAddress, uint256 milestone, uint256 subsidyAmount) public onlyGovernment {
        require(producers[producerAddress].isRegistered, "Producer not registered");
        producers[producerAddress].milestone = milestone;
        producers[producerAddress].subsidyAmount = subsidyAmount;
        emit MilestoneSet(producerAddress, milestone, subsidyAmount);
    }
    
    function verifyAndRelease(address producerAddress, uint256 actualVolume) public onlyGovernment {
        Producer storage producer = producers[producerAddress];
        require(producer.isRegistered, "Producer not registered");
        require(!producer.milestoneMet, "Milestone already met");
        
        if (actualVolume >= producer.milestone) {
            producer.milestoneMet = true;
            payable(producerAddress).transfer(producer.subsidyAmount);
            emit SubsidyReleased(producerAddress, producer.subsidyAmount);
        }
    }

    // Function to receive Ether
    receive() external payable {}

    // Function to withdraw contract balance (only for government)
    function withdraw() public onlyGovernment {
        payable(government).transfer(address(this).balance);
    }
}
