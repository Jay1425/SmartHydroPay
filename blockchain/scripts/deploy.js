async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);

  const SubsidyDisbursement = await ethers.getContractFactory("SubsidyDisbursement");
  const subsidyDisbursement = await SubsidyDisbursement.deploy();

  await subsidyDisbursement.waitForDeployment();

  console.log("SubsidyDisbursement contract deployed to:", await subsidyDisbursement.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
