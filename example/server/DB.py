class DB:

    _pkIndex = 1

    def __init__(
        self
    ):
        # (pk) => {URI, description, price, hash}
        self.table = dict()

    # deprecated
    # def upload(self): pass

    def _getPkIndex(self):
        _tmpPkIndex = DB._pkIndex
        DB._pkIndex += 1
        return str(_tmpPkIndex)

    # def _hash(self, name):
    #     _URI = self.serverBaseURI + '/' + name
    #     with open(_URI, 'rb') as f:
    #         _image_bytes = f.read()

    #     _contents = base64.b64encode(_image_bytes)
    #     return hashlib.sha256(_contents).hexdigest()

    # Getter

    def getImage(self, primaryKey: str):
        return self.table[primaryKey]

    def getAllImages(self, startNum=0, endNum=100):
        return [self.table[str(pk)] for pk in range(max(startNum, 1), min(endNum, DB._pkIndex))]

    # Update

    def updateFavorite(self, primaryKey: str, favor=True):
        self.table[primaryKey]["is_favorite"] = favor

    # def set_description(self, name, new_description: dict, number=0):
    #     self.images[(name, str(number))]['description'] = new_description

    # def set_price(self, name, new_price, number=0):
    #     self.images[(name, str(number))]['price'] = str(new_price)

    def sellReset(self, startNum=0, endNum=100):
        for pk in range(max(startNum, 1), min(endNum, DB._pkIndex)):
            self.table[str(pk)]['is_selled'] = False
