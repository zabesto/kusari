pragma solidity ^0.4.8;

// Decentralized RFP Process
contract drfp {

    struct Bidder {
        bool isValid;
        string name;
        string publicKey;
        string bidLocation;
        string privateKey;
    }

    struct BidManager {
        string name;
    }

    struct BidPackage {
        string name;
        string specLocation;
    }

    struct PeriodStarts {
        uint advertisingStart;
        uint biddingStart;
        uint revealStart;
        uint awardDate;
    }

    mapping (address => Bidder) bidders;

    enum RFPPeriods { Advertising, Bidding, Reveal, Award }
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
        require(bidders[msg.sender].isValid);
        _;
    }

    modifier onlyAfter(uint _time) {
        require(now > _time);
        _;
    }

    modifier onlyBefore(uint _time) {
        require(now < _time);
        _;
    }

    function drfp(string bidManagerName, string rfpName, string specLocation,
                    uint advertisingStart, uint biddingStart, uint revealStart, uint awardDate)
    {
        bidManager.name = bidManagerName;
        bidPackage.name = rfpName;
        bidPackage.specLocation = specLocation;
        periodStarts.advertisingStart = advertisingStart;
        periodStarts.biddingStart = biddingStart;
        periodStarts.revealStart = revealStart;
        periodStarts.awardDate = awardDate;
    }

    // private key is set later
    function addBidder(address _address, string _name, string _publicKey)
        onlyOwner()
        onlyBefore(periodStarts.biddingStart) {
        bidders[_address] = Bidder(true, _name, _publicKey, "", "");
    }

    function addBidLocation(string _bidLocation)
        onlyBidders() {
        bidders[msg.sender].bidLocation = _bidLocation;
    }

    function addPrivateKey(string _privateKey)
        onlyAfter(periodStarts.revealStart)
        onlyBidders() {
        bidders[msg.sender].privateKey = _privateKey;
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
