from network import get_signature

import os
import requests
import random
import string
import time


class ServiceToken:
    def __init__(
        self,
        owner: dict,
        config: dict
    ):
        self.ownerAddress = owner['address']
        self.ownerSecret = owner['secret']
        self.server_url = config['server_url']
        self.service_api_key = config['service_api_key']
        self.service_api_secret = config['service_api_secret']
        self.contractId = config['service_token_id']

    def get_info(
        self
    ):
        nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        timestamp = int(round(time.time() * 1000))

        path = '/v1/service-tokens'

        headers = {
            'service-api-key': self.service_api_key,
            'nonce': nonce,
            'timestamp': str(timestamp)
        }

        signature = get_signature('GET', path, nonce, timestamp, self.service_api_secret)
        headers['signature'] = signature

        res = requests.get(self.server_url + path, headers=headers)
        return res.json()

    def mint(
        self,
        toAddress: str,
        amount: str
    ):
        nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        timestamp = int(round(time.time() * 1000))

        path = '/v1/service-tokens/' + self.contractId + '/mint'

        request_body = {
            'ownerAddress': self.ownerAddress,
            'ownerSecret': self.ownerSecret,
            'toAddress': toAddress,
            'amount': amount
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

        path = '/v1/service-tokens/' + self.contractId + '/holders'

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

    def transfer(
        self,
        fromAddress: str,
        walletSecret: str,
        toAddress: str,
        amount: str
    ):
        # transfer service tokens

        nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        timestamp = int(round(time.time() * 1000))

        path = '/v1/wallets/' + fromAddress + '/service-tokens/' + self.contractId + '/transfer'

        request_body = {
            'walletSecret': walletSecret,
            'toAddress': toAddress,
            'amount': amount
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

    # Service Token
    st = ServiceToken(owner, config)

    # mint ST
    res = st.mint(
        user_A['address'],
        '600000'
    )
    print(res)

    # get holders
    res = st.holders()
    print(res)

    # get info
    res = st.get_info()
    print(res)

    # transfer ST
    res = st.transfer(
        fromAddress=user_A['address'],
        walletSecret=user_A['secret'],
        toAddress=user_B['address'],
        amount='700'
    )
    print(res)
