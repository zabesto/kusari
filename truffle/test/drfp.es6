var DRFP = artifacts.require("./drfp.sol");

contract('drfp', function(accounts) {
    bidManager = "DJ Carter";
    rfpName = "Bids for Pandas carrying kusari-gundo";
    specLocation = "0x0923409823049AFAF234";
    advertisingStart = 1503773778;
    biddingStart = 1503860178;
    revealStart = 1503946578;
    awardDate = 1503773778;

    it("should be able to get a bid manager", () => {

        return DRFP.deployed().then(instance => {
            return instance.bidManager.call().then(result => {
                assert.equal(result, bidManager);
            });
        });
    });

    it("should be able to get the advertising start date", () => {

        return DRFP.deployed().then(instance => {
            return instance.periodStarts.call().then(result => {
                assert.equal(result[0], advertisingStart);
            });
        });
    });

    it("should be able to get the bidding start date", () => {

        return DRFP.deployed().then(instance => {
            return instance.periodStarts.call().then(result => {
                assert.equal(result[1], biddingStart);
            });
        });
    });

    it("should be able to get the reveal start date", () => {

        return DRFP.deployed().then(instance => {
            return instance.periodStarts.call().then(result => {
                assert.equal(result[2], revealStart);
            });
        });
    });

    it("should be able to get the award date", () => {

        return DRFP.deployed().then(instance => {
            return instance.periodStarts.call().then(result => {
                assert.equal(result[3], awardDate);
            });
        });
    });



            // assert.equal(txResult.logs.length, 1); // make sure it fired
        // return instance.fund({ from: accounts[0], value: web3.toWei(4, 'ether') }).then(txResult => {
        //         assert.equal(txResult.logs.length, 1); // make sure it fired
        //         assert.equal(txResult.logs[0].event, "Deposit");
        //         assert.equal(txResult.logs[0].args['_amount'], web3.toWei(4, 'ether'));
        //     }
        // );
});
