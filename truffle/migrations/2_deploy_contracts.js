var Drfp = artifacts.require("./drfp.sol");

module.exports = function(deployer) {
    bidManager = "DJ Carter";
    rfpName = "Bids for Pandas carrying kusari-gundo"
    specLocation = "0x0923409823049AFAF234";
    advertisingStart = 1503773778;
    biddingStart = 1503860178;
    revealStart = 1503946578;
    awardDate = 1503773778;
    deployer.deploy(Drfp, bidManager, rfpName, specLocation, advertisingStart, biddingStart, revealStart, awardDate );
};
