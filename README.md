# line-blockchain-api-caller
python implementations of LINE blockchain API caller

# Run

```
python app.py
```

# Curl

## Add artist

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/adduser -d '{"address": "tlink1e38npkztaq90vvc3gnjhn0th8w52na005ahqf0", "secret": "QC3PbuSMC101uDBCOTWJeCsjSCuI57XvVnUDH8623iw="}'
```

* `address`: Wallet address
* `secret`: PW

## Add user

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/adduser -d '{"address": "tlink1jweegl733lmfdusfknelge8d82ftcfmrnm3r48", "secret": "zqDvlusIMR+Ci1WparUmk/CfKXeKtxCPR23SzbzGroo="}'
```
```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/adduser -d '{"address": "tlink1lnl66me3geg6t2l62w07rx5j2utewvn54908vd", "secret": "UkbP/u5dyLqj2vUELA0WMQtcwaA5IxBEomYmdojX3uY="}'
```
* `address`: Wallet address
* `secret`: PW

## Upload image

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/uploadimage -d '{"address": "tlink18vsd3cautlyt759sw5hq9tydhzrsrgrmprs4f0", "imageURI": "./images/1.jpeg", "name": "NVIDIA RTX TITAN", "description": {"artist": "tlink1e38npkztaq90vvc3gnjhn0th8w52na005ahqf0", "something": "nothing"}, "amount": "5", "price": "10000"}'
```

* `address`: Wallet address of uploader
* `imageURI`: URI of image at server-side (therefore, you need to send the image before calling the `uploadimage` API)
* `name`: Name of the image
* `description`: dictionary-like details about the image. It MUST includes an `artist` field.
* `amount`: How many images you want to sell
* `price`: Price of the image.

## Buy image

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/buyimage -d '{"fromAddress": "tlink1lnl66me3geg6t2l62w07rx5j2utewvn54908vd", "toAddress": "tlink1jweegl733lmfdusfknelge8d82ftcfmrnm3r48", "tokenIndex": "00000085", "price": "10000"}'
```

* `fromAddress`: Wallet address of buyer
* `toAddress`: Wallet address of image seller
* `tokenIndex`: NFT token index
* `price`: Price of the image. It MUST be same as seller-uploaded price.

## Get transaction info.

```
curl -X POST -H 'Content-Type: application/json' http://localhost:5000/gettx -d '{"txHash": "DCD0B2D32E9329D77AA642A55DC10469A876767493D2F60254A70E4DCD099202"}'
```
