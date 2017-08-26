pragma solidity ^0.4.8;

// Decentralized RFP Process
contract drfp {

    struct Bidder {
        bool isValid;
        string name;
        string publicKey;
        string privateKey;
        string bidLocation;
    }

    struct BidManager {
        string name;
    }

    struct BidPackage {
        string specLocation;
        string templateLocation;
    }

    struct PeriodStarts {
        uint advertisingStart;
        uint biddingStart;
        uint revealStart;
        uint awardDate;
    }

    mapping (address => Bidder) bidders;

    enum RFPPeriods { Advertising, Bidding, Reveal, Award }
    RFPPeriods currentPeriod;
    RFPPeriods constant defaultChoice = RFPPeriods.Advertising;
    BidManager bidManager;
    BidPackage bidPackage;
    PeriodStarts periodStarts;

    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    modifier onlyBidders() {
        require(!bidders[msg.sender].isValid);
        _;
    }

    modifier onlyAfter(uint _time) {
        require(now > _time);
        _;
    }

    // HACK FOR NOW
    function drfp(string bidManagerName, string specLocation, string templateLocation,
                    uint advertisingStart, uint biddingStart, uint revealStart, uint awardDate)
    {
        currentPeriod = RFPPeriods.Advertising;
        bidManager.name = bidManagerName;
        bidPackage.specLocation = specLocation;
        bidPackage.templateLocation = templateLocation;
        periodStarts.advertisingStart = advertisingStart;
        periodStarts.biddingStart = biddingStart;
        periodStarts.revealStart = revealStart;
        periodStarts.awardDate = awardDate;
    }

    function getCurrentPeriod() returns (RFPPeriods) {
        return currentPeriod;
    }

    function reveal() onlyOwner {
        //if (block.timestamp < deadline) throw;      // TODO investigate block.timestamp

        // do stuff
    }

    // dtor
    function destroy() {
        if (msg.sender == owner) {
            suicide(owner);
        }
    }

    // ignore transactions with invalid data
    function () {
        assert(false);
    }
}
