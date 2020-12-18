import base64
import time
import hashlib
import json
from flask import Flask

from main import Image, Fantopia
from NFT import NFT
from ST import ServiceToken
from utils import get_transaction_info


app = Flask('app')


@app.route('/')
def index():
    return "I'm from docker"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
