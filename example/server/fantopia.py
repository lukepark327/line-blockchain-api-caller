import base64
import time
import hashlib
import json

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

        self.nft = NFT('10000001', owner, config)   # NFT
        self.st = ServiceToken(owner, config)       # [FAN]

        self.artist_fee = 0.0025    # 0.25%
        self.platform_fee = 0.0005  # 0.05%

        self.config = config

        self.DB = DB()
        print(self.insertSamples())

    def insertSamples(self):
        image1 = {'pk': '1', 'type': 'image', 'img_url': 'assets/images/characters/character1.jpg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                  'is_favorite': True, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                  'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        image2 = {'pk': '2', 'type': 'image', 'img_url': 'assets/images/characters/character2.jpg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                  'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                  'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        image3 = {'pk': '3', 'type': 'image', 'img_url': 'assets/images/characters/character3.jpeg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                  'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                  'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        image4 = {'pk': '4', 'type': 'image', 'img_url': 'assets/images/characters/character4.jpg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                  'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                  'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        image5 = {'pk': '5', 'type': 'image', 'img_url': 'assets/images/characters/character5.jpg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                  'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                  'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        image6 = {'pk': '6', 'type': 'image', 'img_url': 'assets/images/characters/character6.jpg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                  'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                  'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        image7 = {'pk': '7', 'type': 'image', 'img_url': 'assets/images/characters/character7.jpg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                  'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                  'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        image8 = {'pk': '8', 'type': 'image', 'img_url': 'assets/images/characters/character8.jpg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                  'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                  'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        image9 = {'pk': '9', 'type': 'image', 'img_url': 'assets/images/characters/character9.jpg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                  'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                  'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        image10 = {'pk': '10', 'type': 'image', 'img_url': 'assets/images/characters/character10.jpg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                   'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                   'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        item1 = {'pk': '11', 'type': 'product', 'img_url': 'assets/images/items/item1.jpeg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                 'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                 'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        item2 = {'pk': '12', 'type': 'product', 'img_url': 'assets/images/items/item2.jpeg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                 'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                 'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        item3 = {'pk': '13', 'type': 'product', 'img_url': 'assets/images/items/item3.jpeg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                 'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                 'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        item4 = {'pk': '14', 'type': 'product', 'img_url': 'assets/images/items/item4.jpeg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                 'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                 'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        item5 = {'pk': '15', 'type': 'product', 'img_url': 'assets/images/items/item5.jpeg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                 'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                 'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        item6 = {'pk': '16', 'type': 'product', 'img_url': 'assets/images/items/item6.jpeg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                 'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                 'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        item7 = {'pk': '17', 'type': 'product', 'img_url': 'assets/images/items/item7.jpeg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                 'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                 'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        item8 = {'pk': '18', 'type': 'product', 'img_url': 'assets/images/items/item8.jpeg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                 'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                 'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        item9 = {'pk': '19', 'type': 'product', 'img_url': 'assets/images/items/item9.jpeg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                 'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                 'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}
        item10 = {'pk': '20', 'type': 'product', 'img_url': 'assets/images/items/item10.jpeg', 'schedule': "2020 아이유 부산콘서트", 'description': '오막포 (캐논의 ‘EOS 5D 마크4’ 카메라) + 새아빠 (EF70-200mm F2.8L IS II USM)로 촬영한 고화질 사진입니다.\n\n2019 아이유 단독 콘서트 C2 구역 중앙에서 촬영하여 흔들림 없는 희귀 정면 사진입니다. 아이유, 장발, 콘서트. 진짜 왜 안사,,?\n',
                  'is_favorite': False, 'price': '0.324', 'serial_num': '1000000100000019', 'artist': '아이유', 'artist_addr': 'tlink1jr4z9698hzuued2alrc2t7vrd03c87mh8lcvcg',
                  'owner_id': 'clze01', 'owner_addr': 'tlink19ejywqvr8caj7yl43sjfqvlw9xjh54wgq5fmtd', 'taken_date': '2020.11.24', 'minted_date': '2020.12.02', 'is_selled': False}

        self.DB.table[self.DB._getPkIndex()] = image1
        self.DB.table[self.DB._getPkIndex()] = image2
        self.DB.table[self.DB._getPkIndex()] = image3
        self.DB.table[self.DB._getPkIndex()] = image4
        self.DB.table[self.DB._getPkIndex()] = image5
        self.DB.table[self.DB._getPkIndex()] = image6
        self.DB.table[self.DB._getPkIndex()] = image7
        self.DB.table[self.DB._getPkIndex()] = image8
        self.DB.table[self.DB._getPkIndex()] = image9
        self.DB.table[self.DB._getPkIndex()] = image10
        self.DB.table[self.DB._getPkIndex()] = item1
        self.DB.table[self.DB._getPkIndex()] = item2
        self.DB.table[self.DB._getPkIndex()] = item3
        self.DB.table[self.DB._getPkIndex()] = item4
        self.DB.table[self.DB._getPkIndex()] = item5
        self.DB.table[self.DB._getPkIndex()] = item6
        self.DB.table[self.DB._getPkIndex()] = item7
        self.DB.table[self.DB._getPkIndex()] = item8
        self.DB.table[self.DB._getPkIndex()] = item9
        self.DB.table[self.DB._getPkIndex()] = item10

        # blockchain
        res = []
        res.append(self.nft.mint(to_=image1['owner_addr'], name=image1['pk'], meta=json.dumps(image1)))
        res.append(self.nft.mint(to_=image2['owner_addr'], name=image2['pk'], meta=json.dumps(image2)))
        res.append(self.nft.mint(to_=image3['owner_addr'], name=image3['pk'], meta=json.dumps(image3)))
        res.append(self.nft.mint(to_=image4['owner_addr'], name=image4['pk'], meta=json.dumps(image4)))
        res.append(self.nft.mint(to_=image5['owner_addr'], name=image5['pk'], meta=json.dumps(image5)))
        res.append(self.nft.mint(to_=image6['owner_addr'], name=image6['pk'], meta=json.dumps(image6)))
        res.append(self.nft.mint(to_=image7['owner_addr'], name=image7['pk'], meta=json.dumps(image7)))
        res.append(self.nft.mint(to_=image8['owner_addr'], name=image8['pk'], meta=json.dumps(image8)))
        res.append(self.nft.mint(to_=image9['owner_addr'], name=image9['pk'], meta=json.dumps(image9)))
        res.append(self.nft.mint(to_=image10['owner_addr'], name=image10['pk'], meta=json.dumps(image10)))
        res.append(self.nft.mint(to_=item1['owner_addr'], name=item1['pk'], meta=json.dumps(item1)))
        res.append(self.nft.mint(to_=item2['owner_addr'], name=item2['pk'], meta=json.dumps(item2)))
        res.append(self.nft.mint(to_=item3['owner_addr'], name=item3['pk'], meta=json.dumps(item3)))
        res.append(self.nft.mint(to_=item4['owner_addr'], name=item4['pk'], meta=json.dumps(item4)))
        res.append(self.nft.mint(to_=item5['owner_addr'], name=item5['pk'], meta=json.dumps(item5)))
        res.append(self.nft.mint(to_=item6['owner_addr'], name=item6['pk'], meta=json.dumps(item6)))
        res.append(self.nft.mint(to_=item7['owner_addr'], name=item7['pk'], meta=json.dumps(item7)))
        res.append(self.nft.mint(to_=item8['owner_addr'], name=item8['pk'], meta=json.dumps(item8)))
        res.append(self.nft.mint(to_=item9['owner_addr'], name=item9['pk'], meta=json.dumps(item9)))
        res.append(self.nft.mint(to_=item10['owner_addr'], name=item10['pk'], meta=json.dumps(item10)))

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
        fromAddress: str,
        toAddress: str,
        tokenIndex: str,
        price: str,
        pk: str
    ):
        meta = json.loads(self.nft.get_info(tokenIndex)['responseData']['meta'])
        artistAddress = meta['artist_addr']

        price_ = meta['price']
        if price != price_:
            return

        self.DB.table[pk]['is_selled'] = True

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
        ))
        res.append(self.st.transfer(
            fromAddress=fromAddress,
            walletSecret=self.users[fromAddress],
            toAddress=toAddress,
            amount=for_receiver
        ))
        res.append(self.st.transfer(
            fromAddress=fromAddress,
            walletSecret=self.users[fromAddress],
            toAddress=artistAddress,
            amount=for_artist
        ))
        res.append(self.st.transfer(
            fromAddress=fromAddress,
            walletSecret=self.users[fromAddress],
            toAddress=self.ownerAddress,
            amount=for_platform
        ))

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
