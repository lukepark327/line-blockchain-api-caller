import base64
import time
import hashlib
import json
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
from pprint import pprint

# from fantopia import Fantopia
from fantopia_offline import Fantopia

import sys
sys.path.append('../../')
from NFT import NFT
from ST import ServiceToken
from utils import get_transaction_info


app = Flask('app')


@app.route('/adduser', methods=['POST'])
def adduser():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    fantopia.add_user(params)

    return 'Success'


@app.route('/addartist', methods=['POST'])
def addartist():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    fantopia.add_artist(params)

    return 'Success'


@app.route('/uploadimage', methods=['POST', 'PUT'])
def uploadimage():
    _who = request.form['who']
    _name = request.form['name']
    _file = request.files['file']
    _amount = 1 if 'amount' not in request.form else int(request.form['amount'])
    _price = None if 'price' not in request.form else int(request.form['price'])

    res = fantopia.upload_image(
        who=_who,
        name=_name,
        image_bytes=_file.read(),
        # description=_discription
        amount=_amount,
        price=_price
    )
    pprint(res)

    return json.dumps(res) or 'Success'


@app.route('/uploaddetail', methods=['POST'])
def uploaddetail():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    _amount = 1 if 'amount' not in params else int(params['amount'])
    _price = None if 'price' not in params else int(params['price'])

    res = fantopia.upload_detail(
        number=params['tokenIndex'],
        name=params['name'],
        new_description=params['description'],
        amount=_amount,
        price=_price
    )
    pprint(res)

    return json.dumps(res) or 'Success'


@app.route('/getimage', methods=['POST'])
def getimage():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    serverBaseURI = 'images' if 'serverBaseURI' not in params else params['serverBaseURI']
    name = params['name']

    return send_file(serverBaseURI + '/' + name, as_attachment=True)


@app.route('/getdetail', methods=['POST'])
def getdetail():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    name = params['name']

    res = []

    res.append(fantopia.img_server.get_description(
        name=name
        # number=i,
    ))

    return json.dumps(res) or 'Success'


@app.route('/getdetails', methods=['POST'])
def getdetails():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    names = params['names']

    res = []

    for name in names:
        res.append(fantopia.img_server.get_description(
            name=name
            # number=i,
        ))

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


@app.route('/uploadproduct', methods=['POST'])
def uploadproduct():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    fantopia.upload_product(
        name=params['name'],
        nft_number=params['nft_number'],
        nft_name=params['nft_name'],
    )

    return 'Success'


@app.route('/getproductimage', methods=['POST'])
def getproduct():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    info = fantopia.get_product(
        name=params['name']
    )
    _name = info['nft_name']

    serverBaseURI = 'images' if 'serverBaseURI' not in params else params['serverBaseURI']

    return send_file(serverBaseURI + '/' + _name, as_attachment=True)


@app.route('/getproductdetail', methods=['POST'])
def getproductdetail():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    res = fantopia.get_nft_detail(
        name=params['name']
    )
    pprint(res)

    return json.dumps(res) or 'Success'


@app.route('/getproductdetails', methods=['POST'])
def getproductdetails():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    names = params['names']

    res = []

    for name in names:
        res.append(fantopia.get_nft_detail(
            name=name
        ))
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
    name = '1.jpeg'
    with open('images/' + name, 'rb') as f:
        image_bytes = f.read()

    res = fantopia.upload_image(
        who=user_A['address'],
        name=name,
        image_bytes=image_bytes,
        description={
            # 'SN':
            'artist': artist['address'],  # 'IU(01)'
            'agency': 'Loen Entertainment',
            'schedule': '2019 IU concert',
            'date': '12/01/2019',
            'minted': '01/12/2020'
            # 'owner':
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
