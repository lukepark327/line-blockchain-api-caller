import os

import requests
import random
import string
import time

from network import get_signature


def mint(
    contractId: str,
    to_: str,
    name: str,
    meta: str = None
):
    nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    timestamp = int(round(time.time() * 1000))

    path = '/v1/item-tokens/' + contractId + '/non-fungibles/10000001/mint'

    if meta is not None:
        request_body = {
            'ownerAddress': ownerAddress,
            'ownerSecret': ownerSecret,
            'toAddress': to_,
            'name': name,
            'meta': meta
        }
    else:
        request_body = {
            'ownerAddress': ownerAddress,
            'ownerSecret': ownerSecret,
            'toAddress': to_,
            'name': name
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


def burn(contractId: str, number: str, meta=None):
    pass


def holders(
    contractId: str
):
    nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    timestamp = int(round(time.time() * 1000))

    path = '/v1/item-tokens/' + contractId + '/non-fungibles/10000001/holders'

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


def holder(
    contractId: str,
    number: str
):
    nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    timestamp = int(round(time.time() * 1000))

    path = '/v1/item-tokens/' + contractId + '/non-fungibles/10000001/' + number + '/holder'

    headers = {
        'service-api-key': service_api_key,
        'nonce': nonce,
        'timestamp': str(timestamp)
    }

    signature = get_signature('GET', path, nonce, timestamp, service_api_secret)
    headers['signature'] = signature

    res = requests.get(server_url + path, headers=headers)
    return res.json()


def get(
    contractId: str,
    number: str
):
    nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    timestamp = int(round(time.time() * 1000))

    path = '/v1/item-tokens/' + contractId + '/non-fungibles/10000001/' + number

    headers = {
        'service-api-key': service_api_key,
        'nonce': nonce,
        'timestamp': str(timestamp)
    }

    signature = get_signature('GET', path, nonce, timestamp, service_api_secret)
    headers['signature'] = signature

    res = requests.get(server_url + path, headers=headers)
    return res.json()


def update(
    contractId: str,
    number: str,
    name: str,
    meta: str = None
):
    nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    timestamp = int(round(time.time() * 1000))

    path = '/v1/item-tokens/' + contractId + '/non-fungibles/10000001/' + number

    request_body = {
        'ownerAddress': ownerAddress,
        'ownerSecret': ownerSecret,
        'name': name,
        'meta': meta
    }

    headers = {
        'service-api-key': service_api_key,
        'nonce': nonce,
        'timestamp': str(timestamp),
        'Content-Type': 'application/json'
    }

    signature = get_signature('PUT', path, nonce, timestamp, service_api_secret, body=request_body)
    headers['signature'] = signature

    res = requests.put(server_url + path, headers=headers, json=request_body)
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

    # # mint NFT
    # res = mint(
    #     contractId='658b4b8a',
    #     to_='tlink14t0y6xwez6uydx0m7tsdlazljn5ukp8s056mw8',
    #     name="IU4",
    #     meta="IU Picture #4"
    # )
    # print(res)

    # # check NFT holders
    # res = holders(
    #     contractId='658b4b8a'
    # )
    # print(res)

    # # check specific NFT's holder
    # res = holder(
    #     contractId='658b4b8a',
    #     number='00000002'
    # )
    # print(res)

    # check specific NFT's info.
    res = get(
        contractId='658b4b8a',
        number='00000002'
    )
    print(res)

    # # update token info.
    # res = update(
    #     contractId='658b4b8a',
    #     number='00000002',
    #     name='BTS1',
    #     meta='A BTS picture'
    # )
    # print(res)