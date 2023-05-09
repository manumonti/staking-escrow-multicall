# Staking Escrow Multicall

This Python script uses [nucypher/multicall.py](https://github.com/nucypher/multicall.py) package to
request stakers information from the [NuCypher Staking
Escrow](https://etherscan.io/address/0xbbd3c0c794f40c4f993b03f65343acc6fcfcb2e2) smartcontract.

## Installation

Python version >= 3.8

It is needed to clone the multicall.py package and install it:

```bash
git clone git@github.com:nucypher/multicall.py.git
pip install -e ~/Projects/nucypher/multicall.py
```

It is needed to have an env variable with a Web3 provider URI:

```bash
export WEB3_PROVIDER_URI=https://mainnet.infura.io/v3/<API_KEY>
```

## Use:

```bash
python escrow-multicall.py
```
