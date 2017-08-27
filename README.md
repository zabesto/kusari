# kusari FTW!

## API

### Install Dependencies

```sh
pip install flask
pip install ipfsapi
pip install py-solc
pip install web3
pip install pycrypto

# install solidity
brew install node
brew tap ethereum/ethereum
brew install ethereum
brew install solidity
npm install -g ethereumjs-testrpc
npm install -g truffle

# install ipfs
[IPFS](https://ipfs.io/docs/install/#installing-from-a-prebuilt-package)
sudo mv go-ipfs/ipfs /usr/local/bin/ipfs
```

### Run

```sh
# start ipfs
ipfs daemon

# start test rpc
testrpc

# start flask server
cd ~/kusari/api
export FLASK_APP=rfpflask.py
flask run
```
