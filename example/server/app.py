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
sys.path.append('../../caller/')
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


# depricated
# @app.route('/uploadimage', methods=['POST', 'PUT'])
# def uploadimage():
#     _who = request.form['who']
#     _name = request.form['name']
#     _file = request.files['file']
#     _amount = 1 if 'amount' not in request.form else int(request.form['amount'])
#     _price = None if 'price' not in request.form else int(request.form['price'])

#     res = fantopia.upload_image(
#         who=_who,
#         name=_name,
#         image_bytes=_file.read(),
#         # description=_description
#         amount=_amount,
#         price=_price
#     )
#     pprint(res)

#     return json.dumps(res) or 'Success'


# # depricated
# @app.route('/uploadproduct', methods=['POST'])
# def uploadproduct():
#     params = json.loads(request.get_data(), encoding='utf-8')
#     if len(params) == 0:
#         return 'No parameter'

#     fantopia.upload_product(
#         name=params['name'],
#         nft_number=params['nft_number'],
#         nft_name=params['nft_name'],
#     )

#     return 'Success'


@app.route('/getimage', methods=['POST'])
def getimage():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    pk = params['pk']

    res = fantopia.getImage(pk)

    return json.dumps(res)


@app.route('/getallimages', methods=['POST'])
def getdetail():
    params = {}
    try:
        params = json.loads(request.get_data(), encoding='utf-8')
    except:
        pass

    startNum = params['startNum'] if 'startNum' in params else 0
    endNum = params['endNum'] if 'endNum' in params else 100

    res = fantopia.getAllImages(startNum=startNum, endNum=endNum)

    return json.dumps(res)


@app.route('/updatefavorite', methods=['POST'])
def updatefavorite():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    pk = params['pk']
    favor = params['favor'] if 'favor' in params else True

    fantopia.updateFavorite(pk, favor)

    return 'Success'


@app.route('/sellreset', methods=['POST'])
def sellreset():
    params = {}
    try:
        params = json.loads(request.get_data(), encoding='utf-8')
    except:
        pass

    startNum = params['startNum'] if 'startNum' in params else 0
    endNum = params['endNum'] if 'endNum' in params else 100

    res = fantopia.sellReset(startNum=startNum, endNum=endNum)

    return json.dumps(res)


@app.route('/buyimage', methods=['POST'])
def buyimage():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    res = fantopia.buy(
        fromAddress=params['fromAddress'],
        toAddress=params['toAddress'],
        tokenIndex=params['tokenIndex'],
        price=params['price'],
        pk = params['pk']
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
