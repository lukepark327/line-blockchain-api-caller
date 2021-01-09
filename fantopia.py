import base64
import time
import hashlib
import json

from NFT import NFT
from ST import ServiceToken
from utils import get_transaction_info


class ImageServer:
    def __init__(
        self,
        serverBaseURI: str = 'server_images'
    ):
        self.serverBaseURI = serverBaseURI

        # (name, id) => {URI, description, price, hash}
        self.images = dict()

    def upload_image(
        self,
        name: str,  # file_name.extension
        image_bytes,
        description: dict = None,
        number=0,
        price=None
    ):
        # Save the image at server
        _URI = self.serverBaseURI + '/' + name
        with open(_URI, 'wb') as f:
            f.write(image_bytes)

        _description = description
        _price = str(price) if price is not None else None
        _hash_value = self._hash(name)

        self.images[(name, str(number))] = {
            'URI': _URI,
            'description': _description,
            'price': _price,
            'hash': _hash_value
        }

    def _hash(self, name):
        _URI = self.serverBaseURI + '/' + name
        with open(_URI, 'rb') as f:
            _image_bytes = f.read()

        _contents = base64.b64encode(_image_bytes)
        return hashlib.sha256(_contents).hexdigest()

    # Setter

    def set_description(self, name, new_description: dict, number=0):
        self.images[(name, str(number))]['description'] = new_description

    def set_price(self, name, new_price, number=0):
        self.images[(name, str(number))]['price'] = str(new_price)

    # Getter

    def get_image_bytes(self, name, number=0):
        _URI = self.images[(name, str(number))]['URI']
        with open(_URI, 'rb') as f:
            _image_bytes = f.read()
        return _image_bytes

    def get_description(self, name, number=0):
        return self.images[(name, str(number))]['description']

    def get_price(self, name, number=0):
        return self.images[(name, str(number))]['price']

    def get_hash(self, name, number=0):
        return self.images[(name, str(number))]['hash']


class ProductServer:
    def __init__(
        self
    ):
        self.products = dict()

    def upload_product(
        self,
        name: str,
        nft_number: str,
        nft_name: str,
    ):
        self.products['name'] = {
            'nft_number': nft_number,
            'nft_name': nft_name
        }

    def get_product(
        self,
        name: str
    ):
        return self.products['name']

    def get_nft_detail(
        self,
        img_server: ImageServer,
        name: str
    ):
        _name = self.products['name']['nft_name']
        return img_server.get_description(_name)


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

        self.img_server = ImageServer(serverBaseURI='server_images')
        self.product_server = ProductServer()

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
        name: str,  # file_name.extension
        image_bytes,
        description: dict = None,
        amount=1,
        price=None
    ):
        # condition: only user can upload image(s)
        if not self.is_user(who):
            return

        res = []

        # mint NFT
        for i in range(amount):
            self.img_server.upload_image(
                name, image_bytes, description, i, price
            )

            _hash = self.img_server.get_hash(name=name)
            _description = description
            _price = price

            if (_description is not None) and (_price is not None):
                res.append(
                    self.nft.mint(
                        to_=who,
                        name=name,
                        meta=json.dumps({
                            'hash': _hash,
                            # 'SN'
                            'artist': _description['artist'],
                            'agency': _description['agency'],
                            'schedule': _description['schedule'],
                            'date': _description['date'],
                            'minted': _description['minted'],
                            # 'owner'
                            'price': _price
                        })
                    )
                )
            elif (_description is not None) and (_price is None):
                res.append(
                    self.nft.mint(
                        to_=who,
                        name=name,
                        meta=json.dumps({
                            'hash': _hash,
                            # 'SN'
                            'artist': _description['artist'],
                            'agency': _description['agency'],
                            'schedule': _description['schedule'],
                            'date': _description['date'],
                            'minted': _description['minted']
                            # 'owner'
                        })
                    )
                )
            elif (_description is None) and (_price is not None):
                res.append(
                    self.nft.mint(
                        to_=who,
                        name=name,
                        meta=json.dumps({
                            'hash': _hash,
                            'price': _price
                        })
                    )
                )
            else:  # (_description is None) and (_price is None)
                res.append(
                    self.nft.mint(
                        to_=who,
                        name=name,
                        meta=json.dumps({
                            'hash': _hash
                        })
                    )
                )

        return res

    def upload_detail(
        self,
        number: str,  # NFT number
        name: str,
        new_description: dict,
        amount=1,
        price=None
    ):
        res = []

        # update NFT
        for i in range(amount):
            self.img_server.set_description(
                name, new_description, i
            )

            _hash = self.img_server.get_hash(name=name)
            _description = new_description
            _price = self.img_server.get_price(name=name) or str(price)

            if _price is None:
                raise Exception('price MUST not be None')

            res.append(
                self.nft.update_info(
                    number=number,
                    name=name,
                    meta=json.dumps({
                        'hash': _hash,
                        # 'SN'
                        'artist': _description['artist'],
                        'agency': _description['agency'],
                        'schedule': _description['schedule'],
                        'date': _description['date'],
                        'minted': _description['minted'],
                        # 'owner'
                        'price': _price
                    })
                )
            )

        return res

    def upload_product(
        self,
        name: str,
        nft_number: str,
        nft_name: str,
    ):
        self.product_server.upload_product(name, nft_number, nft_name)

    def get_product(self, name: str):
        return self.product_server.get_product(name)

    def get_nft_detail(self, name: str):
        return self.product_server.get_nft_detail(self.img_server, name)

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
    name = '1.jpeg'
    with open('client_images/' + name, 'rb') as f:
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
