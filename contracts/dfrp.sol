pragma solidity ^0.4.0;


contract dfrp {
    address public owner;
    uint public deadline;
    bool ended;

    modifier onlyOwner() {
        if (msg.sender != owner) throw;
        _
    }

    modifier

    // ctor
    function drfp(uint _deadline) {
        owner = msg.sender;

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
