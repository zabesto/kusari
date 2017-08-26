# kusari FTW!


## API

### Install Dependencies

```sh
pip install flask
pip install -U flask-cors --upgrade --ignore-installed six
pip install ipfsapi
pip install py-solc
pip install web3[tester]

# install solidity
brew install node
brew tap ethereum/ethereum
brew install ethereum
brew install solidity
npm install -g ethereumjs-testrpc
npm install -g truffle
```

### Run

```sh
# start flask server
cd ~/kusari/api
export FLASK_APP=rfpflask.py
flask run

# start ipfs
ipfs daemon

# start test rpc
testrpc
```
