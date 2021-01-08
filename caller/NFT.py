from network import get_signature

import os
import requests
import random
import string
import time


class NFT:
    def __init__(
        self,
        tokenType: str,
        owner: dict,
        config: dict
    ):
        self.tokenType = tokenType

        self.ownerAddress = owner['address']
        self.ownerSecret = owner['secret']
        self.server_url = config['server_url']
        self.service_api_key = config['service_api_key']
        self.service_api_secret = config['service_api_secret']
        self.contractId = config['item_token_id']

    def mint(
        self,
        to_: str,
        name: str,
        meta: str = None
    ):
        nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        timestamp = int(round(time.time() * 1000))

        path = '/v1/item-tokens/' + self.contractId + '/non-fungibles/' + self.tokenType + '/mint'

        if meta is not None:
            request_body = {
                'ownerAddress': self.ownerAddress,
                'ownerSecret': self.ownerSecret,
                'toAddress': to_,
                'name': name,
                'meta': meta
            }
        else:
            request_body = {
                'ownerAddress': self.ownerAddress,
                'ownerSecret': self.ownerSecret,
                'toAddress': to_,
                'name': name
            }

        headers = {
            'service-api-key': self.service_api_key,
            'nonce': nonce,
            'timestamp': str(timestamp),
            'Content-Type': 'application/json'
        }

        signature = get_signature('POST', path, nonce, timestamp, self.service_api_secret, body=request_body)
        headers['signature'] = signature

        res = requests.post(self.server_url + path, headers=headers, json=request_body)
        return res.json()

    def holders(
        self
    ):
        nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        timestamp = int(round(time.time() * 1000))

        path = '/v1/item-tokens/' + self.contractId + '/non-fungibles/' + self.tokenType + '/holders'

        query_params = {
            'limit': 10,
            'orderBy': 'desc',
            'page': 1
        }

        headers = {
            'service-api-key': self.service_api_key,
            'nonce': nonce,
            'timestamp': str(timestamp)
        }

        signature = get_signature('GET', path, nonce, timestamp, self.service_api_secret, query_params)
        headers['signature'] = signature

        res = requests.get(self.server_url + path, params=query_params, headers=headers)
        return res.json()

    def holder(
        self,
        number: str
    ):
        nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        timestamp = int(round(time.time() * 1000))

        path = '/v1/item-tokens/' + self.contractId + '/non-fungibles/' + self.tokenType + '/' + number + '/holder'

        headers = {
            'service-api-key': self.service_api_key,
            'nonce': nonce,
            'timestamp': str(timestamp)
        }

        signature = get_signature('GET', path, nonce, timestamp, self.service_api_secret)
        headers['signature'] = signature

        res = requests.get(self.server_url + path, headers=headers)
        return res.json()

    def get_info(
        self,
        number: str
    ):
        nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        timestamp = int(round(time.time() * 1000))

        path = '/v1/item-tokens/' + self.contractId + '/non-fungibles/' + self.tokenType + '/' + number

        headers = {
            'service-api-key': self.service_api_key,
            'nonce': nonce,
            'timestamp': str(timestamp)
        }

        signature = get_signature('GET', path, nonce, timestamp, self.service_api_secret)
        headers['signature'] = signature

        res = requests.get(self.server_url + path, headers=headers)
        return res.json()

    def update_info(
        self,
        number: str,
        name: str,
        meta: str = None
    ):
        nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        timestamp = int(round(time.time() * 1000))

        path = '/v1/item-tokens/' + self.contractId + '/non-fungibles/' + self.tokenType + '/' + number

        request_body = {
            'ownerAddress': self.ownerAddress,
            'ownerSecret': self.ownerSecret,
            'name': name,
            'meta': meta
        }

        headers = {
            'service-api-key': self.service_api_key,
            'nonce': nonce,
            'timestamp': str(timestamp),
            'Content-Type': 'application/json'
        }

        signature = get_signature('PUT', path, nonce, timestamp, self.service_api_secret, body=request_body)
        headers['signature'] = signature

        res = requests.put(self.server_url + path, headers=headers, json=request_body)
        return res.json()

    def transfer(
        self,
        fromAddress: str,
        walletSecret: str,
        toAddress: str,
        tokenIndex: str
    ):
        # transfer non fungible item tokens
        # tokenId = concat(tokenType, tokenIndex)

        nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        timestamp = int(round(time.time() * 1000))

        path = '/v1/wallets/' + fromAddress + '/item-tokens/' + self.contractId + '/non-fungibles/' + self.tokenType + '/' + tokenIndex + '/transfer'

        request_body = {
            'walletSecret': walletSecret,
            'toAddress': toAddress
        }

        headers = {
            'service-api-key': self.service_api_key,
            'nonce': nonce,
            'timestamp': str(timestamp),
            'Content-Type': 'application/json'
        }

        signature = get_signature('POST', path, nonce, timestamp, self.service_api_secret, body=request_body)
        headers['signature'] = signature

        res = requests.post(self.server_url + path, headers=headers, json=request_body)
        return res.json()


if __name__ == "__main__":
    # You can check more info. about Tx at below:
    # https://explorer.blockchain.line.me/cashew/transaction/{txHash}

    import json

    # Load info.
    with open('./users.json') as f:
        users = json.load(f)

    owner = users['Owner']
    artist = users['Artist']
    user_A = users['Customer_A']
    user_B = users['Customer_B']

    with open('./config.json') as f:
        config = json.load(f)

    # NFT
    nft = NFT('10000001', owner, config)

    # mint NFT
    res = nft.mint(
        to_=user_A['address'],
        name="SOME",
        meta="THING"
    )
    print(res)

    # get NFT holders
    res = nft.holders()
    print(res)

    # get specific NFT's holder
    res = nft.holder(
        number='00000002'
    )
    print(res)

    # get specific NFT's info.
    res = nft.get_info(
        number='00000002'
    )
    print(res)

    # update token info.
    res = nft.update_info(
        number='00000002',
        name='BTS1',
        meta='A BTS picture'
    )
    print(res)

    # transfer NFT
    res = nft.transfer(
        fromAddress=user_A['address'],
        walletSecret=user_A['secret'],
        toAddress=user_B['address'],
        tokenIndex='00000018'
    )
    print(res)
