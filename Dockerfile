FROM python:3

ADD petall.py / 

COPY abi.json / 
COPY aavegotchiDiamond.txt / 

ENV PRIVATE_KEY=YOUR_PRIVATE_KEY
ENV MATIC_RPC=https://rpc-mainnet.maticvigil.com

RUN pip install web3 eth_account python-decouple

CMD [ "python", "-u", "./petall.py" ]
