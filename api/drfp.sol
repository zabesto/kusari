pragma solidity ^0.4.8;

// Decentralized RFP Process
contract drfp {

    struct Bidder {
        bool isValid;
        address account;
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

    mapping (address => Bidder) public bidders;
    address[] public bidderWhitelist;
    address public testAddress;

    enum RFPPeriods { Advertising, Bidding, Reveal, Award }
    RFPPeriods constant defaultChoice = RFPPeriods.Advertising;
    BidManager public bidManager;
    BidPackage public bidPackage;
    PeriodStarts public periodStarts;

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
        owner = msg.sender;
        bidManager.name = bidManagerName;
        bidPackage.name = rfpName;
        bidPackage.specLocation = specLocation;
        periodStarts.advertisingStart = advertisingStart;
        periodStarts.biddingStart = biddingStart;
        periodStarts.revealStart = revealStart;
        periodStarts.awardDate = awardDate;

        // TEMP
        //bidderWhitelist.push(0xb9b35f2bd3b6e13721a349bde7f1f0a902ae7e57);
    }

    function getWhitelist() returns (address[]){
        return bidderWhitelist;
    }

//    function getWhitelist(int index) returns (address){
//        return bidderWhitelist(index);
//    }

    function addBidder(address _address)
        onlyOwner() {
        //onlyBefore(periodStarts.biddingStart) {
        bidders[_address] = Bidder(true, _address, "", "", "", "");
        testAddress = _address;
        bidderWhitelist.push(_address);
    }

    function addBidderName(string _name)
        //onlyAfter(periodStarts.advertisingStart)
        onlyBidders() {
        bidders[msg.sender].name = _name;
    }

    function addPublicKey(string _publicKey)
        //onlyAfter(periodStarts.biddingStart)
        onlyBidders() {
        bidders[msg.sender].publicKey = _publicKey;
    }

    function addBidLocation(string _bidLocation)
        //onlyAfter(periodStarts.biddingStart)
        onlyBidders() {
        bidders[msg.sender].bidLocation = _bidLocation;
    }

    function addPrivateKey(string _privateKey)
        //onlyAfter(periodStarts.revealStart)
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
