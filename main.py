import base64
import time
import hashlib
import json

from NFT import NFT
from ST import ServiceToken
from utils import get_transaction_info


class Image:
    def __init__(
        self,
        imageURI: str,
        name: str,
        description: dict,  # Artist address (*) , Agency, Schedule, Date Taken, etc.
        number,
        price
    ):
        with open(imageURI, 'rb') as f:
            self.contents = base64.b64encode(f.read())
        self.name = name
        self.description = description
        self.number = str(number)
        self.price = str(price)
        self.hash = self.get_hash()

    def get_hash(self):
        return hashlib.sha256(self.contents).hexdigest()

    def updata_price(self, new_price: int):
        self.price = new_price


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

        self.artist_fee = 0.0025  # 0.25%
        self.platform_fee = 0.0005  # 0.05%

        self.config = config

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

    def upload_image(
        self,
        who: str,
        imageURI: str,
        name: str,
        description: str,
        amount: int,
        price: int
    ):
        # condition: only user can upload image(s)
        if not self.is_user(who):
            return

        res = []

        # mint NFT
        for i in range(amount):
            image = Image(
                imageURI=imageURI,
                name=name,
                description=description,
                number=i,
                price=price
            )
            res.append(
                self.nft.mint(
                    to_=who,
                    name=name,
                    meta=json.dumps({
                        'hash': image.hash,
                        'artist': image.description['artist'],
                        'price': image.price
                    })
                )
            )

        return res

    def buy(
        self,
        fromAddress: str,
        toAddress: str,
        tokenIndex: str,
        price: str
    ):
        meta = json.loads(self.nft.get_info(tokenIndex)['responseData']['meta'])
        artistAddress = str(meta['artist'])
        price_ = str(meta['price'])

        if price != price_:
            return

        price = int(price)
        for_artist = int(price * self.artist_fee)
        for_platform = int(price * self.platform_fee)
        for_receiver = int(price - for_artist - for_platform)

        price = str(price)
        for_artist = str(for_artist)
        for_platform = str(for_platform)
        for_receiver = str(for_receiver)

        res = []

        res.append(
            self.st.transfer(
                fromAddress=fromAddress,
                walletSecret=self.users[fromAddress],
                toAddress=toAddress,
                amount=for_receiver
            )
        )
        res.append(
            self.nft.transfer(
                fromAddress=toAddress,
                walletSecret=self.users[toAddress],
                toAddress=fromAddress,
                tokenIndex=tokenIndex
            )
        )
        res.append(
            self.st.transfer(
                fromAddress=fromAddress,
                walletSecret=self.users[fromAddress],
                toAddress=artistAddress,
                amount=for_artist
            )
        )
        res.append(
            self.st.transfer(
                fromAddress=fromAddress,
                walletSecret=self.users[fromAddress],
                toAddress=self.ownerAddress,
                amount=for_platform
            )
        )

        return res

    def collection(self, who: str):
        return self.users[who]


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
