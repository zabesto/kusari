pragma solidity ^0.4.0;

// Decentralized RFP Process
contract dfrp {

    struct Bidder {
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
        uint AdvertisingStart;
        uint BiddingStart;
        uint RevealStart;
        uint Award;
    }

    mapping (address => Bidder) bidderWhitelist;

    enum RFPPeriods { Advertising, Bidding, Reveal, Award }
    RFPPeriods currentPeriod;
    RFPPeriods constant defaultChoice = RFPPeriods.Advertising;
    BidManager bidManager;

    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    modifier onlyBidders() {
        require(bidderWhitelist[msg.sender])
        _;
    }

    modifier onlyAfter(uint _time) {
        require(now >= _time);
        _;
    }


    // ctor
    function drfp(BidManager _manager, Bidder[] _bidders, BidPackage _package, PeriodStarts _periods) {
        owner = msg.sender;

    }

    function getCurrentPeriod() returns (RFPPeriods) {
        return currentPeriod;
    }

    function reveal() onlyOwner {
        if (block.timestamp < deadline) throw;      // TODO investigate block.timestamp

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
        throw;
    }
}
