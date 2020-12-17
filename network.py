import hmac, hashlib, base64


def get_signature(method, path, nonce, timestamp, service_api_secret, body=None):
    req = ''
    if body is not None:
        keys = sorted(body.keys())
        req = '&'.join([key_ + '=' + str(body[key_]) for key_ in keys])
    
    if req != '':
        requiredMsg = nonce + str(timestamp) + method + path + '?' + req
    else:
        requiredMsg = nonce + str(timestamp) + method + path
    # print(requiredMsg)

    hash_ = hmac.new(
        bytes(service_api_secret, 'utf-8'),
        bytes(requiredMsg, 'utf-8'),
        hashlib.sha512
    ).digest()
    res = base64.b64encode(hash_).strip()

    return res.decode()
