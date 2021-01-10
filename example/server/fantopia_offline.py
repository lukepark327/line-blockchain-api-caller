import base64
import time
import hashlib
import json

from DB import DB

import sys
sys.path.append('../../caller/')
from NFT import NFT
from ST import ServiceToken
from utils import get_transaction_info


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

        self.nft = NFT('10000001', owner, config)   # NFT
        self.st = ServiceToken(owner, config)       # [FAN]

        self.artist_fee = 0.0025    # 0.25%
        self.platform_fee = 0.0005  # 0.05%

        self.config = config

        self.DB = DB()
        print(self.insertSamples())

    def insertSamples(self):
        sample1 = {
            "pk": "1",
            "type": "image",
            "img_url": "https://w.namu.la/s/cc411f2978e4e15799cd982f19b5519012e1195f7ab39bd094d5b5098973d301149abfe1e394459909951f2bc13575d93f3f1e93dfb5ae6c7525dd4d840a2cb6f345c8e19ec2e259e5e46d98a23787d9e2f3f0bbb1b8cb33fa3e73b8de9844b9b16718fa3cb8dbb273aa547ae550f9b3",
            "schedule": "2020 아이유 부산콘서트",
            "description": "오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n",
            "is_favorite": True,
            "price": "0.324",
            "serial_num": "1000000100000019",
            "artist": "아이유",
            "artist_addr": "tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg",
            "owner_id": "clze01",
            "owner_addr": "tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd",
            "taken_date": "2020.11.24",
            "minted_date": "2020.12.02"
        }
        sample2 = {
            "pk": "2",
            "type": "product",
            "img_url": "https://w.namu.la/s/cc411f2978e4e15799cd982f19b5519012e1195f7ab39bd094d5b5098973d301149abfe1e394459909951f2bc13575d93f3f1e93dfb5ae6c7525dd4d840a2cb6f345c8e19ec2e259e5e46d98a23787d9e2f3f0bbb1b8cb33fa3e73b8de9844b9b16718fa3cb8dbb273aa547ae550f9b3",
            "schedule": "2019 아이유 부산콘서트",
            "description": "오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n",
            "is_favorite": False,
            "price": "0.324",
            "serial_num": "1000000100000018",
            "artist": "아이유",
            "artist_addr": "tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg",
            "owner_id": "clze01",
            "owner_addr": "tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd",
            "taken_date": "2020.11.24",
            "minted_date": "2020.12.02"
        }

        self.DB.table[self.DB._getPkIndex()] = sample1
        self.DB.table[self.DB._getPkIndex()] = sample2

        # blockchain
        res = []
        # res.append(self.nft.mint(
        #     to_=sample1['owner_addr'],
        #     name=sample1['pk'],
        #     meta=json.dumps(sample1)
        # ))
        # res.append(self.nft.mint(
        #         to_=sample2['owner_addr'],
        #         name=sample2['pk'],
        #         meta=json.dumps(sample2)
        # ))

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

    def buy(
        self,
        fromAddress: str,
        toAddress: str,
        tokenIndex: str,
        price: str
    ):
        # meta = json.loads(self.nft.get_info(tokenIndex)['responseData']['meta'])
        # artistAddress = meta['artist_addr']

        # price_ = meta['price']
        # if price != price_:
        #     return

        price = int(price)
        for_artist, for_platform = int(price * self.artist_fee), int(price * self.platform_fee)
        for_receiver = int(price - for_artist - for_platform)

        price = str(price)
        for_artist, for_platform, for_receiver =\
            str(for_artist), str(for_platform), str(for_receiver)

        # # blockchain
        # res = []
        # res.append(self.nft.transfer(
        #     fromAddress=toAddress,
        #     walletSecret=self.users[toAddress],
        #     toAddress=fromAddress,
        #     tokenIndex=tokenIndex
        # ))
        # res.append(self.st.transfer(
        #     fromAddress=fromAddress,
        #     walletSecret=self.users[fromAddress],
        #     toAddress=toAddress,
        #     amount=for_receiver
        # ))
        # res.append(self.st.transfer(
        #     fromAddress=fromAddress,
        #     walletSecret=self.users[fromAddress],
        #     toAddress=artistAddress,
        #     amount=for_artist
        # ))
        # res.append(self.st.transfer(
        #     fromAddress=fromAddress,
        #     walletSecret=self.users[fromAddress],
        #     toAddress=self.ownerAddress,
        #     amount=for_platform
        # ))

        # update DB
        # TBA

        # return txs
        # TBA
        return 'DCD0B2D32E9329D77AA642A55DC10469A876767493D2F60254A70E4DCD099202'


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
        fromAddress=user_B['address'],
        toAddress=user_A['address'],
        tokenIndex='00000085',
        price='10000'
    )
    pprint(res)

    res = get_transaction_info(
        server_url=config['server_url'],
        service_api_key=config['service_api_key'],
        service_api_secret=config['service_api_secret'],
        txHash="DCD0B2D32E9329D77AA642A55DC10469A876767493D2F60254A70E4DCD099202"
    )
    pprint(res)
