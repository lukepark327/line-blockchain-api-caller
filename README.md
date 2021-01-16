# line-blockchain-api-caller
Python implementations of LINE blockchain API caller.

See [`./caller`](https://github.com/lukepark327/line-blockchain-api-caller/tree/main/caller) for source codes.

---

# :european_castle: Fantopia

The concrete example of LINE blockchain API caller.

<!--
*Fantopia* is the ...
-->

# Run (Server-side)

```
cd example/server
python app.py
```

*or*

```
cd example/server
docker build -t fantopia:latest .
docker run -d -p 5000:5000 fantopia
```

# Curl (Client-side)

```
cd example/client
```

## :couple: User

### Add artist

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/addartist -d '{"address": "tlink1e38npkztaq90vvc3gnjhn0th8w52na005ahqf0", "secret": "QC3PbuSMC101uDBCOTWJeCsjSCuI57XvVnUDH8623iw="}'
```

* `address`: Wallet address
* `secret`: PW

### Add user

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/adduser -d '{"address": "tlink18vsd3cautlyt759sw5hq9tydhzrsrgrmprs4f0", "secret": "gD6Skn0b66WLt5oq8OYe0ejI4OzjthyWMYm4V7gqamg="}'
```
```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/adduser -d '{"address": "tlink1lnl66me3geg6t2l62w07rx5j2utewvn54908vd", "secret": "UkbP/u5dyLqj2vUELA0WMQtcwaA5IxBEomYmdojX3uY="}'
```
* `address`: Wallet address
* `secret`: PW

## :floppy_disk: Image

<!--
### Upload image

```
curl -i -X PUT http://localhost:5000/uploadimage -F who="tlink1jweegl733lmfdusfknelge8d82ftcfmrnm3r48" -F name="1.jpeg" -F file=@"client_images/1.jpeg" -F amount="5"
```

* `who`: Wallet address of uploader
* `name`: Unique name of the file
* `file`: URI of the file
* `amount`: (optional) How many images you want to sell
* `price`: (optional) Price of the image

### Upload detail of image

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/uploaddetail -d '{"tokenIndex": "00000085", "name": "1.jpeg", "description": {"artist": "tlink1e38npkztaq90vvc3gnjhn0th8w52na005ahqf0", "agency": "Loen Entertainment", "schedule": "2019 IU concert", "date": "12/01/2019", "minted": "01/12/2020"}, "amount": "5", "price": "10000"}'
```

* `tokenIndex`: NFT token index
* `name`: Unique name of the file
* `description`: dictionary-like details about the image. It MUST includes `artist`, `agency`, `schedule`, `date` and `minted` fields.
* `amount`: (optional) How many images you want to sell
* `price`: (optional) Price of the image
-->

### Get one image

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/getimage -d '{"pk": "1"}'
```

### Get multiple images

```
curl -X POST http://localhost:5000/getallimages
```

*or*

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/getallimages -d '{"startNum": 1, "endNum": 3}'
```

### Update detail: favorite

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/updatefavorite -d '{"pk": "2"}'
```

*or*

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/updatefavorite -d '{"pk": "2", "favor": true}'
```

### Reset detail: sell

```
curl -X POST http://localhost:5000/sellreset
```

*or*

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/sellreset -d '{"startNum": 1, "endNum": 3}'
```

### Buy image

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/buyimage -d '{"pk": "1", "fromAddress": "tlink1lnl66me3geg6t2l62w07rx5j2utewvn54908vd", "toAddress": "tlink18vsd3cautlyt759sw5hq9tydhzrsrgrmprs4f0"}'
```

*or*

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/buyimage -d '{"pk": "1", "fromAddress": "tlink1lnl66me3geg6t2l62w07rx5j2utewvn54908vd", "toAddress": "tlink18vsd3cautlyt759sw5hq9tydhzrsrgrmprs4f0", "tokenIndex": "000000c3", "price": "100"}'
```

* `pk`: Primary Key.
* `fromAddress`: Wallet address of buyer
* `toAddress`: Wallet address of image seller
* `tokenIndex`: (optional) NFT token index
* `price`: (optional) Price of the image. It MUST be higher or same as seller-uploaded price.

<!--
## :coffee: Product

### Upload product

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/uploadproduct -d '{"name": "Cup", "nft_number": "00000085", "nft_name": "1.jpeg"}'
```

* `name`: Unique name of the product
* `nft_number`: NFT token index
* `nft_name`: Unique name of the image

### Get one image of product

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/getproductimage -d '{"name": "Cup"}'
```

If saving file is needed, try:

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/getproductimage -d '{"name": "Cup"}' > output.jpeg
```

**Notice**: Python Flask supports sending only one file at once.

### Get detail of product

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/getproductdetail -d '{"name": "Cup"}'
```

* `name`: Unique name of the product

### Get multiple products' detail

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/getproductdetails -d '{"names": ["Cup"]}'
```

* `names`: The array of the multiple products' name
-->

## :wrench: Utils

### Get Service Token Balance

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/getbalance -d '{"address": "tlink18vsd3cautlyt759sw5hq9tydhzrsrgrmprs4f0"}'
```

### Get NFT info.

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/getinfo -d '{"tokenIndex": "000000c3"}'
```
### Get transaction info.

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/gettx -d '{"txHash": "DCD0B2D32E9329D77AA642A55DC10469A876767493D2F60254A70E4DCD099202"}'
```

<!--
### Test

```
curl http://localhost:5000/test
```
-->
