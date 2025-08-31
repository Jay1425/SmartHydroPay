require("@nomicfoundation/hardhat-ethers");

module.exports = {
  solidity: "0.8.0",
  networks: {
    ganache: {
      url: "http://127.0.0.1:8545", // Default Ganache URL
    },
    localhost: {
      url: "http://127.0.0.1:8546", // Local Hardhat node
    },
  },
};
