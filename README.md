# aavegotchi-pet-all
A simple repository for petting all of a user's Aavegotchis

# How to use

```
pip3 install web3
pip3 install eth_account
pip3 install python-decouple
```

Create a .env file with the following variables
PRIVATE_KEY=YOUR_PRIVATE_KEY
MATIC_RPC=A_MATIC_RPC

The default matic RPC is `https://rpc-mainnet.maticvigil.com`
# For Use with Docker

Modifiy the Dockerfile adding in the above ENV variables

```
docker build -t aavegotchi-pet-all .
docker run -d aavegotchi-pet-all
```
