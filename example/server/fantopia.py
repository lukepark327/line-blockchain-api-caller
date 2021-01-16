import base64
import time
import hashlib
import json
from tqdm import tqdm

from DB import DB

import sys
sys.path.append('../../caller/')
from utils import get_transaction_info
from ST import ServiceToken
from NFT import NFT


class Fantopia:
    def __init__(
        self,
        owner: dict,
        config: dict
    ):
        self.owner = {}
        self.ownerAddress = owner['address']
        self.owner[self.ownerAddress] = owner['secret']

        self.artists = {}
        self.users = {}

        self.tokenType = '10000001'
        self.nft = NFT(self.tokenType, owner, config)   # NFT
        self.st = ServiceToken(owner, config)           # [FAN]

        self.artist_fee = 0.0025    # 0.25%
        self.platform_fee = 0.0005  # 0.05%

        self.config = config

        self.DB = DB()
        _ = self.insertSamples(startNum=0, endNum=20)

    def insertSamples(self, startNum=0, endNum=20):
        res = []

        print("Init: Upload Samples...")
        for i in tqdm(range(startNum, endNum)):
            with open('./samples/sample' + str(i) + '.json', 'r') as f:
                sample = json.load(f)

            # index
            idx = self.DB._getPkIndex()
            sample['pk'] = idx

            # blockchain
            # if sample['type'] == 'image':
            new_nft_log = self.nft.mint(
                to_=sample['owner_addr'],
                name='image_' + sample['pk'],
                meta=json.dumps({
                    'pk': sample['pk'],
                    'type': sample['type'],
                    'artist_addr': sample['artist_addr'],
                    'price': sample['price'],
                })
            )

            # tx hash
            tx_hash = new_nft_log['responseData']['txHash']

            while True:
                time.sleep(0.1)
                new_nft_tx = get_transaction_info(
                    server_url=self.config['server_url'],
                    service_api_key=self.config['service_api_key'],
                    service_api_secret=self.config['service_api_secret'],
                    txHash=tx_hash
                )
                if new_nft_tx['statusMessage'] == 'Success':
                    break
            serial_num = new_nft_tx['responseData']['logs'][0]['events'][1]['attributes'][2]['value']
            sample['serial_num'] = serial_num

            # insert at DB
            self.DB.table[idx] = sample

            res.append(tx_hash)

        return res

    # def change_owner(self):
    #     pass

    def add_artist(self, artist: dict):
        self.artists[artist['address']] = artist['secret']

    def add_user(self, user: dict):
        self.users[user['address']] = user['secret']

    def is_artist(self, who: str):
        return who in self.artists

    def is_user(self, who: str):
        return who in self.users

    # DB

    # deprecated
    # def upload(self): pass

    def getImage(self, primaryKey: str):
        return self.DB.getImage(primaryKey)

    def getAllImages(self, startNum=0, endNum=100):
        return self.DB.getAllImages(startNum=startNum, endNum=endNum)

    def updateFavorite(self, primaryKey: str, favor=True):
        self.DB.updateFavorite(primaryKey, favor)

    def sellReset(self, startNum=0, endNum=100):
        self.DB.sellReset(startNum=startNum, endNum=endNum)

    def buy(
        self,
        pk: str,
        fromAddress: str,
        toAddress: str,
        tokenIndex: str = None,
        price: str = None
    ):
        tokenIndex = tokenIndex or self.DB.table[pk]['serial_num'].replace(self.tokenType, '')

        meta = json.loads(self.nft.get_info(tokenIndex)['responseData']['meta'])
        artistAddress = meta['artist_addr']
        price_ = meta['price']

        if price is None:
            price = price_
        elif price < price_:
            return

        price = int(price)
        for_artist, for_platform = int(price * self.artist_fee), int(price * self.platform_fee)
        for_receiver = int(price - for_artist - for_platform)

        price = str(price)
        for_artist, for_platform, for_receiver =\
            str(for_artist), str(for_platform), str(for_receiver)

        # blockchain
        res = []
        res.append(self.nft.transfer(
            fromAddress=toAddress,
            walletSecret=self.users[toAddress],
            toAddress=fromAddress,
            tokenIndex=tokenIndex
        )['responseData']['txHash'])
        res.append(self.st.transfer(
            fromAddress=fromAddress,
            walletSecret=self.users[fromAddress],
            toAddress=artistAddress,
            amount=for_artist
        )['responseData']['txHash'])
        res.append(self.st.transfer(
            fromAddress=fromAddress,
            walletSecret=self.users[fromAddress],
            toAddress=self.ownerAddress,
            amount=for_platform
        )['responseData']['txHash'])
        res.append(self.st.transfer(
            fromAddress=fromAddress,
            walletSecret=self.users[fromAddress],
            toAddress=toAddress,
            amount=for_receiver
        )['responseData']['txHash'])

        # update DB
        self.DB.table[pk]['is_selled'] = True
        self.DB.table[pk]['owner_addr'] = fromAddress

        # return txs
        return res


if __name__ == "__main__":
    from pprint import pprint

    # Load info.
    with open('./users.json') as f:
        users = json.load(f)

    owner = users['Owner']
    artist = users['Artist']
    user_A = users['Customer_A']
    user_B = users['Customer_B']

    with open('./config.json') as f:
        config = json.load(f)

    # Set Fantopia service
    fantopia = Fantopia(owner, config)

    # Add artist
    fantopia.add_artist(artist)

    # Add user
    fantopia.add_user(user_A)
    fantopia.add_user(user_B)

    # Buy image
    res = fantopia.buy(
        pk="1",
        fromAddress=user_B['address'],
        toAddress=user_A['address'],
        # tokenIndex='00000085',
        price='32400'
    )
    pprint(res)

    # res = get_transaction_info(
    #     server_url=config['server_url'],
    #     service_api_key=config['service_api_key'],
    #     service_api_secret=config['service_api_secret'],
    #     txHash="DCD0B2D32E9329D77AA642A55DC10469A876767493D2F60254A70E4DCD099202"
    # )
    # pprint(res)
