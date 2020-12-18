import os

import requests
import random
import string
import time

from network import get_signature


def get(

):
    nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    timestamp = int(round(time.time() * 1000))

    path = '/v1/service-tokens'

    headers = {
        'service-api-key': service_api_key,
        'nonce': nonce,
        'timestamp': str(timestamp)
    }

    signature = get_signature('GET', path, nonce, timestamp, service_api_secret)
    headers['signature'] = signature

    res = requests.get(server_url + path, headers=headers)
    return res.json()


def mint(
    contractID: str,
    toAddress: str,
    amount: str
):
    nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    timestamp = int(round(time.time() * 1000))

    path = '/v1/service-tokens/' + contractID + '/mint'

    request_body = {
        'ownerAddress': ownerAddress,
        'ownerSecret': ownerSecret,
        'toAddress': toAddress,
        'amount': amount
    }

    headers = {
        'service-api-key': service_api_key,
        'nonce': nonce,
        'timestamp': str(timestamp),
        'Content-Type': 'application/json'
    }

    signature = get_signature('POST', path, nonce, timestamp, service_api_secret, body=request_body)
    headers['signature'] = signature

    res = requests.post(server_url + path, headers=headers, json=request_body)
    return res.json()


def burn():
    pass


def holders(
    contractID: str,
):
    nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    timestamp = int(round(time.time() * 1000))

    path = '/v1/service-tokens/' + contractID + '/holders'

    query_params = {
        'limit': 10,
        'orderBy': 'desc',
        'page': 1
    }

    headers = {
        'service-api-key': service_api_key,
        'nonce': nonce,
        'timestamp': str(timestamp)
    }

    signature = get_signature('GET', path, nonce, timestamp, service_api_secret, query_params)
    headers['signature'] = signature

    res = requests.get(server_url + path, params=query_params, headers=headers)
    return res.json()


if __name__ == "__main__":
    pass

    # You can check more info. about Tx at below:
    # https://explorer.blockchain.line.me/cashew/transaction/{txHash}

    # Hyperparams.
    server_url = os.environ['SERVER_URL']
    service_api_key = os.environ['SERVICE_API_KEY']
    service_api_secret = os.environ['SERVICE_AP_SECRET']
    ownerAddress = os.environ['OWNER_ADDRESS']
    ownerSecret = os.environ['OWNER_SECRET']

    # # get service token
    # res = get()
    # print(res)

    # # mint service token
    # res = mint(
    #     contractID='928c9877',
    #     toAddress='tlink18vsd3cautlyt759sw5hq9tydhzrsrgrmprs4f0',
    #     amount='2000'
    # )
    # print(res)

    # check holders
    res = holders(
        contractID='928c9877'
    )
    print(res)
