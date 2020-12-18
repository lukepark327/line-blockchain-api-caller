import base64
import time
import hashlib
import json
from flask import Flask, request
from pprint import pprint

from main import Image, Fantopia
from NFT import NFT
from ST import ServiceToken
from utils import get_transaction_info


app = Flask('app')


@app.route('/adduser', methods=['POST'])
def adduser():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    res = fantopia.add_user(params)
    pprint(res)

    return json.dumps(res) or 'Success'


@app.route('/addartist', methods=['POST'])
def addartist():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    res = fantopia.add_artist(params)
    pprint(res)

    return json.dumps(res) or 'Success'


@app.route('/uploadimage', methods=['POST'])
def uploadimage():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    res = fantopia.upload_image(
        who=params['address'],
        imageURI=params['imageURI'],
        name=params['name'],
        description=params['description'],
        amount=int(params['amount']),
        price=int(params['price'])
    )
    pprint(res)

    return json.dumps(res) or 'Success'


@app.route('/buyimage', methods=['POST'])
def buyimage():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    res = fantopia.buy(
        fromAddress=params['fromAddress'],
        toAddress=params['toAddress'],
        tokenIndex=params['tokenIndex'],
        price=params['price']
    )
    pprint(res)

    return json.dumps(res) or 'Success'


@app.route('/gettx', methods=['POST'])
def gettx():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    res = get_transaction_info(
        server_url=fantopia.config['server_url'],
        service_api_key=fantopia.config['service_api_key'],
        service_api_secret=fantopia.config['service_api_secret'],
        txHash=params['txHash']
    )
    pprint(res)

    return json.dumps(res) or 'Success'


@app.route('/test', methods=['GET'])
def test():
    ress = []

    # Load info.
    with open('./users.json') as f:
        users = json.load(f)

    owner = users['Owner']
    artist = users['Artist']
    user_A = users['Customer_A']
    user_B = users['Customer_B']

    with open('./config.json') as f:
        config = json.load(f)

    # Add artist
    fantopia.add_artist(artist)

    # Add user
    fantopia.add_user(user_A)
    fantopia.add_user(user_B)

    # Upload image
    # description must have 'artist' & 'price' field
    # which formal one is the wallet address of the artist.
    res = fantopia.upload_image(
        who=user_A['address'],
        imageURI='./images/1.jpeg',
        name='NVIDIA RTX TITAN',
        description={
            'artist': artist['address'],
            'something': 'nothing'
        },
        amount=5,
        price=10000
    )
    pprint(res)
    ress.append(res)

    # Buy image
    res = fantopia.buy(
        fromAddress=user_B['address'],
        toAddress=user_A['address'],
        tokenIndex='00000085',
        price='10000'
    )
    pprint(res)
    ress.append(res)

    res = get_transaction_info(
        server_url=config['server_url'],
        service_api_key=config['service_api_key'],
        service_api_secret=config['service_api_secret'],
        txHash="DCD0B2D32E9329D77AA642A55DC10469A876767493D2F60254A70E4DCD099202"
    )
    pprint(res)
    ress.append(res)

    return json.dumps(ress) or 'Success'


if __name__ == "__main__":
    # Load info.
    with open('./users.json') as f:
        users = json.load(f)

    owner = users['Owner']

    with open('./config.json') as f:
        config = json.load(f)

    # Set Fantopia service
    fantopia = Fantopia(owner, config)

    app.run(host='0.0.0.0', debug=True)
