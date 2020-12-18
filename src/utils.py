from network import get_signature

import os
import requests
import random
import string
import time


def get_transaction_info(
    server_url: str,
    service_api_key: str,
    service_api_secret: str,
    txHash: str
):
    nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    timestamp = int(round(time.time() * 1000))

    path = '/v1/transactions/' + txHash

    headers = {
        'service-api-key': service_api_key,
        'nonce': nonce,
        'timestamp': str(timestamp)
    }

    signature = get_signature('GET', path, nonce, timestamp, service_api_secret)
    headers['signature'] = signature

    res = requests.get(server_url + path, headers=headers)
    return res.json()


# def transferBC(
#     fromAddress: str,
#     walletSecret: str,
#     toAddress: str,
#     amount: str
# ):
#     # transfer base coins

#     nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
#     timestamp = int(round(time.time() * 1000))

#     path = '/v1/wallets/' + fromAddress + '/base-coin/transfer'

#     request_body = {
#         'walletSecret': walletSecret,
#         'toAddress': toAddress,
#         'amount': amount
#     }

#     headers = {
#         'service-api-key': service_api_key,
#         'nonce': nonce,
#         'timestamp': str(timestamp),
#         'Content-Type': 'application/json'
#     }

#     signature = get_signature('POST', path, nonce, timestamp, service_api_secret, body=request_body)
#     headers['signature'] = signature

#     res = requests.post(server_url + path, headers=headers, json=request_body)
#     return res.json()
